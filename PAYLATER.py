
# Simulasi database pengguna dan pembayaran
users = [
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "+1234567890",  # Format nomor internasional
        "paylater_due_date": datetime(2024, 11, 28),  # Tanggal jatuh tempo
        "amount_due": 500.00  # Jumlah yang harus dibayar
    },
    # Tambahkan lebih banyak pengguna jika diperlukan
]

# Fungsi untuk mengirim email pengingat
def send_email(to_email, subject, body):
    sender_email = "your_email@example.com"
    sender_password = "your_password"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, message)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Fungsi untuk mengirim pesan WhatsApp
def send_whatsapp(to_phone, message):
    account_sid = "your_twilio_account_sid"
    auth_token = "your_twilio_auth_token"
    from_whatsapp_number = "whatsapp:+14155238886"  # Twilio WhatsApp sandbox number

    client = Client(account_sid, auth_token)
    try:
        client.messages.create(
            from_=from_whatsapp_number,
            to=f"whatsapp:{to_phone}",
            body=message
        )
        print(f"WhatsApp message sent to {to_phone}")
    except Exception as e:
        print(f"Failed to send WhatsApp message to {to_phone}: {e}")

# Fungsi untuk memeriksa pembayaran yang jatuh tempo dan mengirim pengingat
def check_and_notify():
    today = datetime.now()
    for user in users:
        due_date = user["paylater_due_date"]
        if due_date - today <= timedelta(days=3):  # Pengingat 3 hari sebelum jatuh tempo
            subject = f"Pengingat Pembayaran PayLater untuk {user['name']}"
            body = (f"Halo {user['name']},\n\n"
                    f"Ini adalah pengingat bahwa pembayaran PayLater Anda sebesar "
                    f"${user['amount_due']} akan jatuh tempo pada {due_date.strftime('%Y-%m-%d')}.\n"
                    "Harap pastikan pembayaran Anda dilakukan tepat waktu untuk menghindari denda.\n\n"
                    "Terima kasih.")
            send_email(user["email"], subject, body)
            send_whatsapp(
                user["phone"],
                f"Halo {user['name']}, pembayaran PayLater sebesar ${user['amount_due']} akan jatuh tempo pada {due_date.strftime('%Y-%m-%d')}."
            )

# Jalankan fungsi pengingat
if __name__ == "_main_":
    check_and_notify()