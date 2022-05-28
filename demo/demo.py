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
import pprint

class BaitAnalysis:
  def __init__(self):
    self.BOHOUR_PATTERNS = {}
    abs_path = "/content/qawafi/qawafi_server"
    for bahr_file in glob.glob(f"{abs_path}/bohour_patterns/ints/*.txt"):
        patterns = open(bahr_file, "r").read().splitlines()
        bahr_name = bahr_file.split("/")[-1].split(".")[0]
        if bahr_name not in BOHOUR_NAMES:
            # print(bahr_name)
            continue
        self.BOHOUR_PATTERNS[bahr_name] = patterns

    self.BOHOUR_TAFEELAT = {}
    for bahr_file in glob.glob(f"{abs_path}/bohour_patterns/strs/*.txt"):
        patterns = open(bahr_file, "r").read().splitlines()
        bahr_name = bahr_file.split("/")[-1].split(".")[0]
        if bahr_name not in BOHOUR_NAMES:
            # print(bahr_name)
            continue
        self.BOHOUR_TAFEELAT[bahr_name] = patterns

    print("load meter classification model ...")
    self.METERS_MODEL = create_transformer_model()
    self.METERS_MODEL.load_weights(f"{abs_path}/deep-learning-models/meters_model/cp.ckpt")

    print("load embedding model ...")
    self.BASE_MODEL = create_model_v1()
    self.BASE_MODEL.load_weights(f"{abs_path}/deep-learning-models/embeddings_extractor_model/cp.ckpt")
    self.FEATURES_EXTRACTOR = Model(self.BASE_MODEL.layers[0].input, self.BASE_MODEL.layers[4].output)
    self.BAITS_EMBEDDINGS = load_from_disk(f"{abs_path}/deep-learning-models/baits_embeddings")

    print("load era classification model ...")
    self.ERA_MODEL = create_era_theme_model()
    self.ERA_MODEL.load_weights(f"{abs_path}/deep-learning-models/era_classification_model/cp.ckpt")

    self.ERA_TOKENIZER = tk.SentencePieceTokenizer()
    self.ERA_TOKENIZER.load_model(f"{abs_path}/deep-learning-models/era_classification_model/vocab.model")

    print("load theme classification model ...")
    self.THEME_MODEL = create_era_theme_model()
    self.THEME_MODEL.load_weights(f"{abs_path}/deep-learning-models/theme_classification_model/cp.ckpt")

    self.THEME_TOKENIZER = tk.SentencePieceTokenizer()
    self.THEME_TOKENIZER.load_model(f"{abs_path}/deep-learning-models/theme_classification_model/vocab.model")

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
      processed_baits = [[char2idx[char] for char in self.preprocess(bait)] for bait in baits]
      processed_baits = pad_sequences(
          processed_baits,
          padding="post",
          value=0,
          maxlen=128,
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
      meter = BOHOUR_NAMES[BOHOUR_NAMES_AR.index(bahr)]
      for comb, tafeelat in zip(
          self.BOHOUR_PATTERNS[meter],
          self.BOHOUR_TAFEELAT[meter],
      ):
          prob = self.similarity_score(tf3, comb)
          out.append((comb, prob, tafeelat))
      return sorted(out, key=lambda x: x[1], reverse=True)

  def get_closest_patterns(self, patterns, meter):
      most_similar_patterns = list()
      for pattern in patterns:
          most_similar_patterns.append(
              self.check_similarity(
                  tf3=pattern,
                  bahr=meter,
              )[0]
          )
      return most_similar_patterns

  def majority_vote(self, a):
    return Counter(a).most_common()[0][0]

  def analyze(self):
    baits = open('/content/qawafi/demo/baits_input.txt', 'r').read().splitlines()
    diacritized_baits = open('/content/qawafi/demo/baits_output.txt', 'r').read().splitlines()
    arudi_styles_and_patterns = get_arudi_style(diacritized_baits)
    meter = self.majority_vote(self.get_meter(baits))
    most_closest_patterns = self.get_closest_patterns(
        patterns=[pattern for (arudiy_style, pattern) in arudi_styles_and_patterns],
        meter=meter,
    )
    qafiyah = self.majority_vote(get_qafiyah(baits))
    closest_baits = self.get_closest_baits(baits)
    era = self.predict_era(" ".join(baits))
    theme = self.predict_theme(" ".join(baits))
    pprint.pprint( 
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

        


