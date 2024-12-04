import csv
import bcrypt
import smtplib
import os
import re
import threading
import schedule
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from tkinter import Tk, Canvas
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PIL import Image, ImageTk

# Fungsi untuk hashing password
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Fungsi untuk verifikasi password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Fungsi validasi email
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# Fungsi untuk menghitung cicilan per bulan

# Fungsi untuk mengirim email pengingat
def send_email(receiver_email, subject, message):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")  # Gunakan environment variable untuk keamanan

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email berhasil dikirim!")
    except Exception as e:
        print("Gagal mengirim email:", e)
    finally:
        server.quit()

# Fungsi untuk mengirim pengingat cicilan
def send_reminders():
    try:
        if not os.path.exists("users.csv"):
            print("File users.csv tidak ditemukan.")
            return

        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row["Email"]
                name = row["Name"]
                subject = "Pengingat Pembayaran Cicilan"
                body = (
                    f"Halo {name},\n\n"
                    "Ini adalah pengingat untuk pembayaran cicilan Anda.\n"
                    "Harap pastikan pembayaran cicilan Anda tepat waktu.\n\n"
                    "Terima kasih atas perhatian Anda!"
                )
                send_email(email, subject, body)
                print(f"Pengingat dikirim ke {email}")
    except Exception as e:
        print("Terjadi kesalahan:", e)

