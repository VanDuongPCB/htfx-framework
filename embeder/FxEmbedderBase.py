import inspect
from colorama import init, Fore, Style # type: ignore
import numpy as np # type: ignore

from framework.embeder.FxEmbedderSetup import CFxEmbedderSetup

class CFxEmbedderBase:
    def __init__(self, setup: CFxEmbedderSetup):
        self.setup = setup
        self.module = None
        pass

    def embed(self, texts : list[str]) -> np.array:
        print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
        return None
        pass

    def save_module(self):
        print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
        pass

    def load_from_module(self):
        print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
        pass