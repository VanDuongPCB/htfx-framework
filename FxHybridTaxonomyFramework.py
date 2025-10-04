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
        np.save(f"{self.setup.workspace}/embeddings.npy", vecs)
        print(f"{Fore.GREEN}Embedding succeeded!{Style.RESET_ALL}")
        print(vecs.shape)
        return vecs
        pass