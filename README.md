# Telegram Video Split Bot

Bot Telegram untuk memotong video besar menjadi bagian kecil (maks 99MB) menggunakan FFmpeg. Dijalankan di VPS Google Cloud dan dilengkapi antarmuka dashboard web.

## Fitur
- Terima video sampai 2GB
- Potong otomatis jadi file 99MB MKV
- Kirim kembali ke pengguna
- Antrian proses
- Dashboard real-time

## Deploy ke VPS
```bash
chmod +x deploy_bot.sh
./deploy_bot.sh
```

## Dashboard Web
Akses via: `http://<IP-VPS-ANDA>:5000`
