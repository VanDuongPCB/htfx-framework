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
            self.module = SentenceTransformer(self.setup.pretrained, device=self.setup.device)
            if self.module is None:
                return None
            
        return self.module.encode(texts, batch_size = self.setup.batch_size, convert_to_numpy=True, show_progress_bar=True)
    
    def embed_text(self, text) -> np.array:
        from sentence_transformers import SentenceTransformer # type: ignore
        if self.module is None:
            self.module = SentenceTransformer(self.setup.pretrained, device=self.setup.device)
            if self.module is None:
                return None
        
        texts = [text]
        return self.module.encode(texts, batch_size = self.setup.batch_size, convert_to_numpy=True, show_progress_bar=False)