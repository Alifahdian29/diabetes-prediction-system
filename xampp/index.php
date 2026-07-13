<?php
/**
 * index.php
 * File ini ditaruh di folder htdocs XAMPP (misal: htdocs/diabetes-system/index.php)
 *
 * SYARAT: Aplikasi Flask (python app.py) harus tetap dijalankan terpisah
 * di terminal/VS Code, karena PHP tidak menjalankan Python. File ini
 * hanya menampilkan (embed) sistem Flask yang sudah berjalan di
 * http://127.0.0.1:5000, supaya bisa diakses lewat Apache XAMPP juga.
 *
 * Cara pakai:
 * 1. Jalankan XAMPP, aktifkan Apache
 * 2. Jalankan "python app.py" di terminal terpisah (biarkan tetap jalan)
 * 3. Copy file ini ke: C:\xampp\htdocs\diabetes-system\index.php
 * 4. Buka browser ke: http://localhost/diabetes-system/
 */

$flask_url = "http://127.0.0.1:5000/";

// Cek apakah server Flask sedang aktif
$flask_aktif = @get_headers($flask_url);
$status = ($flask_aktif && strpos($flask_aktif[0], '200')) ? true : false;
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Sistem Prediksi & Rekomendasi Diabetes</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; }
        iframe {
            width: 100%;
            height: 100vh;
            border: none;
            display: block;
        }
        .warning {
            background: #fbeae7;
            color: #b8412f;
            padding: 20px;
            text-align: center;
            font-size: 15px;
        }
        .warning code {
            background: #f0d9d4;
            padding: 2px 8px;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <?php if (!$status): ?>
        <div class="warning">
            ⚠️ Server Flask (Python) belum berjalan. Jalankan
            <code>python app.py</code> di terminal terlebih dahulu,
            lalu refresh halaman ini.
        </div>
    <?php else: ?>
        <iframe src="<?php echo $flask_url; ?>"></iframe>
    <?php endif; ?>
</body>
</html>
