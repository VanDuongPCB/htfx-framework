import inspect
from colorama import init, Fore, Style # type: ignore

from framework.labeler.FxLabelerSetup import CFxLabelerSetup

class CFxLabelerBase:
    def __init__(self, setup: CFxLabelerSetup):
        self.setup = setup
        pass


    def labeling(self):
        print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
        pass
    pass