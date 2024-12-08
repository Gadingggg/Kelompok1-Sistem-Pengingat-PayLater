# KELOMPOK 1 KELAS C

## Kelas : C
## Kelompok : 1
## Anggota :
- I0324110 Agung Rizkianto (AGUNGRIZKIANTO)
- I0324121 Novan Gading Krisniawidhi (Gadingggg)
- I0324134 Raditya Hilmy Hariyanto (RadityaHilmy)

## Tema : Sistem Pengingat PayLater
## Deskripsi :
Sistem pengingat PayLater adalah sebuah aplikasi atau layanan digital yang dirancang untuk membantu pengguna mengelola kewajiban pembayaran cicilan paylater (bayar nanti). Sistem ini berfokus pada pengelolaan jadwal pembayaran, pengiriman notifikasi, serta pengelolaan informasi transaksi terkait paylater. Sistem ini memiliki tujuan untuk memberikan pemberitahuan kepada pengguna mengenai jadwal pembayaran cicilan paylater sebelum jatuh tempo. menghindari keterlambatan pembayaran yang dapat menyebabkan denda atau penalti. meningkatkan kesadaran pengguna terhadap status kewajiban finansialnya.

## Alur Kerja Sistem :
1. Aplikasi dimulai, dengan gambar latar belakang ditampilkan.
2. Pengguna memilih untuk Sign Up atau Log In.
   Sign Up: Pengguna mengisi data diri, dan jika valid, data tersebut disimpan dan pengguna berhasil mendaftar.
   Log In: Pengguna memasukkan email dan kata sandi. Jika cocok, pengguna masuk ke dashboard.
3. Dashboard menampilkan produk yang diambil dari file CSV. Pengguna dapat memilih produk dan melanjutkan ke halaman pembayaran.
4. Pembayaran: Pengguna memilih metode pembayaran dan durasi cicilan.
5. Pengingat Pembayaran: Secara otomatis dikirimkan melalui email kepada pengguna setiap minggu.

## Fitur yang tersedia : 
1. Pendaftaran Pengguna (Sign Up) – Pengguna dapat mendaftar dengan email, nama, dan kata sandi.
2. Login Pengguna – Pengguna dapat login menggunakan email dan kata sandi yang terdaftar.
3. Dashboard Produk – Menampilkan daftar produk dengan harga dan gambar.
4. Pembelian Produk – Pengguna dapat memilih produk dan metode pembayaran (termasuk cicilan).
5. Pengingat Cicilan – Pengguna menerima pengingat pembayaran cicilan melalui email.
6. Keamanan Data – Kata sandi disimpan dalam bentuk hash untuk keamanan.
7. Antarmuka Grafis – Aplikasi menggunakan antarmuka berbasis Tkinter dengan tombol dan menu.
8. Metode Pembayaran – Beragam opsi pembayaran seperti kartu kredit dan e-wallet.
9. Fitur Keluar – Tombol untuk keluar dari aplikasi kapan saja.

![_Flowchart Pengingat PayLater  drawio (3)](https://github.com/user-attachments/assets/5c07c9f7-9d40-46f5-b278-4078ce1a50f3)

## Cara Menggunakan :
1) Registrasi 
   - Registrasi: ada jendela utama, klik tombol Sign Up.
   - Jendela baru akan terbuka untuk mengisi form pendaftaran dengan informasi berikut:
     1. Email: Masukkan email yang valid.
     2. Nama: Masukkan nama lengkap.
     3. Kata Sandi: Masukkan kata sandi yang diinginkan.
     4. Konfirmasi Kata Sandi: Masukkan kata sandi yang sama untuk konfirmasi.
     5. Klik tombol Sign Up setelah semua form diisi.
     6. Jika format email tidak valid, aplikasi akan memberi pesan kesalahan.
     7. Jika kata sandi tidak cocok, aplikasi akan memberi pesan kesalahan.
     8. Jika email sudah terdaftar, aplikasi juga akan memberi pesan kesalahan.
     9. Jika semua validasi berhasil, akun akan dibuat dan aplikasi akan memberi notifikasi Akun berhasil dibuat.
2) Login Pengguna
   - Pada jendela utama, klik tombol Log In.
   - Jendela login baru akan muncul dengan dua kolom input:
      1. Email: Masukkan email yang sudah terdaftar.
      2. Kata Sandi: Masukkan kata sandi yang terdaftar.
      3. Klik tombol Log In setelah mengisi form login.
      4. Jika email atau kata sandi salah, aplikasi akan memberi pesan kesalahan.
      5. Jika login berhasil, aplikasi akan menampilkan jendela dashboard yang berisi daftar produ
3) Melihat Produk di Dashboard
  - Setelah login, jendela Dashboard akan terbuka.
  - Di sini, Anda akan melihat daftar produk Samsung yang tersedia.
  - Setiap produk akan ditampilkan dengan gambar (jika ada) dan harga.
  - Anda dapat memilih produk dengan mengklik tombol di bawah nama produk.
4) Pembelian Produk
  - Setelah memilih produk, jendela baru akan terbuka untuk proses pembayaran.
  - Di sini Anda harus mengisi informasi berikut:
    1. Durasi Cicilan: Tentukan durasi pembayaran cicilan (jika membeli dengan cicilan).
    2. Metode Pembayaran: Pilih salah satu metode pembayaran yang tersedia (misalnya BCA, GoPay, BRI, dll.).
    3. Klik tombol Lanjutkan untuk melanjutkan proses pembelian atau keluar menggunakan tombol Keluar.
5) Menerima Pengingat Pembayaran Cicilan
 - Sistem ini secara otomatis mengirimkan email kepada pengguna yang memiliki cicilan yang harus dibayar.
6) Menutup Aplikasi
  - Setiap jendela aplikasi memiliki tombol Keluar di bagian bawah untuk menutup jendela tersebut dan keluar dari aplikasi.



