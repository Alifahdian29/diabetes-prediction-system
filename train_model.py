"""
train_model.py
Melatih model Random Forest untuk klasifikasi risiko diabetes
menggunakan Dataset of Diabetes (Mendeley).

Kolom dataset:
ID, No_Pation, Gender, AGE, Urea, Cr, HbA1c, Chol, TG, HDL, LDL, VLDL, BMI, CLASS
CLASS: N (Normal), P (Prediabetes), Y (Diabetes)
"""

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix
)

DATA_PATH = "data/diabetes.csv"
MODEL_PATH = "model/random_forest_model.pkl"
SCALER_PATH = "model/scaler.pkl"
ENCODER_PATH = "model/label_encoder.pkl"

FEATURES = ["Gender", "AGE", "Urea", "Cr", "HbA1c",
            "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"]
TARGET = "CLASS"


def load_and_clean_data(path):
    df = pd.read_csv(path)
    # Bersihkan nama kolom dari spasi berlebih
    df.columns = [c.strip() for c in df.columns]

    # Bersihkan & normalisasi label CLASS (ada variasi spasi/huruf kecil di data mentah)
    df["CLASS"] = df["CLASS"].astype(str).str.strip().str.upper()
    df["CLASS"] = df["CLASS"].replace({"Y ": "Y", "N ": "N", "P ": "P"})

    # Normalisasi Gender (ada 'f' huruf kecil di data)
    df["Gender"] = df["Gender"].astype(str).str.strip().str.upper()

    # Hanya pakai 3 kelas valid
    df = df[df["CLASS"].isin(["N", "P", "Y"])]

    # Drop baris dengan data kosong pada kolom penting
    df = df.dropna(subset=FEATURES + [TARGET])

    return df


def main():
    df = load_and_clean_data(DATA_PATH)
    print(f"Jumlah data setelah cleaning: {len(df)}")
    print(df["CLASS"].value_counts())

    # Encode Gender: M=1, F=0
    df["Gender"] = df["Gender"].map({"M": 1, "F": 0})
    df = df.dropna(subset=["Gender"])

    X = df[FEATURES]
    y = df[TARGET]

    # Encode target label
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)  # N, P, Y -> 0,1,2 (urut alfabet)
    print("Label mapping:", dict(zip(le.classes_, le.transform(le.classes_))))

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Scaling fitur numerik (membantu GaussianNB dengan skala berbeda)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Training model Random Forest
    model = RandomForestClassifier(
        n_estimators=150,
        criterion="gini",
        max_depth=8,
        random_state=42,
    )
    model.fit(X_train_scaled, y_train)

    # Evaluasi
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nAkurasi model: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Simpan model, scaler, dan label encoder
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(le, ENCODER_PATH)
    print(f"\nModel disimpan di: {MODEL_PATH}")
    print(f"Scaler disimpan di: {SCALER_PATH}")
    print(f"Label encoder disimpan di: {ENCODER_PATH}")


if __name__ == "__main__":
    main()
