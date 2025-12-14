import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from abc import ABC, abstractmethod
from datetime import datetime
import calendar

# =============================================================================
# 1. KONFIGURASI GLOBAL (WARNA & FONT)
# Mengumpulkan semua aset visual di satu tempat agar mudah diubah.
# =============================================================================
COLORS = {
    "pink_header": "#FF9EAA",
    "pink_main": "#FF71AB",
    "lavender": "#E2BCFF",
    "cream": "#FFF5E4",
    "white": "#FFFFFF",
    "lime": "#B0D9B1", 
    "rose": "#FF8F8F",
    "danger": "#D04848",
    "text": "#5C5470",
    "btn_text": "#FFFFFF"
}

# Font kustom untuk tema "Cute"
FONT_TITLE_L = ("Comic Sans MS", 24, "bold") 
FONT_TITLE_M = ("Comic Sans MS", 14, "bold")
FONT_UI_S = ("Comic Sans MS", 10)
FONT_STD = ("Segoe UI Emoji", 10)

# =============================================================================
# 2. DATABASE MANAGER
# Menangani semua koneksi ke SQLite (Create, Read, Delete).
# =============================================================================
class DatabaseManager:
    def __init__(self, db_file="dompet_pintar.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.buat_tabel()

    def buat_tabel(self):
        """Membuat tabel users dan transaksi jika belum ada."""
        # Tabel untuk Login
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)
        # Tabel untuk Data Keuangan
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            jenis TEXT,
            kategori TEXT,
            deskripsi TEXT,
            nominal REAL,
            tanggal TEXT
        )
        """)
        self.conn.commit()

    def registrasi_user(self, username, password):
        """Mendaftarkan user baru."""
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Username sudah ada

    def cek_login(self, username, password):
        """Memvalidasi login user."""
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone() is not None

    def tambah_data(self, username, jenis, kategori, deskripsi, nominal):
        """Menyimpan transaksi ke database."""
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO transaksi (username, jenis, kategori, deskripsi, nominal, tanggal) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, jenis, kategori, deskripsi, nominal, tanggal))
        self.conn.commit()

    def ambil_semua_data(self, username):
        """Mengambil data milik user tertentu."""
        self.cursor.execute("SELECT * FROM transaksi WHERE username=? ORDER BY tanggal DESC", (username,))
        return self.cursor.fetchall()

    def ambil_data_tahunan(self, username, tahun):
        """Mengambil rekap data per bulan untuk tahun tertentu."""
        query = """
            SELECT strftime('%m', tanggal) as bulan, jenis, SUM(nominal) 
            FROM transaksi 
            WHERE strftime('%Y', tanggal) = ? AND username = ? 
            GROUP BY bulan, jenis
        """
        self.cursor.execute(query, (str(tahun), username))
        return self.cursor.fetchall()

    def hapus_data(self, id_transaksi):
        """Menghapus data berdasarkan ID."""
        self.cursor.execute("DELETE FROM transaksi WHERE id=?", (id_transaksi,))
        self.conn.commit()

# =============================================================================
# 3. PENERAPAN OOP (CORE LOGIC)
# Bagian ini PENTING untuk nilai UAS: Inheritance, Encapsulation, Polymorphism.
# =============================================================================

class Transaksi(ABC):
    """
    [PARENT CLASS] Kelas abstrak untuk semua jenis transaksi.
    """
    def __init__(self, deskripsi, nominal, kategori):
        self.deskripsi = deskripsi
        self.kategori = kategori
        # [ENCAPSULATION] Atribut private
        self.__nominal = nominal 

    def get_nominal(self):
        return self.__nominal

    @abstractmethod
    def info_sukses(self):
        """[POLYMORPHISM] Method abstrak yang akan di-override anak."""
        pass

class Pemasukan(Transaksi):
    """[CHILD CLASS] Mewarisi Transaksi."""
    def info_sukses(self):
        # [POLYMORPHISM] Override pesan untuk Pemasukan
        return f"Yey! Uang masuk Rp {self.get_nominal():,.0f} berhasil disimpan! 🤑"

class Pengeluaran(Transaksi):
    """[CHILD CLASS] Mewarisi Transaksi."""
    def info_sukses(self):
        # [POLYMORPHISM] Override pesan untuk Pengeluaran
        return f"Oke, pengeluaran Rp {self.get_nominal():,.0f} tercatat. Hemat ya! 🥺"

# =============================================================================
# 4. KOMPONEN UI & UTILITIES
# =============================================================================

def create_washi_tape(parent):
    """Membuat hiasan visual pita washi tape di bagian atas window."""
    frame = tk.Frame(parent, bg=COLORS["cream"], height=30)
    frame.pack(fill="x", side="top")
    pattern = "🍓  ✨  🌸  ✨  🍓  ✨  🌸  ✨  🍓  ✨  🌸  ✨  🍓"
    tk.Label(frame, text=pattern, font=("Segoe UI Emoji", 12), bg=COLORS["cream"], fg=COLORS["pink_main"]).pack(pady=2)

# =============================================================================
# 5. WINDOWS (LOGIN & REGISTER)
# =============================================================================

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("🍓 Dompet Pintar - Login")
        self.root.geometry("400x550")
        self.root.configure(bg=COLORS["cream"])
        self.db = DatabaseManager()

        create_washi_tape(self.root)

        # Kartu Login (Tengah)
        card = tk.Frame(root, bg=COLORS["white"], padx=30, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center", width=340)

        # Logo & Judul
        tk.Label(card, text="🧸", font=("Segoe UI Emoji", 50), bg=COLORS["white"]).pack()
        tk.Label(card, text="Welcome!", font=FONT_TITLE_L, bg=COLORS["white"], fg=COLORS["pink_main"]).pack(pady=(0, 5))
        
        # Input Fields
        self.entry_user = self.create_styled_entry(card, "Username 🎀")
        self.entry_pass = self.create_styled_entry(card, "Password 🔐", show_char="•")

        # Tombol Login
        tk.Button(card, text="Masuk Sekarang ✨", bg=COLORS["pink_main"], fg="white", 
                  font=FONT_TITLE_M, relief="flat", cursor="hand2", 
                  command=self.proses_login).pack(fill="x", pady=10, ipady=5)

        # Link Register
        frame_reg = tk.Frame(card, bg=COLORS["white"])
        frame_reg.pack(pady=10)
        tk.Label(frame_reg, text="Belum punya akun?", bg=COLORS["white"], font=FONT_UI_S).pack(side="left")
        tk.Button(frame_reg, text="Daftar disini 📝", bg=COLORS["white"], fg=COLORS["pink_main"], 
                  bd=0, font=("Comic Sans MS", 10, "bold"), cursor="hand2",
                  command=self.buka_register).pack(side="left")

    def create_styled_entry(self, parent, label_txt, show_char=None):
        """Membuat input field dengan garis bawah (style material design)."""
        tk.Label(parent, text=label_txt, font=FONT_UI_S, bg=COLORS["white"], fg=COLORS["text"]).pack(anchor="w")
        entry = tk.Entry(parent, font=FONT_STD, bg=COLORS["cream"], relief="flat", show=show_char)
        entry.pack(fill="x", pady=(5, 15), ipady=5)
        # Garis hiasan
        tk.Frame(parent, bg=COLORS["lavender"], height=2).pack(fill="x", pady=(0, 10))
        return entry

    def proses_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        if self.db.cek_login(username, password):
            self.root.withdraw() # Sembunyikan login window
            Dashboard(tk.Toplevel(self.root), self.root, username) # Buka dashboard
        else:
            messagebox.showerror("Ups!", "Username atau Password salah nih 🥺")

    def buka_register(self):
        RegisterWindow(self.root, self.db)

class RegisterWindow:
    def __init__(self, parent, db_manager):
        self.window = tk.Toplevel(parent)
        self.window.title("Daftar Akun Baru ✨")
        self.window.geometry("350x450")
        self.window.configure(bg=COLORS["cream"])
        self.db = db_manager
        create_washi_tape(self.window)
        
        tk.Label(self.window, text="Buat Akun 🍓", font=FONT_TITLE_L, bg=COLORS["cream"], fg=COLORS["text"]).pack(pady=20)
        
        frame_form = tk.Frame(self.window, bg=COLORS["cream"], padx=30)
        frame_form.pack(fill="both")

        tk.Label(frame_form, text="Username Baru:", bg=COLORS["cream"], font=FONT_UI_S).pack(anchor="w")
        self.entry_user = tk.Entry(frame_form, font=FONT_STD, bg="white", relief="flat")
        self.entry_user.pack(fill="x", pady=5, ipady=5)
        
        tk.Label(frame_form, text="Password:", bg=COLORS["cream"], font=FONT_UI_S).pack(anchor="w", pady=(10,0))
        self.entry_pass = tk.Entry(frame_form, font=FONT_STD, bg="white", relief="flat", show="•")
        self.entry_pass.pack(fill="x", pady=5, ipady=5)

        tk.Button(self.window, text="Simpan Akun ✅", bg=COLORS["lime"], fg=COLORS["text"], 
                  font=FONT_TITLE_M, relief="flat", command=self.simpan_akun).pack(fill="x", padx=30, pady=30, ipady=5)

    def simpan_akun(self):
        if self.db.registrasi_user(self.entry_user.get(), self.entry_pass.get()):
            messagebox.showinfo("Yey!", "Akun berhasil dibuat! Login yuk 🥳")
            self.window.destroy()
        else:
            messagebox.showwarning("Hmm..", "Username itu udah dipake orang lain 😢")

# =============================================================================
# 6. DASHBOARD UTAMA (GUI UTAMA)
# =============================================================================

class Dashboard:
    def __init__(self, root, original_root, username):
        self.root = root
        self.original_root = original_root
        self.username = username
        
        self.root.title(f"🎀 Dashboard - {username}")
        self.root.geometry("950x720") 
        self.root.configure(bg=COLORS["cream"])
        self.db = DatabaseManager()
        
        # Saat dashboard ditutup, matikan seluruh aplikasi
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_styles()
        self.setup_header()       
        self.setup_input_area()   
        self.setup_footer()       
        self.setup_table()        

        self.refresh_data()

    def setup_styles(self):
        """Konfigurasi style untuk Treeview dan Progressbar."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style Tabel
        style.configure("Treeview.Heading", background=COLORS["pink_main"], foreground="white", font=FONT_UI_S, relief="flat")
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=FONT_STD, borderwidth=0)
        style.map("Treeview", background=[('selected', COLORS["lavender"])])
        
        # Style Progress Bar
        style.configure("Pink.Horizontal.TProgressbar", troughcolor=COLORS["cream"], background=COLORS["lime"], thickness=15, borderwidth=0)
        
        # Style Combobox dropdown font
        self.root.option_add('*TCombobox*Listbox.font', FONT_STD)

    def setup_header(self):
        """Header Pink dengan info user, saldo, dan meteran hemat."""
        frame_header = tk.Frame(self.root, bg=COLORS["pink_main"], height=160) 
        frame_header.pack(fill="x", side="top")
        frame_header.pack_propagate(False) # Agar ukuran frame tetap

        # Pattern Hiasan
        tk.Label(frame_header, text="✨ 🍓 ✨ 🍓 ✨ 🍓 ✨ 🍓 ✨", bg=COLORS["pink_main"], fg="white", font=("Segoe UI Emoji", 10)).pack(pady=(5,0))
        
        # Top Bar (Nama & Tombol Logout)
        frame_top = tk.Frame(frame_header, bg=COLORS["pink_main"])
        frame_top.pack(fill="x", padx=30, pady=5)
        
        tk.Label(frame_top, text=f"Halo, {self.username}! 👋", font=("Comic Sans MS", 22, "bold"), bg=COLORS["pink_main"], fg="white").pack(side="left")
        
        btn_logout = tk.Button(frame_top, text="Keluar ➜", bg="#FF5588", fg="white", bd=0, font=("Comic Sans MS", 10, "bold"), 
                            cursor="hand2", command=self.logout)
        btn_logout.pack(side="right")

        # --- FLOATING CARD SALDO ---
        self.card_saldo = tk.Frame(self.root, bg="white", bd=0)
        self.card_saldo.place(relx=0.5, y=85, anchor="n", width=380, height=110)
        
        tk.Label(self.card_saldo, text="💰 Sisa Uang Jajan:", font=("Comic Sans MS", 11), bg="white", fg="grey").pack(pady=(10,0))
        self.lbl_saldo = tk.Label(self.card_saldo, text="Rp 0", font=("Comic Sans MS", 20, "bold"), bg="white", fg=COLORS["pink_main"])
        self.lbl_saldo.pack(pady=2)

        # --- METERAN HEMAT (PROGRESS BAR) ---
        frame_bar = tk.Frame(self.card_saldo, bg="white")
        frame_bar.pack(fill="x", padx=25, pady=(5,0))
        
        tk.Label(frame_bar, text="Meteran Boros: ", font=("Segoe UI Emoji", 9), bg="white", fg="grey").pack(side="left")
        
        self.progress_hemat = ttk.Progressbar(frame_bar, style="Pink.Horizontal.TProgressbar", length=100, mode='determinate')
        self.progress_hemat.pack(side="left", fill="x", expand=True, padx=5)
        
        self.lbl_persen_boros = tk.Label(frame_bar, text="0%", font=("Segoe UI Emoji", 9, "bold"), bg="white", fg=COLORS["lime"])
        self.lbl_persen_boros.pack(side="right")

    def setup_input_area(self):
        """Area Form Input Data Transaksi."""
        # Spacer
        tk.Frame(self.root, bg=COLORS["cream"], height=50).pack(side="top") 
        
        wrapper = tk.Frame(self.root, bg=COLORS["cream"])
        wrapper.pack(fill="x", padx=30, pady=5, side="top")

        # LabelFrame Container
        lf_input = tk.LabelFrame(wrapper, text=" ✨ Tambah Catatan Baru ✨ ", font=FONT_TITLE_M, 
                           bg=COLORS["white"], fg=COLORS["text"], bd=0, padx=30, pady=15)
        lf_input.pack(fill="x")
        lf_input.columnconfigure(0, weight=1)
        lf_input.columnconfigure(1, weight=3)

        # 1. Deskripsi
        tk.Label(lf_input, text="Keperluan 📝 :", bg="white", font=FONT_UI_S).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.entry_desc = tk.Entry(lf_input, bg=COLORS["cream"], relief="flat", font=FONT_STD)
        self.entry_desc.grid(row=0, column=1, sticky="w", ipadx=5, ipady=5, padx=10)

        # 2. Nominal (DENGAN AUTO FORMAT)
        tk.Label(lf_input, text="Berapa? 💸 :", bg="white", font=FONT_UI_S).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.entry_nom = tk.Entry(lf_input, bg=COLORS["cream"], relief="flat", font=FONT_STD)
        self.entry_nom.grid(row=1, column=1, sticky="w", ipadx=5, ipady=5, padx=10)
        self.entry_nom.bind('<KeyRelease>', self.format_rupiah_typing) # Bind event ngetik

        # 3. Kategori
        tk.Label(lf_input, text="Kategori 🏷️ :", bg="white", font=FONT_UI_S).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.combo_kategori = ttk.Combobox(lf_input, values=["🍔 Makanan", "🚗 Transport", "🛍️ Belanja", "💰 Gaji", "💅 Skincare", "✨ Lainnya"], 
                                  font=FONT_STD, width=25, state="readonly")
        self.combo_kategori.current(0)
        self.combo_kategori.grid(row=2, column=1, sticky="w", padx=10, ipady=3)

        # 4. Jenis Transaksi
        tk.Label(lf_input, text="Tipe ⚖️ :", bg="white", font=FONT_UI_S).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        frame_radio = tk.Frame(lf_input, bg="white")
        frame_radio.grid(row=3, column=1, sticky="w", padx=10)
        
        self.var_jenis = tk.StringVar(value="Pengeluaran")
        rb_style = {"bg": "white", "font": FONT_STD, "activebackground": "white", "cursor": "hand2"}
        tk.Radiobutton(frame_radio, text="Pemasukan 📈", variable=self.var_jenis, value="Pemasukan", fg=COLORS["lime"], **rb_style).pack(side="left")
        tk.Radiobutton(frame_radio, text="Pengeluaran 📉", variable=self.var_jenis, value="Pengeluaran", fg=COLORS["rose"], **rb_style).pack(side="left", padx=15)

        # Tombol Simpan
        btn_simpan = tk.Button(lf_input, text="💖 SIMPAN CATATAN 💖", bg=COLORS["lavender"], fg=COLORS["text"], 
                               font=FONT_TITLE_M, bd=0, cursor="hand2", command=self.simpan_transaksi)
        btn_simpan.grid(row=4, column=0, columnspan=2, sticky="ew", padx=50, pady=(15, 5), ipady=5)

    def setup_footer(self):
        """Area tombol aksi tambahan di bawah."""
        frame_footer = tk.Frame(self.root, bg=COLORS["cream"], pady=15)
        frame_footer.pack(side="bottom", fill="x")
        
        btn_style = {"font": FONT_UI_S, "bd": 0, "cursor": "hand2", "padx": 20, "pady": 8}
        
        tk.Button(frame_footer, text="🗑️ Hapus Data", bg=COLORS["rose"], fg="white", 
                  activebackground="#D04848", command=self.hapus_data, **btn_style).pack(side="left", padx=30)
        
        tk.Button(frame_footer, text="📂 Export CSV", bg=COLORS["lime"], fg=COLORS["text"], 
                  activebackground="#95D2B3", command=self.export_csv, **btn_style).pack(side="left", padx=5)
        
        tk.Button(frame_footer, text="📅 Lihat Arsip Tahunan", bg=COLORS["pink_main"], fg="white", 
                  activebackground="#FF5588", command=self.buka_arsip, **btn_style).pack(side="right", padx=30)

    def setup_table(self):
        """Area Tabel Riwayat Transaksi."""
        frame_table = tk.Frame(self.root, bg=COLORS["cream"], padx=30, pady=10)
        frame_table.pack(fill="both", expand=True, side="top")

        tk.Label(frame_table, text="Riwayat Transaksi Terakhir 👇", font=FONT_UI_S, bg=COLORS["cream"], fg="grey").pack(anchor="w", pady=(0,5))

        cols = ("ID", "Tanggal", "Jenis", "Kategori", "Deskripsi", "Nominal")
        self.tree = ttk.Treeview(frame_table, columns=cols, show="headings")
        
        for c in cols: self.tree.heading(c, text=c)
        
        # Konfigurasi kolom
        self.tree.column("ID", width=0, stretch=False) # Sembunyikan ID
        self.tree.column("Tanggal", width=100, anchor="center")
        self.tree.column("Jenis", width=80, anchor="center")
        self.tree.column("Kategori", width=100, anchor="center")
        self.tree.column("Deskripsi", width=250, anchor="w")
        self.tree.column("Nominal", width=120, anchor="e")

        scrollbar = ttk.Scrollbar(frame_table, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Tag warna baris
        self.tree.tag_configure("in", foreground="#6A9C89", background="#E9EFEC")
        self.tree.tag_configure("out", foreground="#D04848", background="#FDECEC")

    # =========================================================================
    # LOGIKA & EVENT HANDLERS
    # =========================================================================

    def format_rupiah_typing(self, event=None):
        """Format angka menjadi format ribuan (1.000.000) saat mengetik."""
        value = self.entry_nom.get()
        clean_value = value.replace(".", "") # Hapus titik lama
        
        if clean_value == "": return
            
        if clean_value.isdigit():
            # Format ulang dengan titik
            formatted = "{:,.0f}".format(int(clean_value)).replace(",", ".")
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, formatted)

    def simpan_transaksi(self):
        try:
            desc = self.entry_desc.get()
            raw_nom = self.entry_nom.get().replace(".", "") # Ambil angka murni
            jenis = self.var_jenis.get()
            kategori = self.combo_kategori.get()
            
            if not desc: return messagebox.showwarning("Eits!", "Deskripsinya diisi dulu dong 😉")
            if not raw_nom: return messagebox.showwarning("Kosong?", "Isi nominalnya ya!")

            nominal = float(raw_nom)

            # [PENERAPAN OOP] Membuat Objek Transaksi sesuai Jenisnya
            transaksi_baru = None
            if jenis == "Pemasukan":
                transaksi_baru = Pemasukan(desc, nominal, kategori)
            else:
                transaksi_baru = Pengeluaran(desc, nominal, kategori)

            # Simpan ke DB menggunakan data dari Objek
            self.db.tambah_data(self.username, jenis, transaksi_baru.kategori, 
                                transaksi_baru.deskripsi, transaksi_baru.get_nominal())
            
            # Reset form
            self.entry_desc.delete(0, 'end')
            self.entry_nom.delete(0, 'end')
            self.refresh_data()
            
            # Tampilkan pesan sukses dari Method Polymorphism
            messagebox.showinfo("Sukses", transaksi_baru.info_sukses())

        except ValueError: 
            messagebox.showerror("Error", "Nominal harus angka ya cantik/ganteng 🥺")

    def refresh_data(self):
        """Mengambil data terbaru dan menghitung ulang saldo/meteran boros."""
        for i in self.tree.get_children(): self.tree.delete(i)
        
        data = self.db.ambil_semua_data(self.username)
        saldo = 0
        total_masuk = 0
        total_keluar = 0

        for r in data:
            # r = (id, username, jenis, kategori, deskripsi, nominal, tanggal)
            is_income = r[2] == "Pemasukan"
            nominal = r[5]
            
            if is_income:
                saldo += nominal
                total_masuk += nominal
            else:
                saldo -= nominal
                total_keluar += nominal
            
            tgl_short = r[6][:10] # Ambil tanggal saja (YYYY-MM-DD)
            jenis_txt = "Masuk" if is_income else "Keluar"
            tag = "in" if is_income else "out"
            
            # Masukkan ke tabel
            self.tree.insert("", "end", values=(r[0], tgl_short, jenis_txt, r[3], r[4], f"Rp {nominal:,.0f}"), tags=(tag,))
            
        # Update UI Saldo
        self.lbl_saldo.config(text=f"Rp {saldo:,.0f}")
        self.lbl_saldo.config(fg=COLORS["danger"] if saldo < 0 else COLORS["pink_main"])

        # Update Meteran Boros
        persen_boros = 0
        if total_masuk > 0:
            persen_boros = (total_keluar / total_masuk) * 100
        elif total_keluar > 0:
            persen_boros = 100 

        tampilan_persen = min(persen_boros, 100)
        self.progress_hemat['value'] = tampilan_persen
        self.lbl_persen_boros.config(text=f"{int(persen_boros)}%")

        # Ganti warna progress bar jika boros > 75%
        s = ttk.Style()
        if persen_boros > 75:
            s.configure("Pink.Horizontal.TProgressbar", background=COLORS["danger"]) 
            self.lbl_persen_boros.config(fg=COLORS["danger"])
        else:
            s.configure("Pink.Horizontal.TProgressbar", background=COLORS["lime"]) 
            self.lbl_persen_boros.config(fg=COLORS["lime"])

    def hapus_data(self):
        if not self.tree.selection(): 
            messagebox.showinfo("Info", "Pilih dulu data yang mau dihapus yaa")
            return
        if messagebox.askyesno("Hapus?", "Yakin mau hapus data ini? 🥺"):
            for i in self.tree.selection(): 
                item_id = self.tree.item(i)['values'][0]
                self.db.hapus_data(item_id)
            self.refresh_data()

    def export_csv(self):
        """Fitur Export data tabel ke file CSV."""
        if not self.tree.get_children():
            messagebox.showwarning("Kosong", "Belum ada data buat diexport nih 😅")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")], 
                                                 title="Simpan Laporan")
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    cols = ("ID", "Tanggal", "Jenis", "Kategori", "Deskripsi", "Nominal")
                    writer.writerow(cols)
                    
                    for item in self.tree.get_children():
                        row = self.tree.item(item)['values']
                        # Bersihkan format Rp dan koma agar jadi angka murni di Excel
                        clean_row = list(row)
                        clean_row[5] = str(row[5]).replace("Rp ", "").replace(",", "")
                        writer.writerow(clean_row)
                        
                messagebox.showinfo("Berhasil", f"Laporan tersimpan di:\n{file_path} ✅")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal nyimpen file: {e}")

    def buka_arsip(self):
        ArsipWindow(self.root, self.db, self.username)

    def logout(self):
        self.root.destroy()
        self.original_root.deiconify() # Tampilkan lagi window login
        
    def on_close(self):
        """Menutup aplikasi sepenuhnya."""
        self.root.destroy()
        self.original_root.destroy()

