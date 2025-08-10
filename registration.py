import requests

def register_user_on_server(user_id):
    url = 'http://yourserver.com/register'
    data = {'user_id': user_id}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True, response.json().get('message')
        else:
            return False, response.json().get('message')
    except Exception as e:
        return False, str(e)

def handle_registration(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    success, message = register_user_on_server(user_id)

    if success:
        update.message.reply_text(f"Вы успешно зарегистрированы: {message}")
    else:
        update.message.reply_text(f"Ошибка регистрации: {message}")
