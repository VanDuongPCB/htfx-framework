import inspect
from colorama import init, Fore, Style # type: ignore
import numpy as np # type: ignore

from framework.embeder.FxEmbedderSetup import CFxEmbedderSetup
from framework.embeder.FxEmbedderBase import CFxEmbedderBase

class CFxEmbedSentenceTransformer(CFxEmbedderBase):
    def __init__(self, setup: CFxEmbedderSetup):
        super().__init__(setup)

    def embed(self, texts : list[str]) -> np.array:
        from sentence_transformers import SentenceTransformer # type: ignore
        if self.module is None:
            self.module = SentenceTransformer(self.setup.pretrained, device="cpu")
            if self.module is None:
                return None
            
        return self.module.encode(texts, batch_size = self.setup.batch_size, convert_to_numpy=True, show_progress_bar=True)
    

    # def save_module(self):
    #     print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
    #     pass

    # def load_from_module(self):
    #     print(f"{Fore.RED}[ {self.__class__.__name__} -> {inspect.currentframe().f_code.co_name} ] - Not Implementation!{Style.RESET_ALL}")
    #     pass