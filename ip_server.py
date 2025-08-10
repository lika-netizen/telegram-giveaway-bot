import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Функция обращения к серверу для проверки лимита по IP
def check_ip_limit():
    url = 'https://ip_server.ru/ip_check'
    try:
        # Отправляем POST-запрос без тела, IP сервер возьмёт из запроса
        response = requests.post(url)
        data = response.json()
        if data.get("allowed", False):
            return True, data.get("count")
        else:
            return False, data.get("count")
    except Exception as e:
        return False, str(e)

# Обработчик команды /register
def register(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_id = update.effective_chat.id

    allowed, info = check_ip_limit()
    if allowed:
        update.message.reply_text(f"Привет, {user.first_name}! Вы успешно зарегистрированы. Текущий счётчик на вашем IP: {info}.")
        # Здесь можно добавить логику добавления пользователя в базу и т.п.
    else:
        update.message.reply_text(f"Извините, регистрация невозможна. Лимит с вашего IP уже достигнут ({info}).")

def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("register", register))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
