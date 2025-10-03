from colorama import init, Fore, Style # type: ignore

from framework.labeler.FxLabelerSetup import CFxLabelerSetup
from framework.labeler.FxLabelerBase import CFxLabelerBase


class CFxLabelerDefault(CFxLabelerBase):
    def __init__(self, setup: CFxLabelerSetup):
        super().__init__(setup)
        pass

    def labeling(self):
        import os
        import json
        import sqlite3
        from sklearn.preprocessing import LabelEncoder # type: ignore

        conn = sqlite3.connect(self.setup.db_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT {self.setup.db_label_column} FROM {self.setup.db_table}")
        rows = cursor.fetchall()
        conn.close()

        label_names = [ r[0] for r in rows ]
        label_encoder = LabelEncoder()
        label_encoder.fit(label_names)

        mapping = {label: int(idx) for idx, label in enumerate(label_encoder.classes_)}

        os.makedirs(self.setup.workspace, exist_ok=True)
        mapping_file = f"{self.setup.workspace}/label_mapping.json"
        with open(mapping_file, "w", encoding="utf-8") as f:
            json.dump(mapping, f, ensure_ascii=False, indent=2)

        print(label_encoder.classes_)
        pass

    pass