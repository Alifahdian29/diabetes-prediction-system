"""
recommendation.py
Modul rule-based untuk menghasilkan rekomendasi kesehatan personal
berdasarkan hasil prediksi kelas (N/P/Y) dan nilai-nilai klinis pasien.

Catatan: Ambang batas (threshold) berikut mengacu pada rentang umum yang
dipakai pada dataset ini (bukan pengganti diagnosis medis profesional).
"""

CLASS_INFO = {
    "N": {
        "label": "Normal (Tidak Diabetes)",
        "summary": "Berdasarkan data yang dimasukkan, sistem tidak mendeteksi "
                    "indikasi diabetes yang signifikan.",
        "color": "#2f8f5b",
    },
    "P": {
        "label": "Prediabetes",
        "summary": "Sistem mendeteksi indikasi awal (prediabetes). Ini adalah "
                    "sinyal untuk mulai mengubah gaya hidup sebelum kondisi "
                    "berkembang menjadi diabetes.",
        "color": "#c98a1d",
    },
    "Y": {
        "label": "Diabetes",
        "summary": "Sistem mendeteksi indikasi kuat diabetes berdasarkan "
                    "nilai klinis yang dimasukkan. Disarankan konsultasi "
                    "lebih lanjut dengan tenaga medis.",
        "color": "#c0392b",
    },
}


def generate_recommendations(predicted_class: str, data: dict) -> list:
    """
    Menghasilkan daftar rekomendasi personal (diet & gaya hidup)
    berdasarkan kelas prediksi + nilai-nilai klinis individu.
    """
    recs = []

    hba1c = data.get("HbA1c", 0)
    bmi = data.get("BMI", 0)
    chol = data.get("Chol", 0)
    tg = data.get("TG", 0)
    hdl = data.get("HDL", 0)
    ldl = data.get("LDL", 0)
    age = data.get("AGE", 0)

    # --- Rekomendasi berbasis kelas prediksi ---
    if predicted_class == "N":
        recs.append(
            "Pertahankan pola makan seimbang dan rutin berolahraga "
            "minimal 150 menit per minggu untuk menjaga kondisi tetap normal."
        )
        recs.append(
            "Lakukan general check-up gula darah setidaknya 1x per tahun "
            "sebagai langkah pencegahan dini."
        )
    elif predicted_class == "P":
        recs.append(
            "Mulai kurangi konsumsi karbohidrat sederhana dan gula tambahan "
            "(minuman manis, makanan olahan) untuk mencegah progresi ke diabetes."
        )
        recs.append(
            "Tingkatkan aktivitas fisik aerobik (jalan cepat, bersepeda, berenang) "
            "3-5 kali per minggu, minimal 30 menit per sesi."
        )
        recs.append(
            "Disarankan cek HbA1c ulang dalam 3-6 bulan untuk memantau perkembangan."
        )
    elif predicted_class == "Y":
        recs.append(
            "Segera konsultasikan hasil ini dengan dokter/ahli endokrin untuk "
            "rencana penanganan medis yang tepat."
        )
        recs.append(
            "Terapkan pola makan rendah indeks glikemik: perbanyak serat "
            "(sayur, kacang-kacangan) dan batasi nasi putih/gula/tepung olahan."
        )
        recs.append(
            "Pantau gula darah secara rutin sesuai anjuran dokter, termasuk "
            "kepatuhan terhadap obat/insulin jika diresepkan."
        )

    # --- Rekomendasi berbasis nilai klinis spesifik ---
    if hba1c >= 6.5:
        recs.append(
            f"Nilai HbA1c Anda ({hba1c}%) tergolong tinggi (>=6.5%). "
            "Fokus pada pengendalian gula darah jangka panjang."
        )
    elif hba1c >= 5.7:
        recs.append(
            f"Nilai HbA1c Anda ({hba1c}%) berada di zona waspada (5.7-6.4%)."
        )

    if bmi >= 30:
        recs.append(
            f"BMI Anda ({bmi}) tergolong obesitas. Program penurunan berat "
            "badan bertahap (0.5-1 kg/minggu) sangat dianjurkan."
        )
    elif bmi >= 25:
        recs.append(
            f"BMI Anda ({bmi}) tergolong overweight. Pertimbangkan defisit "
            "kalori ringan dan peningkatan aktivitas fisik."
        )
    elif bmi < 18.5:
        recs.append(
            f"BMI Anda ({bmi}) tergolong underweight. Konsultasikan asupan "
            "nutrisi dengan ahli gizi."
        )

    if chol >= 6.2:
        recs.append(
            f"Kolesterol total Anda ({chol}) tinggi. Kurangi lemak jenuh "
            "dan perbanyak konsumsi omega-3 (ikan, kacang-kacangan)."
        )

    if tg >= 2.3:
        recs.append(
            f"Trigliserida Anda ({tg}) tinggi. Batasi gula, alkohol, dan "
            "karbohidrat olahan."
        )

    if hdl < 1.0:
        recs.append(
            f"HDL (kolesterol baik) Anda ({hdl}) rendah. Olahraga aerobik "
            "rutin dapat membantu meningkatkan HDL."
        )

    if ldl >= 4.1:
        recs.append(
            f"LDL (kolesterol jahat) Anda ({ldl}) tinggi. Pertimbangkan "
            "pengurangan lemak trans dan konsultasi dengan dokter."
        )

    if age >= 45 and predicted_class != "N":
        recs.append(
            "Usia di atas 45 tahun meningkatkan risiko komplikasi. "
            "Pemeriksaan kesehatan berkala sangat dianjurkan."
        )

    return recs
