from colorama import init, Fore, Style # type: ignore

from framework.labeler.FxLabelerSetup import CFxLabelerSetup
from framework.labeler.FxLabelerBase import CFxLabelerBase


class CFxLabelerHDBSCAN(CFxLabelerBase):
    def __init__(self, setup: CFxLabelerSetup):
        super().__init__(setup)
        pass