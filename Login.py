# Database pengguna (username: password)
users = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

def login():
    print("Selamat datang! Silakan login.")
    
    # Input username dan password dari pengguna
    username = input("Masukkan username: ")
    password = input("Masukkan password: ")
    
    # Memeriksa apakah username ada di database
    if username in users:
        # Memeriksa kecocokan password
        if users[username] == password:
            print("Login berhasil! Selamat datang,", username)
        else:
            print("Password salah. Silakan coba lagi.")
    else:
        print("Username tidak ditemukan. Silakan coba lagi.")

# Menjalankan fungsi login
if __name__ == "_main_":
    login()
    
    # Database pengguna (username: password)
users = {}

def sign_up():
    print("Selamat datang! Silakan daftar akun baru.")
    
    # Input username dari pengguna
    username = input("Masukkan username: ")
    
    # Memeriksa apakah username sudah ada
    if username in users:
        print("Username sudah terdaftar. Silakan pilih username lain.")
        return
    
    # Input password dari pengguna
    password = input("Masukkan password: ")
    
    # Menyimpan username dan password ke dalam database
    users[username] = password
    print("Pendaftaran berhasil! Selamat datang,", username)

# Menjalankan fungsi sign-up
if __name__== "_main_":
    sign_up()