from colorama import init, Fore, Style # type: ignore

from framework.labeler.FxLabelerSetup import CFxLabelerSetup
from framework.labeler.FxLabelerBase import CFxLabelerBase


class CFxLabelerDefault(CFxLabelerBase):
    def __init__(self, setup: CFxLabelerSetup):
        super().__init__(setup)
        pass

    def labeling(self):
        import sqlite3
        from sklearn.preprocessing import LabelEncoder # type: ignore
        import numpy as np # type: ignore

        conn = sqlite3.connect(self.setup.db_working_path)
        try:
            cursor = conn.cursor()

            cursor.execute(f"SELECT item_id,main_category FROM products ORDER BY item_id")
            rows = cursor.fetchall()
            
            item_ids = []
            label_names = []

            for row in rows:
                item_ids.append(row[0])
                label_names.append(row[1])

            label_encoder = LabelEncoder()
            label_ids = label_encoder.fit_transform(label_names)
            for label_id in label_ids:
                print(label_id)
                break

            # Insert label id
            cursor.execute(f"DELETE FROM labels")
            cursor.executemany("INSERT INTO labels (item_id, label_id) VALUES (?, ?)", zip(item_ids, map(int,label_ids)))
            conn.commit()

            # Insert label mapping
            cursor.execute(f"DELETE FROM label_mappings")
            cursor.executemany("INSERT INTO label_mappings (label_id, label_name) VALUES (?, ?)", 
                                [(label_id, label_name) for label_id, label_name in enumerate(label_encoder.classes_)])
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            conn.close()
            pass
        pass

    pass