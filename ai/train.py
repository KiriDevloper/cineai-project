import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import pickle
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# =========================
# LOAD DATASET
# =========================

data = pd.read_csv("dataset/IMDB Dataset.csv")

texts = data["review"].tolist()

labels = [
    1 if x == "positive" else 0
    for x in data["sentiment"]
]

# =========================
# TOKENIZER
# =========================

tokenizer = Tokenizer(num_words=10000)

tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)

max_len = 200

X = pad_sequences(sequences, maxlen=max_len)

y = np.array(labels)

# =========================
# SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =========================
# MODEL
# =========================

model = Sequential()

model.add(Embedding(10000, 128, input_length=max_len))

model.add(LSTM(64))

model.add(Dense(32, activation='relu'))

model.add(Dense(1, activation='sigmoid'))

# =========================
# COMPILE
# =========================

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# =========================
# TRAIN
# =========================

model.fit(
    X_train,
    y_train,
    epochs=3,
    batch_size=64,
    validation_data=(X_test, y_test)
)

# =========================
# SAVE MODEL
# =========================

os.makedirs("model", exist_ok=True)

model.save("model/sentiment_model.h5")

with open("model/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Train xong!")