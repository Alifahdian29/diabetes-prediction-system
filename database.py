"""
database.py
Modul untuk menyimpan dan mengambil riwayat prediksi menggunakan SQLite.
SQLite dipilih karena sudah built-in di Python (tidak perlu install
MySQL/XAMPP terpisah), datanya tersimpan dalam satu file: data/history.db
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "history.db")


def init_db():
    """Membuat tabel riwayat jika belum ada. Dipanggil sekali saat app start."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT NOT NULL,
            gender TEXT,
            age REAL,
            urea REAL,
            cr REAL,
            hba1c REAL,
            chol REAL,
            tg REAL,
            hdl REAL,
            ldl REAL,
            vldl REAL,
            bmi REAL,
            predicted_class TEXT,
            prob_n REAL,
            prob_p REAL,
            prob_y REAL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(gender_display, input_data, pred_class, proba_dict):
    """Menyimpan satu record hasil prediksi ke database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prediction_history
        (waktu, gender, age, urea, cr, hba1c, chol, tg, hdl, ldl, vldl, bmi,
         predicted_class, prob_n, prob_p, prob_y)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        gender_display,
        input_data["AGE"],
        input_data["Urea"],
        input_data["Cr"],
        input_data["HbA1c"],
        input_data["Chol"],
        input_data["TG"],
        input_data["HDL"],
        input_data["LDL"],
        input_data["VLDL"],
        input_data["BMI"],
        pred_class,
        proba_dict.get("N", 0),
        proba_dict.get("P", 0),
        proba_dict.get("Y", 0),
    ))
    conn.commit()
    conn.close()


def get_all_history(limit=100):
    """Mengambil semua riwayat prediksi, terbaru di atas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM prediction_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def clear_history():
    """Menghapus semua riwayat (dipakai tombol reset di halaman history)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prediction_history")
    conn.commit()
    conn.close()
