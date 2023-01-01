# load the meters model
import glob
import os
import time

import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras import layers
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import util

import tensorflow as tf
from django.conf import settings
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tensorflow.keras.layers import (
    GRU,
    BatchNormalization,
    Bidirectional,
    Dense,
    Dropout,
    Embedding,
    Input,
)
from tensorflow.keras.models import Sequential

# cos_sim = lambda a, b: dot(a, b) / (norm(a) * norm(b))

vocab = list("إةابتثجحخدذرزسشصضطظعغفقكلمنهويىأءئؤ#آ ")
vocab += list("ًٌٍَُِّ") + ["ْ"] + ["ٓ"]

char2idx = {u: i + 1 for i, u in enumerate(vocab)}

label2name = settings.BOHOUR_NAMES_AR


def create_model_v1():
    model = Sequential()
    model.add(Input((128,)))
    model.add(Embedding(len(char2idx) + 1, 32))
    model.add(Bidirectional(GRU(units=64, return_sequences=True)))
    model.add(Bidirectional(GRU(units=64, return_sequences=True)))
    model.add(Bidirectional(GRU(units=64, return_sequences=True)))
    model.add(Bidirectional(GRU(units=64)))
    model.add(Dense(len(label2name), activation="softmax"))
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        # self.ffn = keras.Sequential(
        #     [layers.Dense(ff_dim, activation="relu"), layers.Dense(embed_dim),]
        # )
        self.ffn = tf.keras.Sequential(
            [
                layers.Bidirectional(GRU(units=ff_dim, return_sequences=True)),
                layers.Bidirectional(GRU(units=ff_dim, return_sequences=True)),
                layers.Bidirectional(GRU(units=ff_dim, return_sequences=True)),
                layers.Dense(embed_dim),
            ]
        )
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(rate)
        self.dropout2 = layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        # print(out1.shape)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim):
        super(TokenAndPositionEmbedding, self).__init__()
        self.token_emb = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim)
        self.pos_emb = layers.Embedding(input_dim=maxlen, output_dim=embed_dim)

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        # return x + positions
        return x


def create_transformer_model():
    embed_dim = 64  # Embedding size for each token
    num_heads = 3  # Number of attention heads
    ff_dim = 64  # Hidden layer size in feed forward network inside transformer
    maxlen = 128
    vocab_size = len(char2idx) + 1
    inputs = layers.Input(shape=(maxlen,))
    embedding_layer = TokenAndPositionEmbedding(maxlen, vocab_size, embed_dim)
    x = embedding_layer(inputs)
    transformer_block = TransformerBlock(embed_dim, num_heads, ff_dim)
    x = transformer_block(x)
    x = layers.Flatten()(x)
    # x = layers.Dropout(0.1)(x)
    x = layers.Dense(128, activation="relu")(x)
    # x = layers.Dropout(0.1)(x)
    outputs = layers.Dense(len(label2name), activation="softmax")(x)

    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    model.compile(
        optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
    )
    return model


def extract_features(x):
    x = [[char2idx[char] for char in preprocess(line)] for line in x]
    x = pad_sequences(x, padding="post", value=0, maxlen=128)
    feature_extractor = settings.FEATURES_EXTRACTOR
    out = feature_extractor.predict(x)
    return out


def get_closest_baits(baits, k=1):
    # sample_embedding = extract_features(baits)
    closest_baits = list()
    for bait in baits:
        sample_embedding = extract_features([bait])
        sample_similarity = settings.BAITS_EMBEDDINGS.map(
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


def preprocess(text):
    out = ""
    for l in text:
        if l in vocab:
            out += l
    return out


def get_meter(baits):
    meters_model = settings.METERS_MODEL
    processed_baits = [[char2idx[char] for char in preprocess(bait)] for bait in baits]
    processed_baits = pad_sequences(
        processed_baits,
        padding="post",
        value=0,
        maxlen=128,
    )
    labels = meters_model.predict(processed_baits).argmax(-1)
    return [label2name[label] for label in labels]


def create_era_theme_model():
    model = Sequential()
    model.add(Input((128,)))
    model.add(Embedding(10_000, 128))
    model.add(Bidirectional(GRU(units=64, return_sequences=True, dropout=0.3)))
    model.add(Bidirectional(GRU(units=64, return_sequences=True, dropout=0.3)))
    model.add(Bidirectional(GRU(units=64, dropout=0.3)))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(4, activation="softmax"))
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def predict_era(poem, max_tokens=128):
    labels2era = [
        ["العصر الجاهلي", "العصر الإسلامي", "العصر الأموي", "قبل الإسلام"],
        ["العصر العباسي"],
        ["العصر الفاطمي", "العصر الأيوبي", "العصر المملوكي"],
        ["العصر الحديث", "العصر العثماني"],
    ]
    tokenizer = settings.ERA_TOKENIZER
    model = settings.ERA_MODEL
    tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
    return labels2era[model.predict(tokenized).argmax(-1)[0]]


def predict_theme(poem, max_tokens=128):
    labels2theme = [
        ["قصيدة حزينه", "قصيدة رثاء", "قصيدة عتاب", "قصيدة فراق"],
        ["قصيدة ذم", "قصيدة هجاء"],
        ["قصيدة مدح"],
        ["قصيدة رومنسيه", "قصيدة شوق", "قصيدة غزل"],
    ]
    tokenizer = settings.THEME_TOKENIZER
    model = settings.THEME_MODEL
    tokenized = tokenizer.encode_sentences([poem], out_length=max_tokens)
    return labels2theme[model.predict(tokenized).argmax(-1)[0]]
