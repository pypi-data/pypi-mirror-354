import time
from threading import Event
from typing import Optional, List

from ovos_bus_client.message import Message
from ovos_bus_client.session import SessionManager, UtteranceState, Session
from ovos_bus_client.util import get_message_lang
from ovos_config.config import Configuration
from ovos_config.locale import setup_locale
from ovos_plugin_manager.templates.pipeline import PipelineMatch, PipelinePlugin
from ovos_utils import flatten_list
from ovos_utils.lang import standardize_lang_tag
from ovos_utils.log import LOG
from ovos_workshop.permissions import ConverseMode, ConverseActivationMode


class ConverseService(PipelinePlugin):
    """Intent Service handling conversational skills."""

    def __init__(self, bus):
        self.bus = bus
        self._consecutive_activations = {}
        self.bus.on('mycroft.speech.recognition.unknown', self.reset_converse)
        self.bus.on('intent.service.skills.deactivate', self.handle_deactivate_skill_request)
        self.bus.on('intent.service.skills.activate', self.handle_activate_skill_request)
        self.bus.on('active_skill_request', self.handle_activate_skill_request)  # TODO backwards compat, deprecate
        self.bus.on('intent.service.active_skills.get', self.handle_get_active_skills)
        self.bus.on("skill.converse.get_response.enable", self.handle_get_response_enable)
        self.bus.on("skill.converse.get_response.disable", self.handle_get_response_disable)
        super().__init__(config=Configuration().get("skills", {}).get("converse") or {})

    @property
    def active_skills(self):
        session = SessionManager.get()
        return session.active_skills

    @active_skills.setter
    def active_skills(self, val):
        session = SessionManager.get()
        session.active_skills = []
        for skill_id, ts in val:
            session.activate_skill(skill_id)

    @staticmethod
    def get_active_skills(message: Optional[Message] = None) -> List[str]:
        """Active skill ids ordered by converse priority
        this represents the order in which converse will be called

        Returns:
            active_skills (list): ordered list of skill_ids
        """
        session = SessionManager.get(message)
        return [skill[0] for skill in session.active_skills]

    def deactivate_skill(self, skill_id: str, source_skill: Optional[str] = None,
                         message: Optional[Message] = None):
        """Remove a skill from being targetable by converse.

        Args:
            skill_id (str): skill to remove
            source_skill (str): skill requesting the removal
            message (Message): the bus message that requested deactivation
        """
        source_skill = source_skill or skill_id
        if self._deactivate_allowed(skill_id, source_skill):
            session = SessionManager.get(message)
            if session.is_active(skill_id):
                # update converse session
                session.deactivate_skill(skill_id)

                # keep message.context
                message = message or Message("")
                message.context["session"] = session.serialize()  # update session active skills
                # send bus event
                self.bus.emit(
                    message.forward("intent.service.skills.deactivated",
                                    data={"skill_id": skill_id}))
                if skill_id in self._consecutive_activations:
                    self._consecutive_activations[skill_id] = 0

    def activate_skill(self, skill_id: str, source_skill: Optional[str] = None,
                       message: Optional[Message] = None) -> Optional[Session]:
        """Add a skill or update the position of an active skill.

        The skill is added to the front of the list, if it's already in the
        list it's removed so there is only a single entry of it.

        Args:
            skill_id (str): identifier of skill to be added.
            source_skill (str): skill requesting the removal
            message (Message): the bus message that requested activation
        """
        source_skill = source_skill or skill_id
        if self._activate_allowed(skill_id, source_skill):
            # update converse session
            session = SessionManager.get(message)
            session.activate_skill(skill_id)

            # keep message.context
            message = message or Message("")
            message.context["session"] = session.serialize()  # update session active skills
            message = message.forward("intent.service.skills.activated",
                                      {"skill_id": skill_id})
            # send bus event
            self.bus.emit(message)
            # update activation counter
            self._consecutive_activations[skill_id] += 1
            return session

    def _activate_allowed(self, skill_id: str, source_skill: Optional[str] = None) -> bool:
        """Checks if a skill_id is allowed to jump to the front of active skills list

        - can a skill activate a different skill
        - is the skill blacklisted from conversing
        - is converse configured to only allow specific skills
        - did the skill activate too many times in a row

        Args:
            skill_id (str): identifier of skill to be added.
            source_skill (str): skill requesting the removal

        Returns:
            permitted (bool): True if skill can be activated
        """

        # cross activation control if skills can activate each other
        if not self.config.get("cross_activation"):
            source_skill = source_skill or skill_id
            if skill_id != source_skill:
                # different skill is trying to activate this skill
                return False

        # mode of activation dictates under what conditions a skill is
        # allowed to activate itself
        acmode = self.config.get("converse_activation") or \
                 ConverseActivationMode.ACCEPT_ALL
        if acmode == ConverseActivationMode.PRIORITY:
            prio = self.config.get("converse_priorities") or {}
            # only allowed to activate if no skill with higher priority is
            # active, currently there is no api for skills to
            # define their default priority, this is a user/developer setting
            priority = prio.get(skill_id, 50)
            if any(p > priority for p in
                   [prio.get(s, 50) for s in self.get_active_skills()]):
                return False
        elif acmode == ConverseActivationMode.BLACKLIST:
            if skill_id in self.config.get("converse_blacklist", []):
                return False
        elif acmode == ConverseActivationMode.WHITELIST:
            if skill_id not in self.config.get("converse_whitelist", []):
                return False

        # limit of consecutive activations
        default_max = self.config.get("max_activations", -1)
        # per skill override limit of consecutive activations
        skill_max = self.config.get("skill_activations", {}).get(skill_id)
        max_activations = skill_max or default_max
        if skill_id not in self._consecutive_activations:
            self._consecutive_activations[skill_id] = 0
        if max_activations < 0:
            pass  # no limit (mycroft-core default)
        elif max_activations == 0:
            return False  # skill activation disabled
        elif self._consecutive_activations.get(skill_id, 0) > max_activations:
            return False  # skill exceeded authorized consecutive number of activations
        return True

    def _deactivate_allowed(self, skill_id: str, source_skill: Optional[str] = None) -> bool:
        """Checks if a skill_id is allowed to be removed from active skills list

        - can a skill deactivate a different skill

        Args:
            skill_id (str): identifier of skill to be added.
            source_skill (str): skill requesting the removal

        Returns:
            permitted (bool): True if skill can be deactivated
        """
        # cross activation control if skills can deactivate each other
        if not self.config.get("cross_activation"):
            source_skill = source_skill or skill_id
            if skill_id != source_skill:
                # different skill is trying to deactivate this skill
                return False
        return True

    def _converse_allowed(self, skill_id: str) -> bool:
        """Checks if a skill_id is allowed to converse

        - is the skill blacklisted from conversing
        - is converse configured to only allow specific skills

        Args:
            skill_id (str): identifier of skill that wants to converse.

        Returns:
            permitted (bool): True if skill can converse
        """
        opmode = self.config.get("converse_mode",
                                 ConverseMode.ACCEPT_ALL)
        if opmode == ConverseMode.BLACKLIST and skill_id in \
                self.config.get("converse_blacklist", []):
            return False
        elif opmode == ConverseMode.WHITELIST and skill_id not in \
                self.config.get("converse_whitelist", []):
            return False
        return True

    def _collect_converse_skills(self, message: Message) -> List[str]:
        """use the messagebus api to determine which skills want to converse
        This includes all skills and external applications"""
        session = SessionManager.get(message)

        skill_ids = []
        # include all skills in get_response state
        want_converse = [skill_id for skill_id, state in session.utterance_states.items()
                         if state == UtteranceState.RESPONSE]
        skill_ids += want_converse  # dont wait for these pong answers (optimization)

        active_skills = self.get_active_skills()

        if not active_skills:
            return want_converse

        event = Event()

        def handle_ack(msg):
            nonlocal event
            skill_id = msg.data["skill_id"]

            # validate the converse pong
            if all((skill_id not in want_converse,
                    msg.data.get("can_handle", True),
                    skill_id in active_skills)):
                want_converse.append(skill_id)

            if skill_id not in skill_ids:  # track which answer we got
                skill_ids.append(skill_id)

            if all(s in skill_ids for s in active_skills):
                # all skills answered the ping!
                event.set()

        self.bus.on("skill.converse.pong", handle_ack)

        # ask skills if they want to converse
        for skill_id in active_skills:
            self.bus.emit(message.forward(f"{skill_id}.converse.ping",
                                          {"skill_id": skill_id}))

        # wait for all skills to acknowledge they want to converse
        event.wait(timeout=0.5)

        self.bus.remove("skill.converse.pong", handle_ack)
        return want_converse

    def _check_converse_timeout(self, message: Message):
        """ filter active skill list based on timestamps """
        timeouts = self.config.get("skill_timeouts") or {}
        def_timeout = self.config.get("timeout", 300)
        session = SessionManager.get(message)
        session.active_skills = [
            skill for skill in session.active_skills
            if time.time() - skill[1] <= timeouts.get(skill[0], def_timeout)]

    def converse(self, utterances: List[str], skill_id: str, lang: str, message: Message) -> bool:
        """Call skill and ask if they want to process the utterance.

        Args:
            utterances (list of tuples): utterances paired with normalized
                                         versions.
            skill_id: skill to query.
            lang (str): current language
            message (Message): message containing interaction info.

        Returns:
            handled (bool): True if handled otherwise False.
        """
        lang = standardize_lang_tag(lang)
        session = SessionManager.get(message)
        session.lang = lang

        state = session.utterance_states.get(skill_id, UtteranceState.INTENT)
        if state == UtteranceState.RESPONSE:
            converse_msg = message.reply(f"{skill_id}.converse.get_response",
                                         {"utterances": utterances,
                                          "lang": lang})
            self.bus.emit(converse_msg)
            return True

        if self._converse_allowed(skill_id):
            converse_msg = message.reply(f"{skill_id}.converse.request",
                                         {"utterances": utterances,
                                          "lang": lang})
            result = self.bus.wait_for_response(converse_msg,
                                                'skill.converse.response',
                                                timeout=self.config.get("max_skill_runtime", 10))
            if result and 'error' in result.data:
                error_msg = result.data['error']
                LOG.error(f"{skill_id}: {error_msg}")
                return False
            elif result is not None:
                return result.data.get('result', False)
            else:
                # abort any ongoing converse
                # if skill crashed or returns False, all good
                # if it is just taking a long time, more than 1 skill would end up answering
                self.bus.emit(message.forward("ovos.skills.converse.force_timeout",
                                              {"skill_id": skill_id}))
                LOG.warning(f"{skill_id} took too long to answer, "
                            f'increasing "max_skill_runtime" in mycroft.conf might help alleviate this issue')
        return False

    def converse_with_skills(self, utterances: List[str], lang: str, message: Message) -> Optional[PipelineMatch]:
        """
        Attempt to converse with active skills for a given set of utterances.
        
        Iterates through active skills to find one that can handle the utterance. Filters skills based on timeout and blacklist status.
        
        Args:
            utterances (List[str]): List of utterance strings to process
            lang (str): 4-letter ISO language code for the utterances
            message (Message): Message context for generating a reply
        
        Returns:
            PipelineMatch: Match details if a skill successfully handles the utterance, otherwise None
            - handled (bool): Whether the utterance was fully handled
            - match_data (dict): Additional match metadata
            - skill_id (str): ID of the skill that handled the utterance
            - updated_session (Session): Current session state after skill interaction
            - utterance (str): The original utterance processed
        
        Notes:
            - Standardizes language tag
            - Filters out blacklisted skills
            - Checks for skill conversation timeouts
            - Attempts conversation with each eligible skill
        """
        lang = standardize_lang_tag(lang)
        session = SessionManager.get(message)

        # we call flatten in case someone is sending the old style list of tuples
        utterances = flatten_list(utterances)
        # filter allowed skills
        self._check_converse_timeout(message)
        # check if any skill wants to handle utterance
        for skill_id in self._collect_converse_skills(message):
            if skill_id in session.blacklisted_skills:
                LOG.debug(f"ignoring match, skill_id '{skill_id}' blacklisted by Session '{session.session_id}'")
                continue
            LOG.debug(f"Attempting to converse with skill: {skill_id}")
            if self.converse(utterances, skill_id, lang, message):
                state = session.utterance_states.get(skill_id, UtteranceState.INTENT)
                return PipelineMatch(handled=state != UtteranceState.RESPONSE,
                                     # handled == True -> emit "ovos.utterance.handled"
                                     match_data={},
                                     skill_id=skill_id,
                                     updated_session=session,
                                     utterance=utterances[0])
        return None

    @staticmethod
    def handle_get_response_enable(message: Message):
        skill_id = message.data["skill_id"]
        session = SessionManager.get(message)
        session.enable_response_mode(skill_id)
        if session.session_id == "default":
            SessionManager.sync(message)

    @staticmethod
    def handle_get_response_disable(message: Message):
        skill_id = message.data["skill_id"]
        session = SessionManager.get(message)
        session.disable_response_mode(skill_id)
        if session.session_id == "default":
            SessionManager.sync(message)

    def handle_activate_skill_request(self, message: Message):
        # TODO imperfect solution - only a skill can activate itself
        # someone can forge this message and emit it raw, but in OpenVoiceOS all
        # skill messages should have skill_id in context, so let's make sure
        # this doesnt happen accidentally at very least
        skill_id = message.data['skill_id']
        source_skill = message.context.get("skill_id")
        self.activate_skill(skill_id, source_skill, message)
        sess = SessionManager.get(message)
        if sess.session_id == "default":
            SessionManager.sync(message)

    def handle_deactivate_skill_request(self, message: Message):
        # TODO imperfect solution - only a skill can deactivate itself
        # someone can forge this message and emit it raw, but in ovos-core all
        # skill message should have skill_id in context, so let's make sure
        # this doesnt happen accidentally
        skill_id = message.data['skill_id']
        source_skill = message.context.get("skill_id") or skill_id
        self.deactivate_skill(skill_id, source_skill, message)
        sess = SessionManager.get(message)
        if sess.session_id == "default":
            SessionManager.sync(message)

    def reset_converse(self, message: Message):
        """Let skills know there was a problem with speech recognition"""
        lang = get_message_lang()
        self.converse_with_skills([], lang, message)

    def handle_get_active_skills(self, message: Message):
        """Send active skills to caller.

        Argument:
            message: query message to reply to.
        """
        self.bus.emit(message.reply("intent.service.active_skills.reply",
                                    {"skills": self.get_active_skills(message)}))

    def shutdown(self):
        self.bus.remove('mycroft.speech.recognition.unknown', self.reset_converse)
        self.bus.remove('intent.service.skills.deactivate', self.handle_deactivate_skill_request)
        self.bus.remove('intent.service.skills.activate', self.handle_activate_skill_request)
        self.bus.remove('active_skill_request', self.handle_activate_skill_request)  # TODO backwards compat, deprecate
        self.bus.remove('intent.service.active_skills.get', self.handle_get_active_skills)
        self.bus.remove("skill.converse.get_response.enable", self.handle_get_response_enable)
        self.bus.remove("skill.converse.get_response.disable", self.handle_get_response_disable)
