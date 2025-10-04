from framework.classifier.FxClassifierSetup import CFxClassifierSetup
from framework.classifier.FxClassifierBase import CFxClassifierBase

class CFxClassifierLogisticRegression(CFxClassifierBase):
    def __init__(self, setup: CFxClassifierSetup):
        super().__init__(setup)