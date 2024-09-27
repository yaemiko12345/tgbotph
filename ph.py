import telebot
from pytube import YouTube
import os

# Token bot dari BotFather
API_TOKEN = '7656527709:AAEDaSgfU2fXoc7aZ_Y6R219LK6QNd_ycrI'

# Membuat instance bot
bot = telebot.TeleBot(API_TOKEN)

# Fungsi untuk mengunduh video YouTube
def download_youtube_video(url):
    try:
        yt = YouTube(url)
        # Memilih stream dengan resolusi terendah (360p) untuk memastikan ukuran file kecil
        stream = yt.streams.filter(progressive=True, file_extension='mp4', res="360p").first()
        if stream is None:
            return "Video dengan resolusi yang cocok tidak ditemukan."

        # Mengunduh video ke direktori kerja saat ini
        stream.download()
        return stream.default_filename  # Mengembalikan nama file video yang diunduh
    except Exception as e:
        print(f"Error downloading video: {str(e)}")  # Logging error untuk debugging
        return str(e)

# Handle pesan /start atau /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirim link video YouTube yang ingin Anda unduh.")

# Handle semua pesan yang berisi link YouTube
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    # Memeriksa apakah URL yang dikirim adalah link YouTube
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Sedang mengunduh video, harap tunggu...")
        video_filename = download_youtube_video(url)

        if video_filename.endswith(".mp4"):
            # Mengirim file video ke pengguna
            if os.path.exists(video_filename):
                video_size = os.path.getsize(video_filename) / (1024 * 1024)  # Ukuran dalam MB
                if video_size > 50:
                    bot.reply_to(message, "Maaf, ukuran video melebihi batas 50MB.")
                    os.remove(video_filename)  # Menghapus file video jika terlalu besar
                else:
                    with open(video_filename, 'rb') as video:
                        bot.send_video(message.chat.id, video)
                    os.remove(video_filename)  # Menghapus file video setelah dikirim
            else:
                bot.reply_to(message, f"Gagal mengunduh video: file {video_filename} tidak ditemukan.")
        else:
            bot.reply_to(message, f"Kesalahan saat mengunduh video: {video_filename}")
    else:
        bot.reply_to(message, "Harap kirim link video YouTube yang valid.")

# Menjalankan bot
bot.polling()
