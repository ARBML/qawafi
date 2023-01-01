import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras import layers
from numpy import dot
from numpy.linalg import norm
from sentence_transformers import util

import tensorflow as tf
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
from .utils import label2name, char2idx


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
