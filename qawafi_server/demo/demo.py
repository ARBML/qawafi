import glob
from utils import BOHOUR_NAMES
from models import create_transformer_model, create_model_v1, create_era_theme_model
from tensorflow.keras.models import Model
from datasets import load_from_disk
import tkseem as tk

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