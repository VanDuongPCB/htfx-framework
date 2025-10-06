
class CFxEmbedderSetup:
    def __init__(self):
        self.framework = None
        self.pretrained = None
        self.device:str = "auto"
        self.batch_size = 32
        self.db_working_path = None
        pass