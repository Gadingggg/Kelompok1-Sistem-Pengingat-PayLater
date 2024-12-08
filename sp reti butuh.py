import csv
import hashlib
import smtplib
import pandas as pd
import schedule
import time
import os
import threading
from tkinter import *
from tkinter import messagebox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fungsi untuk hashing password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Fungsi untuk menghitung cicilan per bulan
def calculate_installment(price, interest_rate, duration_months):
    total_price = price + (price * interest_rate * duration_months / 12)
    monthly_installment = total_price / duration_months
    return total_price, monthly_installment

# Fungsi untuk mengirim email pengingat
def send_email(receiver_email, subject, message):
    sender_email = "11novangading28@gmail.com"
    sender_password = "goiu efwk bplq uwyn"  # Gunakan App Password di sini

    try:
        # Membuat koneksi ke server Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Membuat email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Kirim email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email berhasil dikirim!")
    except Exception as e:
        print("Gagal mengirim email:", e)
    finally:
        server.quit()

# Fungsi untuk mengirim pengingat cicilan
def send_reminders():
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

# Fungsi untuk menjadwalkan pengingat cicilan
def schedule_reminders():
    schedule.every().wednesday.at("09:00").do(send_reminders)

    while True:
        schedule.run_pending()  # Mengeksekusi tugas yang dijadwalkan
        time.sleep(1)  # Menunggu sebentar sebelum memeriksa lagi

# Daftar barang Samsung beserta harga
items = {
    "Samsung Galaxy A55 5G 8/256GB - Awesome Ice Blue": 5729000,
    "Samsung Galaxy A35 5G 8/256GB - Awesome Ice Blue": 4799000,
    "Samsung Galaxy S23 8GB/256GB - Phantom Black": 9999000,
    "Samsung Galaxy S23 Ultra 12GB/256GB-Phantom Black": 16199000,
    "Samsung Galaxy Z Flip6 12/512GB - Silver": 18999000,
    "Samsung Galaxy Z Fold6 12/256GB - Silver Shadow": 26499000,
    "Samsung Soundbar HW-B550 2.1ch dengan Dolby Audio & Bass Boost": 2199000,
    "Samsung Soundbar HW-B650 3.1ch dengan Dolby Audio & Bass Boost": 2749000,
    "Samsung HD TV 32 inch UA32T4001": 2699000,
    "Samsung Smart TV 43 inch UHD 4K AU7002": 3299000,
    "Samsung Smart TV 65 inch UHD 4K AU7002": 7399000,
    "Samsung Smart TV 50 inch QLED 4K Q60D": 7999000,
    "Samsung Alpha Inverter AC 0,5 PK": 3569900,
    "Samsung Alpha Inverter AC 1.5 PK": 5149900,
    "Samsung Mesin Cuci Top Loading 8 KG WA80H4200SW": 2429000,
    "Samsung Mesin Cuci Front Loading 8 Kg - WW80T3040BW/SE": 4438500,
    "Samsung VC18M2120SB/SE Canister Vacuum Cleaner": 1394300,
    "Samsung Microwave Solo, 30 L - MS30T5018UK": 1729900,
    "Samsung Microwave Grill, 30 L - MG30T5068CK": 1829900,
}

# Fungsi untuk sign up
def sign_up():
    def submit_signup():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        hashed_password = hash_password(password)

        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Email", "Password"])

        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email:
                    messagebox.showerror("Error", "Email sudah terdaftar.")
                    return

        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, hashed_password])
            messagebox.showinfo("Success", "Sign Up berhasil! Silakan login.")

    sign_up_window = Toplevel(root)
    sign_up_window.title("Sign Up")

    Label(sign_up_window, text="Nama:").pack()
    name_entry = Entry(sign_up_window)
    name_entry.pack()

    Label(sign_up_window, text="Email:").pack()
    email_entry = Entry(sign_up_window)
    email_entry.pack()

    Label(sign_up_window, text="Password:").pack()
    password_entry = Entry(sign_up_window, show="*")
    password_entry.pack()

    Button(sign_up_window, text="Sign Up", command=submit_signup).pack()

# Fungsi untuk log in
def log_in():
    def submit_login():
        email = email_entry.get()
        password = password_entry.get()

        hashed_password = hash_password(password)

        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Email"] == email and row["Password"] == hashed_password:
                    messagebox.showinfo("Success", f"Selamat datang, {row['Name']}!")
                    purchase_item(email)
                    return

        messagebox.showerror("Error", "Email atau password salah. Silakan coba lagi.")

    log_in_window = Toplevel(root)
    log_in_window.title("Log In")

    Label(log_in_window, text="Email:").pack()
    email_entry = Entry(log_in_window)
    email_entry.pack()

    Label(log_in_window, text="Password:").pack()
    password_entry = Entry(log_in_window, show="*")
    password_entry.pack()

    Button(log_in_window, text="Log In", command=submit_login).pack()

# Fungsi untuk membeli barang
def purchase_item(user_email):
    def submit_purchase():
        selected_item = item_var.get()
        price = items[selected_item]
        duration = int(duration_entry.get())

        interest_rate = 0.05
        total_price, monthly_installment = calculate_installment(price, interest_rate, duration)

        # Kirim email pengingat
        subject = "Pengingat Pembelian Barang"
        body = (
            f"Halo,\n\n"
            f"Anda telah membeli {selected_item} dengan harga Rp{price:,.2f}.\n"
            f"Cicilan Anda selama {duration} bulan adalah Rp{monthly_installment:,.2f} per bulan.\n\n"
            f"Harap lakukan pembayaran tepat waktu. Terima kasih!"
        )
        send_email(user_email, subject, body)
        messagebox.showinfo("Success", "Pembelian berhasil!")

    purchase_window = Toplevel(root)
    purchase_window.title("Pembelian Barang")

    Label(purchase_window, text="Pilih Barang:").pack()
    item_var = StringVar()
    item_var.set(list(items.keys())[0])  # Set default item

    item_menu = OptionMenu(purchase_window, item_var, *items.keys())
    item_menu.pack()

    Label(purchase_window, text="Durasi Cicilan (bulan):").pack()
    duration_entry = Entry(purchase_window)
    duration_entry.pack()

    Button(purchase_window, text="Beli", command=submit_purchase).pack()

# Fungsi untuk menu utama
def main():
    global root
    root = Tk()
    root.title("Aplikasi Pembelian Barang")

    Button(root, text="Sign Up", command=sign_up).pack()
    Button(root, text="Log In", command=log_in).pack()
    Button(root, text="Keluar", command=root.quit).pack()

    root.mainloop()

# Fungsi untuk memulai penjadwalan 
# pengingat cicilan di latar belakang
def start_schedule():
    schedule_thread = threading.Thread(target=schedule_reminders)
    schedule_thread.daemon = True
    schedule_thread.start()

if __name__ == "__main__":
    start_schedule()  # Memulai pengingat terjadwal
    main()  # Menjalankan aplikasi utama