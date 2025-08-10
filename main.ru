from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Список для хранения групп (в реале — база данных)
registered_groups = set()

def handle_group_message(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type in ['group', 'supergroup']:
        # Проверяем, что бот админ в группе (можно добавить проверку позже)
        # Запоминаем группу
        registered_groups.add((chat.id, chat.title))
        print(f"Запомнили группу: {chat.title} (ID: {chat.id})")

def main():
    updater = Updater("YOUR_BOT_TOKEN")
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.chat_type.groups, handle_group_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

from telegram.error import BadRequest

def is_user_member(bot, user_id, chat_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        # Проверяем статус
        if member.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except BadRequest:
        return False

# Пример использования
def check_user_subscriptions(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    bot = context.bot

    for group_id, group_title in registered_groups:
        if not is_user_member(bot, user_id, group_id):
            update.message.reply_text(f"Вы должны подписаться на группу {group_title} для участия.")
            return
    update.message.reply_text("Вы подписаны на все группы, участвуете в розыгрыше!")
