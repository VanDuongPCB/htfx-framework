# Common
import os
import shutil
from colorama import init, Fore, Style # type: ignore
import numpy as np

# Framework
from framework.FxHybridTaxonomyFrameworkSetup import CFxHybridTaxonomyFrameworkSetup

# Labeler
from framework.labeler.FxLabelerSetup import CFxLabelerSetup
from framework.labeler.FxLabelerBase import CFxLabelerBase
from framework.labeler.FxLabelerDefault import CFxLabelerDefault
from framework.labeler.FxLabelerKMeans import CFxLabelerKMeans
from framework.labeler.FxLabelerMiniBatchKMeans import CFxLabelerMiniBatchKMeans
from framework.labeler.FxLabelerHDBSCAN import CFxLabelerHDBSCAN

# Embedder
from framework.embeder.FxEmbedderSetup import CFxEmbedderSetup
from framework.embeder.FxEmbedderBase import CFxEmbedderBase
from framework.embeder.FxEmbedderSentenceTransformer import CFxEmbedSentenceTransformer

# Classifier
from framework.classifier.FxClassifierSetup import CFxClassifierSetup

# Searcher
from framework.searcher.FxSearcherSetup import CFxSearcherSetup

class CFxHybridTaxonomyFramework:
    def __init__(self):
        self.setup = None
        
        self.labeler: CFxLabelerBase = None
        self.embedder: CFxEmbedderBase = None
        self.classifier = None
        self.searcher = None
        pass

    def setup_fx(self, setup: CFxHybridTaxonomyFrameworkSetup, force = False) -> bool:
        self.setup = setup
        if force and os.path.exists(setup.workspace):
            shutil.rmtree(setup.workspace)
        os.makedirs(setup.workspace, exist_ok=True)
        return True

    def setup_labeler(self, setup: CFxLabelerSetup) -> bool:
        if setup is None:
            self.labeler = None
            return False
        
        if setup.method == "kmeans":
            self.labeler = CFxLabelerKMeans(setup)
        elif setup.method == "mini-batch-kmeans":
            self.labeler = CFxLabelerMiniBatchKMeans(setup)
        elif setup.method == "hdbscan":
            self.labeler = CFxLabelerHDBSCAN(setup)
        elif setup.method == "default":
            self.labeler = CFxLabelerDefault(setup)
        else:
            self.labeler = CFxLabelerDefault(setup)
            pass

        return True

    def setup_embedder(self, setup: CFxEmbedderSetup):
        if setup.framework == "sentence-transformers":
            self.embedder = CFxEmbedSentenceTransformer(setup)
        pass

    def setup_classifier(self, setup: CFxClassifierSetup):
        pass

    def setup_searcher(self, setup: CFxSearcherSetup):
        pass

    ##########################################################################
    def initialize(self, force = False):
        if force and os.path.exists(self.setup.workspace):
            shutil.rmtree(self.setup.workspace)
        
        os.makedirs(self.setup.workspace)

        # Copy DB
        if not os.path.exists(self.setup.db_working_path):
            shutil.copy(self.setup.db_source_path, self.setup.db_working_path)

        # Create tables
        import sqlite3
        conn = sqlite3.connect(self.setup.db_working_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS labels (
                item_id INTEGER PRIMARY KEY,
                label_id INTEGER NOT NULL
            )
            """)
        conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS label_mappings (
                label_id INTEGER PRIMARY KEY,
                label_name TEXT NOT NULL
            )
            """)
        conn.commit()

        conn.close()


        pass

    def labeling(self):
        print(f"{Fore.CYAN}Labeling...{Style.RESET_ALL}", end="\r")
        self.labeler.labeling()
        print(f"{Fore.GREEN}Labeling succeeded!{Style.RESET_ALL}")
        pass

    def embedding(self):
        print(f"{Fore.CYAN}Embedding...{Style.RESET_ALL}", end="\r")

        import sqlite3
        from sklearn.model_selection import train_test_split # type: ignore

        # Remove dirs
        train_dir = f"{self.setup.workspace}/train"
        test_dir = f"{self.setup.workspace}/test"
        new_dir = f"{self.setup.workspace}/new"

        if os.path.exists(train_dir):
            shutil.rmtree(train_dir)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)

        # Load from DB
        query = """
            SELECT 
                p.item_id,
                l.label_id,
                p.title,
                p.features,
                p.description
            FROM 
                products AS p
            JOIN 
                labels AS l
            ON 
                p.item_id = l.item_id
            ORDER BY p.item_id;
            """

        print(f"{Fore.CYAN}Embedding - load data from database...{Style.RESET_ALL}", end="\r")
        conn = sqlite3.connect(self.setup.db_working_path)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        print(f"{Fore.CYAN}Embedding - format text...{Style.RESET_ALL}", end="\r")
        item_ids = []
        label_ids = []
        texts = []
        for row in rows:
            item_ids.append(row[0])
            label_ids.append(row[1])
            row = row[2:]
            format = " ".join(self.setup.embed_text_formats)
            formatted = format % row
            texts.append(formatted)
            # break
        rows = None

        print(f"{Fore.CYAN}Embedding - encoding...{Style.RESET_ALL}", end="\r")
        vecs = self.embedder.embed(texts)

        # Split
        train_item_ids, remain_item_ids, train_label_ids, remain_label_ids, train_vecs, remain_vecs = \
        train_test_split(
            item_ids, 
            label_ids, 
            vecs, 
            test_size=0.4, 
            random_state=42, 
            shuffle=True, 
            stratify=label_ids)
        item_ids = None
        label_ids = None
        vecs = None

        os.makedirs(train_dir, exist_ok=True)
        np.save(f"{train_dir}/vecs.npy", train_vecs)
        with open(f"{train_dir}/item_ids.txt", "w", encoding="utf-8") as f:
            for item in train_item_ids:
                f.write(f"{item}\n")
        with open(f"{train_dir}/label_ids.txt", "w", encoding="utf-8") as f:
            for item in train_label_ids:
                f.write(f"{item}\n")
        train_item_ids = None
        train_label_ids = None
        train_vecs = None

        test_item_ids, new_item_ids, test_label_ids, new_label_ids, test_vecs, new_vecs = \
        train_test_split(
            remain_item_ids, 
            remain_label_ids, 
            remain_vecs, 
            test_size=0.5, 
            random_state=42, 
            shuffle=True, 
            stratify=remain_label_ids)
        remain_item_ids = None
        remain_label_ids = None
        remain_vecs = None
        
        os.makedirs(test_dir, exist_ok=True)
        np.save(f"{test_dir}/vecs.npy", test_vecs)
        with open(f"{test_dir}/item_ids.txt", "w", encoding="utf-8") as f:
            for item in test_item_ids:
                f.write(f"{item}\n")
        with open(f"{test_dir}/label_ids.txt", "w", encoding="utf-8") as f:
            for item in test_label_ids:
                f.write(f"{item}\n")
        test_item_ids = None
        test_label_ids = None
        test_vecs = None

        os.makedirs(new_dir, exist_ok=True)
        np.save(f"{new_dir}/vecs.npy", new_vecs)
        with open(f"{new_dir}/item_ids.txt", "w", encoding="utf-8") as f:
            for item in new_item_ids:
                f.write(f"{item}\n")
        with open(f"{new_dir}/label_ids.txt", "w", encoding="utf-8") as f:
            for item in new_label_ids:
                f.write(f"{item}\n")
        new_item_ids = None
        new_label_ids = None
        new_vecs = None

        print(f"{Fore.GREEN}Embedding succeeded!{Style.RESET_ALL}")
        return True
        pass


    def train(self):
        pass

    def test(self):
        pass

    def recommend(self, text):
        pass