# Fungsi untuk menjadwalkan pengingat cicilan
def schedule_reminders():
    schedule.every().wednesday.at("09:00").do(send_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Daftar barang Samsung dengan tambahan path gambar
def load_items_from_csv(file_path):
    items = {}  # Inisialisasi dictionary untuk menyimpan data
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Lewati baris header
        for row in reader:
            name, price, image = row  # Ambil data per baris
            items[name] = {
                "price": int(price.replace('.', '').replace(',', '')),  # Konversi harga ke integer
                "image": image
            }
    return items

file_path = "database.csv"  # Sesuaikan nama file dengan lokasi file CSV Anda
items = load_items_from_csv("database.csv")


class SamsungStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAMSUNG STORE")
        self.root.geometry("1920x1080")
        
        # Load the background image
        image = Image.open(r"C:\Users\user\Downloads\jajal.jpg")
        image = image.resize((1600, 900))  # Resize the image to fit the window
        self.bg_image = ImageTk.PhotoImage(image)

        # Create Canvas to display the background
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Create a style for buttons and labels
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Roboto", 20), background="#f0f0f0")
        self.style.configure("TButton", font=("Roboto", 20), background="#007bff", foreground="#007bff")

        self.create_main_frame()

    def create_main_frame(self):
        # Create a Frame to hold the widgets (e.g., buttons and labels)
        main_frame = ttk.Frame(self.root, padding="50 40 50 40", style="TFrame")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

        # Title Label
        title_label = ttk.Label(main_frame, text="SAMSUNG STORE", font=("Lato", 20, "bold"))
        title_label.pack(pady=20)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=100)

        # Sign Up Button
        signup_btn = ttk.Button(button_frame, text="Sign Up", command=self.open_signup_window)
        signup_btn.pack(side=tk.LEFT, padx=100)

        # Log In Button
        login_btn = ttk.Button(button_frame, text="Log In", command=self.open_login_window)
        login_btn.pack(side=tk.LEFT, padx=100)

        # Exit Button
        exit_btn = ttk.Button(button_frame, text="Keluar", command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=100)

    def open_signup_window(self):
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("1920x1080")

        ttk.Label(signup_window, text="Email:").pack(pady=5)
        email_entry = ttk.Entry(signup_window, width=30)
        email_entry.pack(pady=5)

        ttk.Label(signup_window, text="Nama:").pack(pady=30)
        name_entry = ttk.Entry(signup_window, width=30)
        name_entry.pack(pady=5)

        ttk.Label(signup_window, text="Kata Sandi:").pack(pady=30)
        password_entry = ttk.Entry(signup_window, width=30, show="*")
        password_entry.pack(pady=5)

        ttk.Label(signup_window, text="Konfirmasi Kata Sandi:").pack(pady=30)
        confirm_password_entry = ttk.Entry(signup_window, width=30, show="*")
        confirm_password_entry.pack(pady=5)

        def signup():
            email = email_entry.get()
            name = name_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if not is_valid_email(email):
                messagebox.showerror("Error", "Format email tidak valid")
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Kata sandi tidak sama")
                return

            if not os.path.exists("data.csv"):
                with open("data.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Email", "Name", "Password"])

            with open("data.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Email"] == email:
                        messagebox.showerror("Error", "Email sudah terdaftar")
                        return

            hashed_password = hash_password(password)

            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([email, name, hashed_password])

            messagebox.showinfo("Success", "Akun berhasil dibuat")
            signup_window.destroy()

        signup_btn = ttk.Button(signup_window, text="Sign Up", command=signup)
        signup_btn.pack(pady=30)
        
        exit_btn = ttk.Button(signup_window, text="Keluar", command=signup_window.destroy)
        exit_btn.pack(pady=10)

    def open_login_window(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Log In")
        login_window.geometry("1920x1080")

        ttk.Label(login_window, text="Email:").pack(pady=100)
        email_entry = ttk.Entry(login_window, width=30)
        email_entry.pack(pady=5)

        ttk.Label(login_window, text="Kata Sandi:").pack(pady=5)
        password_entry = ttk.Entry(login_window, width=30, show="*")
        password_entry.pack(pady=5)

        def login():
            email = email_entry.get()
            password = password_entry.get()

            if not os.path.exists("data.csv"):
                messagebox.showerror("Error", "Belum ada pengguna yang terdaftar")
                return

            with open("data.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Email"] == email and verify_password(password, row["Password"]):
                        messagebox.showinfo("Success", "Berhasil login")
                        login_window.destroy()
                        self.open_dashboard(email)  # Buka dashboard
                        return

            messagebox.showerror("Error", "Email atau kata sandi salah")

        login_btn = ttk.Button(login_window, text="Log In", command=login)
        login_btn.pack(pady=100)

        exit_btn = ttk.Button(login_window, text="Keluar", command=login_window.destroy)
        exit_btn.pack(pady=100)
        
    def open_dashboard(self, name):
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("1920x1080")

        ttk.Label(dashboard_window, text=f"Selamat Datang, {name}!", font=("Arial", 16)).pack(pady=20)
        ttk.Label(dashboard_window, text="Daftar Produk", font=("Arial", 14)).pack(pady=10)
        for item_name, details in items.items():
            frame = ttk.Frame(dashboard_window)
            frame.pack(fill=tk.X, padx=20, pady=5)

            # Gambar produk (opsional, jika file tersedia)
            try:
                image = Image.open(details["image"])
                image = image.resize((160, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                img_label = ttk.Label(frame, image=photo)
                img_label.image = photo
                img_label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
            except FileNotFoundError:
                pass
            

            item_button = ttk.Button(frame, text=f"{item_name} - Rp{details['price']:,}", command=self.pembelian)
            item_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

        exit_btn = ttk.Button(dashboard_window, text="Keluar", command=dashboard_window.destroy)
        exit_btn.pack(pady=20)
    
    def pembelian(self, selected_item):
        item_details = items[selected_item]
        price = item_details["price"]

    # Window baru untuk pembayaran
        window_pembelian = tk.Toplevel(self.root)
        window_pembelian.title("Pembayaran")
        window_pembelian.geometry("400x400")

    # Label item yang dipilih
        ttk.Label(window_pembelian, text=f"Anda telah memilih: {selected_item}", font=("Arial", 14)).pack(pady=10)
        ttk.Label(window_pembelian, text=f"Harga: Rp{price:,}", font=("Arial", 14)).pack(pady=10)

    # Input durasi cicilan
        ttk.Label(window_pembelian, text="Durasi Cicilan (bulan):", font=("Arial", 12)).pack(pady=5)
        durasi_entry = ttk.Entry(window_pembelian)
        durasi_entry.pack(pady=5)

    # Pilihan metode pembayaran
        metode = {
        "BCA": "Bayar langsung dengan uang tunai",
        "BRI": "Bayar dengan kartu kredit",
        "GoPay": "Bayar nanti dengan metode cicilan",
        "DANA": "Bayar nanti dengan metode cicilan",
        "Mandiri": "Bayar langsung",
        "ShopeePay": "Bayar langsung"
        }

        metode_var = tk.StringVar()
        metode_var.set(list(metode.keys())[0])

        ttk.Label(window_pembelian, text="Pilih Metode Pembayaran:", font=("Arial", 12)).pack(pady=10)
        metode_menu = ttk.OptionMenu(window_pembelian, metode_var, *metode.keys())
        metode_menu.pack(pady=10)

    # Fungsi untuk menghitung cicilan
        def hitung_cicilan():
            try:
                durasi = int(durasi_entry.get())
                if durasi <= 0:
                    raise ValueError
                cicilan_per_bulan = price // durasi
                metode_pembayaran = metode_var.get()
                messagebox.showinfo("Detail Cicilan",
                                f"Metode: {metode_pembayaran}\n"
                                f"Cicilan per bulan: Rp{cicilan_per_bulan:,}\n"
                                f"Durasi: {durasi} bulan")
            except ValueError:
                messagebox.showerror("Error", "Durasi harus berupa angka positif!")

    # Tombol Hitung Cicilan
        hitung_btn = ttk.Button(window_pembelian, text="Hitung Cicilan", command=hitung_cicilan)
        hitung_btn.pack(pady=20)

    # Tombol Keluar
        exit_btn = ttk.Button(window_pembelian, text="Keluar", command=window_pembelian.destroy)
        exit_btn.pack(pady=10)
        
    def is_valid_email(self, email):
        # Validasi email
        return True

    def hash_password(self, password):
        # Hashing kata sandi
        return password

    def verify_password(self, password, hashed_password):
        # Verifikasi kata sandi
        return password == hashed_password

# Menginisialisasi aplikasi
root = tk.Tk()
app = SamsungStoreApp(root)
root.mainloop()