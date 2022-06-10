import glob

from .utils import (
    BOHOUR_NAMES,
    find_mismatch,
    label2name,
    char2idx,
    override_auto_tashkeel,
    vocab,
    BOHOUR_NAMES_AR,
)
from .models import create_transformer_model, create_model_v1, create_era_theme_model
from tensorflow.keras.models import Model
from datasets import load_from_disk
import tkseem as tk
from keras.preprocessing.sequence import pad_sequences
from sentence_transformers import util
from bohour.arudi_style import get_arudi_style
from bohour.qafiah import get_qafiyah
from collections import Counter
from difflib import SequenceMatcher
from pyarabic.araby import strip_tashkeel
import traceback
import sys
import gdown
import bohour


class BaitAnalysis:
    def __init__(self, use_cbhg=True):

        self.BOHOUR_PATTERNS = {}
        self.BOHOUR_TAFEELAT = {}
        # abs_path = "/content/qawafi/qawafi_server"
        abs_path = "."
        for bahr_class in bohour.bohours_list:
            bahr = bahr_class()
            self.BOHOUR_PATTERNS[
                bahr_class.__name__.lower()
            ] = bahr.all_shatr_combinations_patterns
            self.BOHOUR_TAFEELAT[
                bahr_class.__name__.lower()
            ] = bahr.get_all_shatr_combinations(as_str_list=True)
        self.use_cbhg = use_cbhg
        if self.use_cbhg:
            print("load diacritization model ... ")
            try:
                from Arabic_Diacritization.predict import DiacritizationTester

                self.diac_model = DiacritizationTester(
                    "Arabic_Diacritization/config/test.yml", "cbhg"
                )
                self.text_encoder = self.diac_model.text_encoder
            except Exception as e:
                print(traceback.format_exc())
                print(
                    f"{e}. Maybe you should run 'git clone https://github.com/zaidalyafeai/Arabic_Diacritization'?"
                )
                raise e

        print("Exporting the pretrained models ... ")
        url = "https://drive.google.com/uc?id=1P8t7wfjxgLSSdVA9fZ5UYHq9iQ6bkz9G"
        gdown.cached_download(
            url, "deep-learning-models.zip", quiet=False, postprocess=gdown.extractall
        )

        print("load meter classification model ...")
        self.METERS_MODEL = create_transformer_model()
        self.METERS_MODEL.load_weights(
            f"{abs_path}/deep-learning-models/meters_model/cp.ckpt"
        )

        print("load embedding model ...")
        self.BASE_MODEL = create_model_v1()
        self.BASE_MODEL.load_weights(
            f"{abs_path}/deep-learning-models/embeddings_extractor_model/cp.ckpt"
        )
        self.FEATURES_EXTRACTOR = Model(
            self.BASE_MODEL.layers[0].input, self.BASE_MODEL.layers[4].output
        )
        self.BAITS_EMBEDDINGS = load_from_disk(
            f"{abs_path}/deep-learning-models/baits_embeddings"
        )

        print("load era classification model ...")
        self.ERA_MODEL = create_era_theme_model()
        self.ERA_MODEL.load_weights(
            f"{abs_path}/deep-learning-models/era_classification_models_shorter_context/cp.ckpt"
        )

        self.ERA_TOKENIZER = tk.SentencePieceTokenizer()
        self.ERA_TOKENIZER.load_model(
            f"{abs_path}/deep-learning-models/era_classification_models_shorter_context/vocab.model"
        )

        print("load theme classification model ...")
        self.THEME_MODEL = create_era_theme_model()
        self.THEME_MODEL.load_weights(
            f"{abs_path}/deep-learning-models/theme_classification_model/cp.ckpt"
        )

        self.THEME_TOKENIZER = tk.SentencePieceTokenizer()
        self.THEME_TOKENIZER.load_model(
            f"{abs_path}/deep-learning-models/theme_classification_model/vocab.model"
        )

    def extract_features(self, x):
        x = [[char2idx[char] for char in self.preprocess(line)] for line in x]
        x = pad_sequences(x, padding="post", value=0, maxlen=128)
        feature_extractor = self.FEATURES_EXTRACTOR
        out = feature_extractor.predict(x)
        return out

    def get_closest_baits(self, baits, k=1):
        closest_baits = list()
        for bait in baits:
            sample_embedding = self.extract_features([bait])
            sample_similarity = self.BAITS_EMBEDDINGS.map(
                lambda examples: {
                    "similarity": util.cos_sim(
                        examples["embedding"], sample_embedding
                    ).numpy()
                },
                batched=True,
            )
            zipped = zip(sample_similarity["text"], sample_similarity["similarity"])
            closest_baits.append(sorted(zipped, key=lambda x: x[1])[::-1][:k])
        return closest_baits

    def preprocess(self, text):
        out = ""
        for l in text:
            if l in vocab:
                out += l
        return out

    def get_meter(self, baits):
        meters_model = self.METERS_MODEL
        processed_baits = [
            [char2idx[char] for char in self.preprocess(bait)] for bait in baits
        ]
        processed_baits = pad_sequences(
            processed_baits, padding="post", value=0, maxlen=128,
        )
        labels = meters_model.predict(processed_baits).argmax(-1)
        return [label2name[label] for label in labels]

    def predict_era(self, poem, max_tokens=128):
        labels2era = [
            ["العصر الجاهلي", "العصر الإسلامي", "العصر الأموي", "قبل الإسلام"],
            ["العصر العباسي"],
            ["العصر الفاطمي", "العصر الأيوبي", "العصر المملوكي"],
            ["العصر الحديث", "العصر العثماني"],
        ]
        tokenizer = self.ERA_TOKENIZER
        model = self.ERA_MODEL
        tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
        return labels2era[model.predict(tokenized).argmax(-1)[0]]

    def predict_theme(self, poem, max_tokens=128):
        labels2theme = [
            ["قصيدة حزينه", "قصيدة رثاء", "قصيدة عتاب", "قصيدة فراق"],
            ["قصيدة ذم", "قصيدة هجاء"],
            ["قصيدة مدح"],
            ["قصيدة رومنسيه", "قصيدة شوق", "قصيدة غزل"],
        ]
        tokenizer = self.THEME_TOKENIZER
        model = self.THEME_MODEL
        tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
        return labels2theme[model.predict(tokenized).argmax(-1)[0]]

    def similarity_score(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def check_similarity(self, tf3, bahr):
        out = []

        if bahr != "نثر":
            meter = BOHOUR_NAMES[BOHOUR_NAMES_AR.index(bahr)]
            for comb, tafeelat in zip(
                self.BOHOUR_PATTERNS[meter], self.BOHOUR_TAFEELAT[meter],
            ):
                prob = self.similarity_score(tf3, comb)
                out.append((comb, prob, tafeelat))
            return sorted(out, key=lambda x: x[1], reverse=True)
        else:
            # return empty results
            return [("", 0.0, "")]

    def majority_vote(self, a):
        return Counter(a).most_common()[0][0]

    def analyze(
        self,
        baits=None,
        short_qafiyah=False,
        override_tashkeel=False,
        highlight_output=False,
    ):
        proc_baits = []
        diacritized_baits = []
        shatrs_arudi_styles_and_patterns = []
        patterns_mismatches = []
        closest_baits = []
        closest_patterns_from_shatrs =[]
        shatrs = []
        
        

        for bait in baits:
            proc_shatrs = []
            for shatr in bait.split("#"):
                proc_shatr = self.text_encoder.clean(shatr).strip()
                if len(proc_shatr) == 0:
                    continue
                shatrs.append(proc_shatr)

            proc_bait = " # ".join(proc_shatrs)
            proc_baits.append(proc_bait)

        meter = self.majority_vote(self.get_meter(proc_baits))
        qafiyah = self.majority_vote(get_qafiyah(proc_baits, short=short_qafiyah))
        era = self.predict_era(strip_tashkeel(" ".join(proc_baits)))
        theme = self.predict_theme(strip_tashkeel(" ".join(proc_baits)))

        for shatr in shatrs:
            diacritized_shatr = self.diac_model.infer(proc_shatr)

            if override_tashkeel:
                try:
                    overridden_diacritized_shatr = override_auto_tashkeel(
                        diacritized_shatr, proc_shatr,
                    )
                    diacritized_shatr = overridden_diacritized_shatr
                except:
                    print(
                        "Error in override_auto_baits_tashkeel, rolling back to auto diacritization"
                    )
            
            shatr_arudi_style, shatr_pattern = get_arudi_style(shatr)
            closest_pattern, _, _ = self.check_similarity(tf3=shatr_pattern, bahr=meter,)[0]

            pattern_mismatch = find_mismatch(closest_pattern, shatr_pattern, highlight_output=highlight_output,)
            
            shatrs_arudi_styles_and_patterns.append((shatr_arudi_style, shatr_pattern ))
            patterns_mismatches.append(pattern_mismatch)

        analysis = {
            "diacritized": diacritized_baits,
            "arudi_style": shatrs_arudi_styles_and_patterns,
            "patterns_mismatches": patterns_mismatches,
            "qafiyah": qafiyah,
            "meter": meter,
            "closest_baits": closest_baits,
            "era": era,
            "closest_patterns": closest_patterns_from_shatrs,
            "theme": theme,
        }
        return analysis
