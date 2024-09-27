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
        yt = YouTube(url)  # Inisialisasi YouTube object
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        stream.download()  # Mengunduh video ke direktori saat ini
        return stream.default_filename  # Mengembalikan nama file video yang diunduh
    except Exception as e:
        return str(e)  # Mengembalikan pesan error jika terjadi kesalahan

# Handle pesan /start atau /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Kirim link video YouTube yang ingin Anda unduh.")

# Handle semua pesan yang berisi link YouTube
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        bot.reply_to(message, "Sedang mengunduh video, harap tunggu...")
        video_filename = download_youtube_video(url)
        
        if os.path.exists(video_filename):
            # Mengirim file video ke pengguna
            with open(video_filename, 'rb') as video:
                bot.send_video(message.chat.id, video)
            
            # Menghapus video setelah dikirim
            os.remove(video_filename)
        else:
