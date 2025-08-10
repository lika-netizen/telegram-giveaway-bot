import telebot
from telebot import types
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")  # Установи переменную окружения или вставь токен сюда
bot = telebot.TeleBot(TOKEN)

saved_groups = set()  # Просто для примера, в реальности — база

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.lower() == "/start":
        bot.send_message(message.chat.id, "Привет! Перешли мне сообщение из группы.")
    elif message.forward_from_chat:
        chat = message.forward_from_chat
        chat_id = chat.id
        try:
            member = bot.get_chat_member(chat_id, bot.get_me().id)
            if member.status in ['administrator', 'creator']:
                saved_groups.add(chat_id)
                bot.send_message(message.chat.id, f"Группа сохранена: {chat.title}")
            else:
                bot.send_message(message.chat.id, "Бот должен быть админом в этой группе.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

@bot.message_handler(commands=['participate'])
def participate(message):
    user_id = message.from_user.id
    all_subscribed = True
    for group_id in saved_groups:
        try:
            member = bot.get_chat_member(group_id, user_id)
            if member.status == 'left':
                all_subscribed = False
        except:
            all_subscribed = False

    if not all_subscribed:
        bot.send_message(message.chat.id, "Вы не подписаны на все каналы.")
    else:
        confirm_url = f"https://yourdomain.com/confirm?tg_id={user_id}"
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Подтвердить участие", url=confirm_url)
        markup.add(btn)
        bot.send_message(message.chat.id, "Нажмите для подтверждения участия:", reply_markup=markup)

bot.polling()
