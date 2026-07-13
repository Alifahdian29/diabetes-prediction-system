"""
app.py
Sistem Cerdas Prediksi & Rekomendasi Risiko Diabetes
Model: Random Forest | Dataset: Mendeley - Dataset of Diabetes

Cara menjalankan (localhost):
    pip install -r requirements.txt
    python app.py
Lalu buka browser: http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np
import pandas as pd

from recommendation import generate_recommendations, CLASS_INFO
from database import init_db, save_prediction, get_all_history, clear_history

app = Flask(__name__)

# Load model & preprocessing objects sekali saat startup
model = joblib.load("model/random_forest_model.pkl")
scaler = joblib.load("model/scaler.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Inisialisasi database riwayat prediksi (SQLite)
init_db()

FEATURES = ["Gender", "AGE", "Urea", "Cr", "HbA1c",
            "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        form = request.form
        gender_raw = form.get("Gender", "M")
        gender_val = 1 if gender_raw.upper() == "M" else 0

        input_data = {
            "Gender": gender_val,
            "AGE": float(form.get("AGE")),
            "Urea": float(form.get("Urea")),
            "Cr": float(form.get("Cr")),
            "HbA1c": float(form.get("HbA1c")),
            "Chol": float(form.get("Chol")),
            "TG": float(form.get("TG")),
            "HDL": float(form.get("HDL")),
            "LDL": float(form.get("LDL")),
            "VLDL": float(form.get("VLDL")),
            "BMI": float(form.get("BMI")),
        }

        X = pd.DataFrame([input_data])[FEATURES]
        X_scaled = scaler.transform(X)

        pred_encoded = model.predict(X_scaled)[0]
        pred_proba = model.predict_proba(X_scaled)[0]
        pred_class = label_encoder.inverse_transform([pred_encoded])[0]

        proba_dict = {
            cls: round(float(p) * 100, 2)
            for cls, p in zip(label_encoder.classes_, pred_proba)
        }

        recs = generate_recommendations(pred_class, input_data)
        info = CLASS_INFO[pred_class]

        # Simpan hasil prediksi ke database riwayat (SQLite)
        save_prediction(gender_raw, input_data, pred_class, proba_dict)

        return render_template(
            "result.html",
            input_data=input_data,
            gender_display=gender_raw,
            pred_class=pred_class,
            info=info,
            proba_dict=proba_dict,
            recommendations=recs,
        )
    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/history", methods=["GET"])
def history():
    records = get_all_history()
    return render_template("history.html", records=records)


@app.route("/history/clear", methods=["POST"])
def history_clear():
    clear_history()
    return redirect(url_for("history"))


if __name__ == "__main__":
    # use_reloader=False supaya tidak restart terus-menerus akibat salah
    # mendeteksi perubahan pada file di luar folder project (umum terjadi
    # di Windows karena antivirus/OneDrive/indexing menyentuh timestamp file).
    app.run(debug=True, host="127.0.0.1", port=5000, use_reloader=False)
