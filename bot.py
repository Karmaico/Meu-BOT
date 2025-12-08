import telebot
from telebot import types
import random
import os
import yt_dlp

# =========================
# CONFIGURAÇÕES
# =========================
TELEGRAM_TOKEN ="8539746186:AAEbpwMA2UEMyOdLRUVrdkY2FYpQsfBGsPk"

bot = telebot.TeleBot(8539746186:AAEbpwMA2UEMyOdLRUVrdkY2FYpQsfBGsPk)

# =========================
# /start
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱 Gerar Número", callback_data="gerar"))
    markup.add(types.InlineKeyboardButton("🎬 Baixar YouTube", callback_data="baixar"))
    markup.add(types.InlineKeyboardButton("🌐 Redes Sociais", callback_data="redes"))

    texto = (
        "Olá! Sou bot do Karmaico me chamo Togi🌖 Fushiguro.\n"
        "Eu posso fazer várias coisas:\n\n"
        "Escolha uma opção abaixo 👇"
    )
    bot.send_message(message.chat.id, texto, reply_markup=markup)

# =========================
# Callback de botões
# =========================
@bot.callback_query_handler(func=lambda call: True)
def callback_buttons(call):
    if call.data == "gerar":
        gerar_numero(call.message)
    elif call.data == "baixar":
        bot.send_message(call.message.chat.id, "Digite:\n/baixar LINK_DO_YOUTUBE")
    elif call.data == "redes":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("YouTube", url="https://youtube.com/@karmaico7k"))
        markup.add(types.InlineKeyboardButton("TikTok", url="https://www.tiktok.com/@karmaico.007"))
        bot.send_message(call.message.chat.id, "🌐 Siga minhas redes sociais 👇", reply_markup=markup)

# =========================
# /gerar - número BR + formatação nova
# =========================
def gerar_numero(message):
    ddd = random.choice([
        11,12,13,14,15,16,17,18,19,
        21,22,24,27,28,31,32,33,34,35,37,38,
        41,42,43,44,45,46,47,48,49,
        51,53,54,55,
        61,62,63,64,65,66,67,68,69,
        71,73,74,75,77,79,
        81,82,83,84,85,86,87,88,89,
        91,92,93,94,95,96,97,98,99
    ])

    parte1 = random.randint(1000, 9999)
    parte2 = random.randint(1000, 9999)

    numero = f"+55 {ddd} 9{parte1}-{parte2}"

    bot.send_message(
        message.chat.id,
        f"📱 Número aleatório gerado:\n`{numero}`",
        parse_mode="Markdown"
    )

# =========================
# /baixar - baixar vídeo usando yt-dlp
# =========================
@bot.message_handler(commands=['baixar'])
def baixar_video(message):
    link = message.text.replace("/baixar", "").strip()

    if not link:
        bot.send_message(message.chat.id, "⚠️ Envie assim:\n/baixar LINK_DO_YOUTUBE")
        return

    bot.send_message(message.chat.id, "⏳ Baixando, aguarde...")

    try:
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'video.mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        with open("video.mp4", "rb") as f:
            bot.send_video(message.chat.id, f)

        os.remove("video.mp4")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Erro ao baixar vídeo:\n{e}")

# =========================
# Iniciar bot
# =========================
bot.polling()