# =============================================================================
# 7. WINDOW ARSIP TAHUNAN
# =============================================================================

class ArsipWindow:
    def __init__(self, parent, db, user):
        self.win = tk.Toplevel(parent)
        self.win.title("📅 Arsip Tahunan")
        self.win.geometry("600x500")
        self.win.configure(bg=COLORS["cream"])
        self.db = db
        self.user = user

        create_washi_tape(self.win)
        tk.Label(self.win, text="Rekap Keuangan 📊", font=FONT_TITLE_M, bg=COLORS["cream"], fg=COLORS["text"]).pack(pady=10)

        # Filter Tahun
        frame_filter = tk.Frame(self.win, bg=COLORS["cream"])
        frame_filter.pack()
        self.combo_tahun = ttk.Combobox(frame_filter, values=["2025", "2024", "2023"], width=10)
        self.combo_tahun.current(0)
        self.combo_tahun.pack(side="left")
        
        tk.Button(frame_filter, text="Cek!", bg=COLORS["lime"], bd=0, command=self.load_data).pack(side="left", padx=5)

        # Tabel Arsip
        self.tree = ttk.Treeview(self.win, columns=("Bulan", "Masuk", "Keluar"), show="headings")
        for c in ("Bulan", "Masuk", "Keluar"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.load_data()

    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        
        # Ambil data agregat dari DB
        data = self.db.ambil_data_tahunan(self.user, self.combo_tahun.get())
        
        # Struktur data: rekap[bulan] = {'in': 0, 'out': 0}
        rekap = {f"{i:02d}": {'in':0, 'out':0} for i in range(1,13)}
        
        for r in data:
            bulan_key = r[0]
            jenis = r[1]
            total = r[2]
            key_jenis = 'in' if jenis == "Pemasukan" else 'out'
            rekap[bulan_key][key_jenis] = total
            
        # Masukkan ke tabel urut bulan
        for i in range(1,13):
            k = f"{i:02d}"
            nama_bulan = calendar.month_name[i]
            masuk = rekap[k]['in']
            keluar = rekap[k]['out']
            
            # Hanya tampilkan jika ada transaksi
            if masuk > 0 or keluar > 0:
                self.tree.insert("", "end", values=(nama_bulan, f"{masuk:,.0f}", f"{keluar:,.0f}"))

# =============================================================================
# MAIN PROGRAM
# =============================================================================

if __name__ == "__main__":
    root = tk.Tk()
    # Menjalankan Login Window terlebih dahulu
    app = LoginWindow(root)
    root.mainloop()