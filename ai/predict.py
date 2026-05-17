import os
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Đường dẫn tuyệt đối — tránh lỗi "file not found" khi chạy từ thư mục khác
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load_model(os.path.join(BASE_DIR, "sentiment_model.h5"))

with open(os.path.join(BASE_DIR, "tokenizer.pkl"), "rb") as f:
    tokenizer = pickle.load(f)

max_len = 200

def predict_sentiment(text):
    seq     = tokenizer.texts_to_sequences([text])
    padded  = pad_sequences(seq, maxlen=max_len)
    prediction = model.predict(padded)[0][0]
    score   = round(float(prediction) * 10, 1)
    sentiment = "Positive" if prediction >= 0.5 else "Negative"
    return sentiment, score