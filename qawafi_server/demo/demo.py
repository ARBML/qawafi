import glob
from utils import BOHOUR_NAMES
from models import create_transformer_model, create_model_v1, create_era_theme_model
from tensorflow.keras.models import Model
from datasets import load_from_disk
from utils import label2name, char2idx, vocab, BOHOUR_NAMES_AR
import tkseem as tk
from keras.preprocessing.sequence import pad_sequences
from sentence_transformers import util
from bohour.arudi_style import get_arudi_style
from bohour.qafiah import get_qafiah_type, get_qafiyah
from collections import Counter
from difflib import SequenceMatcher

BOHOUR_PATTERNS = {}
for bahr_file in glob.glob("../bohour_patterns/ints/*.txt"):
    patterns = open(bahr_file, "r").read().splitlines()
    bahr_name = bahr_file.split("/")[-1].split(".")[0]
    if bahr_name not in BOHOUR_NAMES:
        # print(bahr_name)
        continue
    BOHOUR_PATTERNS[bahr_name] = patterns

BOHOUR_TAFEELAT = {}
for bahr_file in glob.glob("../bohour_patterns/strs/*.txt"):
    patterns = open(bahr_file, "r").read().splitlines()
    bahr_name = bahr_file.split("/")[-1].split(".")[0]
    if bahr_name not in BOHOUR_NAMES:
        # print(bahr_name)
        continue
    BOHOUR_TAFEELAT[bahr_name] = patterns

# get the model
print("trying loading the meters model")


def extract_features(x):
    x = [[char2idx[char] for char in preprocess(line)] for line in x]
    x = pad_sequences(x, padding="post", value=0, maxlen=128)
    feature_extractor = FEATURES_EXTRACTOR
    out = feature_extractor.predict(x)
    return out


def get_closest_baits(baits, k=1):
    # sample_embedding = extract_features(baits)
    closest_baits = list()
    for bait in baits:
        sample_embedding = extract_features([bait])
        sample_similarity = BAITS_EMBEDDINGS.map(
            lambda examples: {
                "similarity": util.cos_sim(
                    examples["embedding"], sample_embedding
                ).numpy()
            },
            batched=True,
        )
        zipped = zip(baits, sample_similarity["similarity"])
        closest_baits.append(sorted(zipped, key=lambda x: x[1])[::-1][:k])
    return closest_baits


def preprocess(text):
    out = ""
    for l in text:
        if l in vocab:
            out += l
    return out


def get_meter(baits):
    meters_model = METERS_MODEL
    processed_baits = [[char2idx[char] for char in preprocess(bait)] for bait in baits]
    processed_baits = pad_sequences(
        processed_baits,
        padding="post",
        value=0,
        maxlen=128,
    )
    labels = meters_model.predict(processed_baits).argmax(-1)
    return [label2name[label] for label in labels]


def predict_era(poem, max_tokens=128):
    labels2era = [
        ["العصر الجاهلي", "العصر الإسلامي", "العصر الأموي", "قبل الإسلام"],
        ["العصر العباسي"],
        ["العصر الفاطمي", "العصر الأيوبي", "العصر المملوكي"],
        ["العصر الحديث", "العصر العثماني"],
    ]
    tokenizer = ERA_TOKENIZER
    model = ERA_MODEL
    tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
    return labels2era[model.predict(tokenized).argmax(-1)[0]]


def predict_theme(poem, max_tokens=128):
    labels2theme = [
        ["قصيدة حزينه", "قصيدة رثاء", "قصيدة عتاب", "قصيدة فراق"],
        ["قصيدة ذم", "قصيدة هجاء"],
        ["قصيدة مدح"],
        ["قصيدة رومنسيه", "قصيدة شوق", "قصيدة غزل"],
    ]
    tokenizer = THEME_TOKENIZER
    model = THEME_MODEL
    tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
    return labels2theme[model.predict(tokenized).argmax(-1)[0]]

def similarity_score(a, b):
        return SequenceMatcher(None, a, b).ratio()

def check_similarity(tf3, bahr):
    out = []
    meter = BOHOUR_NAMES[BOHOUR_NAMES_AR.index(bahr)]
    for comb, tafeelat in zip(
        BOHOUR_PATTERNS[meter],
        BOHOUR_TAFEELAT[meter],
    ):
        prob = similarity_score(tf3, comb)
        out.append((comb, prob, tafeelat))
    return sorted(out, key=lambda x: x[1], reverse=True)

def get_closest_patterns(patterns, meter):
    most_similar_patterns = list()
    for pattern in patterns:
        most_similar_patterns.append(
            check_similarity(
                tf3=pattern,
                bahr=meter,
            )[0]
        )
    return most_similar_patterns

majority_vote = lambda a: Counter(a).most_common()[0][0]
        


METERS_MODEL = create_transformer_model()
METERS_MODEL.load_weights("../deep-learning-models/meters_model/cp.ckpt")

# get the embeddings model
BASE_MODEL = create_model_v1()
BASE_MODEL.load_weights("../deep-learning-models/embeddings_extractor_model/cp.ckpt")


FEATURES_EXTRACTOR = Model(BASE_MODEL.layers[0].input, BASE_MODEL.layers[4].output)


BAITS_EMBEDDINGS = load_from_disk("../deep-learning-models/baits_embeddings")


ERA_MODEL = create_era_theme_model()
ERA_MODEL.load_weights("../deep-learning-models/era_classification_model/cp.ckpt")

ERA_TOKENIZER = tk.SentencePieceTokenizer()
ERA_TOKENIZER.load_model("../deep-learning-models/era_classification_model/vocab.model")


THEME_MODEL = create_era_theme_model()
THEME_MODEL.load_weights("../deep-learning-models/theme_classification_model/cp.ckpt")

THEME_TOKENIZER = tk.SentencePieceTokenizer()
THEME_TOKENIZER.load_model("../deep-learning-models/theme_classification_model/vocab.model")

baits = ['ألا ليت شعري هل أبيتن ليلة # بجنب الغضا أزجي القلاص النواجيا']
baits = [baits[0]]
diacritized_baits = open('/content/qawafi/shakkelha_server/baits_output.txt', 'r').read().splitlines()
arudi_styles_and_patterns = get_arudi_style(diacritized_baits)
meter = majority_vote(get_meter(baits))
most_closest_patterns = get_closest_patterns(
    patterns=[pattern for (arudiy_style, pattern) in arudi_styles_and_patterns],
    meter=meter,
)
qafiyah = majority_vote(get_qafiyah(baits))
closest_baits = get_closest_baits(baits)
era = predict_era(" ".join(baits))
theme = predict_theme(" ".join(baits))
print( 
    {
        "diacritized": diacritized_baits,
        "arudi_style": arudi_styles_and_patterns,
        "qafiyah": qafiyah,
        "meter": meter,
        "closest_baits": closest_baits,
        "era": era,
        "closest_patterns": most_closest_patterns,
        "theme": theme,
    })

