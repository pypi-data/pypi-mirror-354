from typing import Optional, List, Dict, Iterable

from ovos_config import Configuration
from ovos_plugin_manager.solvers import find_question_solver_plugins
from ovos_utils.log import LOG
from ovos_utils.fakebus import FakeBus

try:
    from ovos_plugin_manager.solvers import find_chat_solver_plugins
    from ovos_plugin_manager.templates.solvers import ChatMessageSolver
except ImportError:
    # using outdated ovos-plugin-manager
    class ChatMessageSolver:
        pass


    def find_chat_solver_plugins():
        return {}


class QuestionSolversService:
    def __init__(self, bus=None, config=None, sort_order=None):
        self.config_core = Configuration()
        self.loaded_modules = {}
        self.sort_order = sort_order or []
        self.bus = bus or FakeBus()
        self.config = config or {}
        self.load_plugins()

    def load_plugins(self):
        for plug_name, plug in find_question_solver_plugins().items():
            config = self.config.get(plug_name) or {}
            if not config.get("enabled", True):
                continue
            LOG.debug(f"loading plugin with cfg: {config}")
            self.loaded_modules[plug_name] = plug(config=config)
            LOG.info(f"loaded question solver plugin: {plug_name}")

        for plug_name, plug in find_chat_solver_plugins().items():
            config = self.config.get(plug_name) or {}
            if not config.get("enabled", True):
                continue
            LOG.debug(f"loading chat plugin with cfg: {config}")
            self.loaded_modules[plug_name] = plug(config=config)
            LOG.info(f"loaded chat solver plugin: {plug_name}")

        plugs = [p for p, c in self.config.items() if c.get("enabled", True)]
        for p in plugs:
            if p not in self.loaded_modules:
                raise ImportError(f"'{p}' not installed")

    @property
    def modules(self):
        if self.sort_order:
            return [self.loaded_modules[m] for m in self.sort_order]
        return sorted(self.loaded_modules.values(),
                      key=lambda k: k.priority)

    def shutdown(self):
        for module in self.modules:
            try:
                module.shutdown()
            except:
                pass

    def chat_completion(self, messages: List[Dict[str, str]],
                        lang: Optional[str] = None,
                        units: Optional[str] = None) -> Optional[str]:
        for module in self.modules:
            try:
                if isinstance(module, ChatMessageSolver):
                    ans = module.get_chat_completion(messages=messages, lang=lang, units=units)
                else:
                    LOG.debug(f"{module} does not supported chat history!")
                    query = messages[-1]["content"]
                    ans = module.spoken_answer(query, lang=lang, units=units)
                if ans:
                    return ans
            except Exception as e:
                LOG.error(e)

    def stream_completion(self, messages: List[Dict[str, str]],
                          lang: Optional[str] = None,
                          units: Optional[str] = None) -> Iterable[str]:
        answered = False
        for module in self.modules:
            try:
                if isinstance(module, ChatMessageSolver):
                    for ans in module.stream_chat_utterances(messages=messages, lang=lang, units=units):
                        answered = True
                        yield ans
                else:
                    LOG.debug(f"{module} does not supported chat history!")
                    query = messages[-1]["content"]
                    for ans in module.stream_utterances(query, lang=lang, units=units):
                        answered = True
                        yield ans
            except Exception as e:
                LOG.error(e)
            if answered:
                break
