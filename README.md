

#🌸 My-Wallet (Dompet Pintar) 

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-pink?style=for-the-badge&logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite3-green?style=for-the-badge&logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

**Aplikasi Manajemen Keuangan Desktop yang Simpel, Estetik, dan Cerdas.**
<br>
Developed for Final Exam Project (UAS)

[Fitur Utama](#-fitur-unggulan) • [Teknologi](#-teknologi-yang-digunakan) • [Konsep OOP](#-penerapan-oop) • [Instalasi](#-cara-instalasi--penggunaan)

</div>

---

## 📝 Deskripsi

**My-Wallet** adalah aplikasi desktop berbasis Python yang dirancang untuk membantu pengguna mencatat pemasukan dan pengeluaran harian dengan antarmuka yang ramah pengguna dan estetik. 

Berbeda dengan pencatat keuangan biasa, aplikasi ini dilengkapi dengan **"Meteran Boros"** visual untuk memantau kesehatan finansial secara real-time, serta fitur ekspor laporan untuk analisis lebih lanjut.

## 🌟 Fitur Unggulan

* **🎨 Cute & Aesthetic UI:** Antarmuka bertema *Pink/Cream* dengan hiasan visual (Washi Tape style) yang nyaman dipandang.
* **🔐 Sistem Autentikasi:** Keamanan data pengguna dengan sistem Login & Register (disimpan dalam database).
* **💸 Smart Dashboard:**
    * Menampilkan sisa saldo secara real-time.
    * **Meteran Boros (Waste Meter):** Progress bar dinamis yang berubah warna (Hijau/Merah) berdasarkan persentase pengeluaran.
* **📝 Manajemen Transaksi:** Catat Pemasukan dan Pengeluaran dengan kategori yang lengkap (Makanan, Transport, Skincare, dll).
* **📊 Riwayat & Arsip:**
    * Tabel riwayat transaksi interaktif.
    * Fitur **Arsip Tahunan** untuk melihat rekapitulasi per bulan.
* **📂 Export Data:** Simpan laporan keuangan ke format **.CSV** (kompatibel dengan Excel/Spreadsheet).

## 🛠 Teknologi yang Digunakan

* **Language:** Python 3.10+
* **GUI Framework:** Tkinter & Ttk (Themed Tkinter)
* **Database:** SQLite3 (Embedded database, tanpa setup server)
* **Libraries:** `csv`, `datetime`, `calendar`, `abc` (Abstract Base Class)

## 🧠 Penerapan OOP (Object-Oriented Programming)

Proyek ini dibangun menggunakan prinsip OOP yang kuat untuk memastikan kode rapi, modular, dan mudah dikembangkan:

1.  **Inheritance (Pewarisan):**
    * Terdapat *Parent Class* `Transaksi` yang menurunkan sifatnya ke *Child Classes* `Pemasukan` dan `Pengeluaran`.
2.  **Encapsulation (Enkapsulasi):**
    * Penggunaan atribut private (contoh: `self.__nominal`) untuk melindungi data sensitif agar tidak diakses langsung secara sembarangan.
3.  **Polymorphism (Polimorfisme):**
    * Method `info_sukses()` yang memiliki perilaku berbeda (pesan notifikasi unik) tergantung apakah objek tersebut adalah Pemasukan atau Pengeluaran.
4.  **Abstraction (Abstraksi):**
    * Menggunakan `ABC` (*Abstract Base Class*) untuk memaksakan struktur standar pada kelas transaksi.

## 📸 Screenshots

*(Tempatkan screenshot aplikasi kamu di sini agar orang bisa melihat desainnya)*

| Login Screen | Dashboard Utama |
|:---:|:---:|
| <img src="https://via.placeholder.com/400x300?text=Login+Screen" width="400"> | <img src="https://via.placeholder.com/400x300?text=Dashboard+Screen" width="400"> |

## 🚀 Cara Instalasi & Penggunaan

Ikuti langkah berikut untuk menjalankan aplikasi di komputermu:

1.  **Clone Repository ini:**
    ```bash
    git clone [https://github.com/username-kamu/My-Wallet.git](https://github.com/username-kamu/My-Wallet.git)
    cd My-Wallet
    ```

2.  **Pastikan Python Terinstal:**
    Aplikasi ini menggunakan modul bawaan Python (Tkinter & SQLite), jadi tidak perlu `pip install` library eksternal yang berat.

3.  **Jalankan Aplikasi:**
    ```bash
    python uasfix.py
    ```
    *(Catatan: Jika nama file kamu ubah, sesuaikan perintah di atas)*

## 📂 Struktur Project



My-Wallet/
│
├── uasfix.py            \# Source code utama (Main Program)
├── dompet\_pintar.db     \# Database (Otomatis dibuat saat dijalankan)
├── README.md            \# Dokumentasi Project
└── Laporan.csv          \# Hasil export (Opsional)


## 🤝 Kontribusi

Tertarik mengembangkan fitur baru? Silakan fork repository ini dan buat Pull Request!
Ide pengembangan selanjutnya:
- [ ] Visualisasi grafik diagram lingkaran (Pie Chart).
- [ ] Fitur *budgeting* bulanan.
- [ ] Mode gelap (Dark Mode).

## 📄 Lisensi

Project ini dibuat untuk tujuan edukasi. Bebas digunakan dan dimodifikasi.

---
<div align="center">

**Dibuat dengan 💖 dan ☕ oleh [Angelica Immanuela]**

</div>
