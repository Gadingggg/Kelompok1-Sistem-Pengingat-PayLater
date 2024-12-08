import csv
import bcrypt
import smtplib
import os
import re
import threading
import schedule
import time
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
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


# Fungsi untuk mengirim email pengingat
def send_email(receiver_email, subject, message):
    sender_email = "11novangading28@gmail.com"
    sender_password = "goiu efwk bplq uwyn"

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
        if not os.path.exists("data.csv"):
            print("File data.csv tidak ditemukan.")
            return

        with open("data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                email = row["Email"]
                name = row["Name"]
                subject = "Pengingat Pembayaran Cicilan"
                body = (
                    f"Halo {name},\n\n"
                    "Ini adalah pengingat untuk pembelian di Samsung Store Anda.\n"
                    "Harap pastikan pembayaran cicilan Anda tepat waktu.\n\n"
                    "Terima kasih atas perhatian Anda!"
                )
                send_email(email, subject, body)
                print(f"Pengingat dikirim ke {email}")
    except Exception as e:
        print("Terjadi kesalahan:", e)


# Fungsi untuk menjadwalkan pengingat cicilan
def schedule_reminders():
    schedule.every().sunday.at("12:00").do(send_reminders)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Daftar barang Samsung dengan tambahan path gambar
def load_items_from_csv(file_path):
    items = {}
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            name, price, image = row
            items[name] = {
                "price": int(price.replace(".", "").replace(",", "")),
                "image": image,
            }
    return items


file_path = "database.csv"
items = load_items_from_csv(file_path)


class SamsungStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAMSUNG STORE")
        self.root.attributes("-fullscreen", True)
        
        self.email = None

        self.cap = cv2.VideoCapture(r"C:\Users\user\Tubes\Tubes_Prokom\samsung vid.mp4")  # Ganti dengan path video Anda

        # Create a canvas to display the background video
        self.canvas = tk.Canvas(self.root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)
        
        # Create a style for buttons and labels
        self.style = ttk.Style()
        self.style.configure("Title.TLabel", font=("Monaco", 28, "bold"))
        self.style.configure("TButton", font=("Georgia", 20), background="#007bff", foreground="#007bff")

        self.play_video()  # Start the video playing

        self.create_main_frame()  # Create the main UI frame

    def play_video(self):
        # Capture the video frame by frame
        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert the frame to ImageTk format
            frame_image = Image.fromarray(frame)
            frame_image = ImageTk.PhotoImage(frame_image)

            # Display the frame on the canvas
            self.canvas.create_image(0, 0, image=frame_image, anchor="nw")

            # Keep a reference to the image to prevent it from being garbage collected
            self.canvas.image = frame_image

            # Call this function again after a small delay to keep the video playing
            self.root.after(5, self.play_video)
        else:
            # When the video ends, restart it
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.root.after(5, self.play_video)
            
    def clear_frame(self):
    # Hanya hapus widget selain canvas
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Canvas):  # Jangan hapus canvas
                continue
            widget.destroy()
            
    def create_main_frame(self):
        self.clear_frame()
        main_frame = ttk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ttk.Label(
        main_frame, text="SAMSUNG STORE", style="Title.TLabel"  # Teks lebih besar
        )
        title_label.pack(pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=50)  # Kurangi jarak vertikal
        
        signup_btn = ttk.Button(
        button_frame, text="Sign Up", command=self.open_signup_window, width=10
        )
        signup_btn.pack(side=tk.LEFT, padx=50)  # Kurangi jarak horizontal

        login_btn = ttk.Button(
            button_frame, text="Log In", command=self.open_login_window, width=10
        )
        login_btn.pack(side=tk.LEFT, padx=50)

        exit_btn = ttk.Button(
            button_frame, text="Keluar", command=self.root.quit, width=10
        )
        exit_btn.pack(side=tk.LEFT, padx=50)

    def open_signup_window(self):
        self.clear_frame()
        signup_window = tk.Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.attributes("-fullscreen", True)

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
                self.open_signup_window()
                return

            if password != confirm_password:
                messagebox.showerror("Error", "Kata sandi tidak sama")
                self.open_signup_window()
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
                        self.open_signup_window()
                        return

            hashed_password = hash_password(password)

            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([email, name, hashed_password])

            messagebox.showinfo("Success", "Akun berhasil dibuat")
            signup_window.destroy()
            self.open_dashboard(email)  # Buka dashboard
            return

        signup_btn = ttk.Button(signup_window, text="Sign Up", command=signup)
        signup_btn.pack(pady=30)
        
        exit_btn = ttk.Button(signup_window, text="Keluar", command=self.create_main_frame)
        exit_btn.pack(pady=10)

    def open_login_window(self):
        self.clear_frame()
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
                self.open_login_window()
                return

            with open("data.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Email"] == email and verify_password(password, row["Password"]):
                        self.email=email
                        messagebox.showinfo("Success", "Berhasil login")
                        login_window.destroy()
                        self.open_dashboard(email)  # Buka dashboard
                        return

            messagebox.showerror("Error", "Email atau kata sandi salah")
            self.open_login_window()
            return

        login_btn = ttk.Button(login_window, text="Log In", command=login)
        login_btn.pack(pady=100)

        exit_btn = ttk.Button(login_window, text="Keluar", command=self.create_main_frame)
        exit_btn.pack(pady=100)

    def open_dashboard(self, name):
        self.clear_frame()
        dashboard_window = tk.Toplevel(self.root)
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("1920x1080")

        ttk.Label(
            dashboard_window, text=f"Selamat Datang, {name}!", font=("Arial", 16)
        ).pack(pady=20)
        ttk.Label(dashboard_window, text="Daftar Produk", font=("Arial", 14)).pack(
            pady=10
        )

        self.current_page = tk.IntVar(value=1)
        self.items_per_page = 3
        self.total_pages = (len(items) + self.items_per_page - 1) // self.items_per_page

        self.content_frame = ttk.Frame(dashboard_window)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.nav_frame = ttk.Frame(dashboard_window)
        self.nav_frame.pack(pady=10)

        prev_button = ttk.Button(
            self.nav_frame, text="Previous", command=self.previous_page
        )
        prev_button.grid(row=0, column=0, padx=5)

        page_label = ttk.Label(
            self.nav_frame, textvariable=self.current_page, font=("Arial", 12)
        )
        page_label.grid(row=0, column=1, padx=5)

        next_button = ttk.Button(
            self.nav_frame, text="Next", command=self.next_page
        )
        next_button.grid(row=0, column=2, padx=5)
        
        exit_btn = ttk.Button(dashboard_window, text="Keluar", command=self.create_main_frame)
        exit_btn.place(x=50,y=100)

        self.render_page()

    def render_page(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        start_index = (self.current_page.get() - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = list(items.items())[start_index:end_index]

        for item_name, details in page_items:
            frame = ttk.Frame(self.content_frame)
            frame.pack(fill=tk.X, padx=20, pady=5)

            try:
                image = Image.open(details["image"])
                image = image.resize((150, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                img_label = ttk.Label(frame, image=photo)
                img_label.image = photo
                img_label.pack(side=tk.TOP, padx=5, pady=5, expand=True)
            except FileNotFoundError:
                pass

            item_button = ttk.Button(
                frame,
                text=f"{item_name} - Rp{details['price']:,}",
                command=lambda item=item_name: self.pembelian(item),
            )
            item_button.pack(side=tk.TOP, padx=10, pady=10, expand=True)

    def next_page(self):
        if self.current_page.get() < self.total_pages:
            self.current_page.set(self.current_page.get() + 1)
            self.render_page()

    def previous_page(self):
        if self.current_page.get() > 1:
            self.current_page.set(self.current_page.get() - 1)
            self.render_page()

    def pembelian(self, selected_item):
        window_pembelian = tk.Toplevel(self.root)
        window_pembelian.title("Pembayaran")
        window_pembelian.geometry("500x400")
    
    # Tampilkan item yang dipilih
        ttk.Label(
            window_pembelian, text=f"Anda telah memilih {selected_item}!", font=("Arial", 16)
        ).pack(pady=20)

        ttk.Label(window_pembelian, text="Durasi (bulan)").pack(pady=5)
        durasi_entry = ttk.Entry(window_pembelian, width=30)
        durasi_entry.pack(pady=5)

        metode = {
            "BCA": "Bayar langsung dengan uang tunai",
            "BRI": "Bayar dengan kartu kredit",
            "GoPay": "Bayar nanti dengan metode cicilan",
            "DANA": "Bayar dengan dompet digital",
            "Mandiri": "Bayar melalui transfer bank",
            "ShopeePay": "Bayar melalui e-wallet",
        }

        metode_var = tk.StringVar()
        metode_var.set(list(metode.keys())[0])  # Set default item
        
        selected_method = metode_var.get()

        ttk.Label(window_pembelian, text="Pilih Metode Pembayaran", font=("Arial", 14)).pack(pady=10)
        metode_menu = ttk.OptionMenu(window_pembelian, metode_var, *metode.keys())
        metode_menu.pack(pady=10)
        
        from functools import partial

    # Tombol untuk memproses pembelian
        proses_btn = ttk.Button(window_pembelian, text="Proses Pembelian", command=lambda: self.hitung_dan_kirim_email(durasi_entry, selected_item,self.email,selected_method))
        proses_btn.pack(pady=20)

    # Tombol keluar
        exit_btn = ttk.Button(window_pembelian, text="Keluar", command=window_pembelian.destroy)
        exit_btn.pack(pady=20)
        
    def hitung_dan_kirim_email(self, durasi_entry, selected_item,email,selected_method):
            # Ambil durasi cicilan dari input
        duration = int(durasi_entry.get())  # Durasi cicilan
        price = items[selected_item]["price"]  # Harga barang
        interest_rate = 0.05  # Bunga tetap (5% per tahun)

            # Hitung cicilan
        total_price = price + (price * interest_rate * duration / 12)
        monthly_installment = total_price / duration

            # Tampilkan hasil perhitungan
        messagebox.showinfo(
            "Detail Cicilan",
            f"Total Pembayaran: Rp{total_price:,.2f}\n"
            f"Cicilan per Bulan: Rp{monthly_installment:,.2f}\n"
            f"Dengan metode pembayaran :{selected_method:}"
        )

            # Kirim email dengan detail pembelian
        subject = "Detail Pembelian Barang"
        body = (
            f"Anda telah membeli {selected_item} dengan harga Rp{price:,.2f}.\n"
            f"Cicilan Anda selama {duration} bulan adalah Rp{monthly_installment:,.2f} per bulan.\n"
            f"Harap lakukan pembayaran tepat waktu. Terima kasih!\n"
        )
        send_email(self.email, subject, body)
        
        self.create_main_frame()
        return

def start_schedule():
    schedule_thread = threading.Thread(target=schedule_reminders)
    schedule_thread.daemon = True
    schedule_thread.start()

# Jalankan aplikasi
if __name__ == "__main__":
    start_schedule()
    root = tk.Tk()
    app = SamsungStoreApp(root)
    root.mainloop()
