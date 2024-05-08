import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters
import datetime
import pytz
import random

TOKEN = '7180060176:AAEALEVZhZNz1iE-1c9ltSUsLz2stbNHycQ'  # Замените на ваш токен от BotFather

# Глобальные переменные для хранения информации о текущем Гапо
GAP_FILE = 'gapo_state.json'

def save_gapo_state(state):
    with open(GAP_FILE, 'w') as file:
        json.dump(state, file)

def load_gapo_state():
    try:
        with open(GAP_FILE, 'r') as file:
            data = json.load(file)
            current_gapo = data.get('current_gapo')
            gapo_expiry_str = data.get('gapo_expiry')
            if gapo_expiry_str:
                try:
                    gapo_expiry = datetime.datetime.fromisoformat(gapo_expiry_str)
                except ValueError:
                    gapo_expiry = datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))
            else:
                gapo_expiry = datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))
            return current_gapo, gapo_expiry
    except (FileNotFoundError, json.JSONDecodeError):
        return None, datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))


current_gapo, gapo_expiry = load_gapo_state()

if not gapo_expiry:
    gapo_expiry = datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))

# Список ответных сообщений, когда уже есть Гапо
gapo_messages = [
    "Настоящий Гапо уже выбран. Не пизди, иди на хуй. Настоящий Гапо: {gapo_name}.",
    "Гапо уже есть, не старайся зря. Сейчас это {gapo_name}.",
    "Кто-то опоздал, Гапо уже в деле! А Гапо сегодня - {gapo_name}.",
    "Уже выбрали Гапо, не твой день сегодня. Гапо сейчас {gapo_name}.",
    "Гапо занят, приходи завтра. Текущий Гапо: {gapo_name}.",
    "Забудь, Гапо уже на месте, не твоё это. Гапо сегодня - {gapo_name}."
]

images = [
    "AgACAgQAAx0Cf3oOeAACCTJmOiGqQ47Sz2fnSFCoTXdSYNJ6xQACq8IxGztc0FFoEVQkF1RxkwEAAwIAA3kAAzUE",
    "AgACAgQAAx0Cf3oOeAACCTNmOiHCwEyUizq0XyteO2T5ZHrL_gACrMIxGztc0FH3ZyY0kol9IwEAAwIAA3kAAzUE",
    "AgACAgQAAx0Cf3oOeAACCTRmOiHHyrnuL5d8F1bOAgaQQhfNgAACrcIxGztc0FFmBCD7Ei2woAEAAwIAA3kAAzUE",
    "AgACAgQAAx0CWtGW8QAC1LlmOiIEX0N1mmj_0tQM0dnLY1MKOgAC87MxG5NGzFGoX9GUYFkXRQEAAwIAA3cAAzUE",
    "AgACAgQAAx0CWtGW8QAC1LpmOiIJ2JPTXX3knNhNe6OgDYDGFwACba4xGyicxVM_z6xXOthPvQEAAwIAA3kAAzUE",
    "AgACAgQAAx0CWtGW8QAC1LtmOiINm9cV2iHD4eEPRQdpoG_ZogACRa8xG6sanVJuwoAaHEEClgEAAwIAA3cAAzUE",
    "AgACAgQAAx0CWtGW8QAC1LxmOiIUgtifBoj8cxhKzGYHtLig3gACbLIxGwsynFAlaTdWIBvRlwEAAwIAA3cAAzUE",
    "AgACAgIAAx0CWtGW8QAC1MtmOiLBMi8tbmlPhQABdsDHxGBuPx4AAgWtMRul1vlLjo9VJ2gsfGABAAMCAAN5AAM1BA",
    "AgACAgQAAx0CWtGW8QAC1L9mOiIkeCr68e2ktiW-dB8zCoSV5wACFbMxG6htNFCjDMc3ZbbppwEAAwIAA3cAAzUE",
    "AgACAgQAAx0CWtGW8QAC1MJmOiI3uL-lBLPfgdXbB9HF-WXfTAACga8xGxN23FEgBGxL8LKH_AEAAwIAA3kAAzUE",
]

# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1L9mOiIkeCr68e2ktiW-dB8zCoSV5wACFbMxG6htNFCjDMc3ZbbppwEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MBmOiIpAbB-Qj6neDuLj3LPeudeuQACKa8xGximfVJdNQUHipNrCgEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MFmOiIveaau0Qv71YCGXSA_k2ow8wACgK4xG9MZbFLJWHXKAULc7QEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MJmOiI3uL-lBLPfgdXbB9HF-WXfTAACga8xGxN23FEgBGxL8LKH_AEAAwIAA3kAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MNmOiI8Hbf1MkckmivrhlsbYR3s1wAClK8xG8qThFOQ9DBJ9SVd7AEAAwIAA3kAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MRmOiI_18Jh38utbHjOdpnQ8g7NRQAClq8xGxe-jVC7hdYMRQVU5QEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MVmOiJEj-G0X3LLjveMZJWbIh0UhwACYa8xG2idpFJhkYZj4XH07wEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MZmOiJN7eAJFwPLsgSBJ_AHrPDVnAACy64xG4WYjFJkrPzTlRv6kgEAAwIAA3cAAzUE
# Received photo with file_id: AgACAgQAAx0CWtGW8QAC1MdmOiJa-bbuTSYhBj2HIuFO6hoAAT8AAgWuMRsFJkVTUsFCSE-Y6DABAAMCAAN3AAM1BA
labels_dict = {}
async def handle_message(update: Update, context):
    global current_gapo, gapo_expiry
    user = update.effective_user
    chat_id = update.effective_chat.id
    now = datetime.datetime.now(pytz.timezone('Asia/Yekaterinburg'))
    message_text = update.effective_message.text

    # Проверяем, не истекло ли время Гапо
    if now >= gapo_expiry:
        current_gapo = None

    if 'кто гапо?' in message_text.lower():
        if current_gapo:
            await context.bot.send_photo(chat_id=chat_id, photo=random.choice(images), caption=f"Сейчас Гапо - {current_gapo}.")
        else:
            await context.bot.send_message(chat_id=chat_id, text="Гапо еще не выбран.")
        return

    # Проверяем, является ли сообщение текстовым и не командой
    if message_text and not message_text.startswith('/'):
        if 'я гапо кста' in message_text.lower():
            if current_gapo:
                # Отправляем одно из заранее подготовленных сообщений, если Гапо уже выбран
                response_message = random.choice(gapo_messages).format(gapo_name=current_gapo)
                await context.bot.send_photo(chat_id=chat_id, photo=random.choice(images), caption=response_message)
            else:
                # Назначаем нового Гапо
                if user.username == 'GACHIBOYCHIK':
                    await context.bot.send_message(chat_id=chat_id, text="Тебе не быть гапо, иди нахуй.")
                current_gapo = user.first_name
                gapo_expiry = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
                save_gapo_state({'current_gapo': current_gapo, 'gapo_expiry': gapo_expiry.isoformat()})
                message = f"{user.first_name} теперь Гапо до {gapo_expiry.strftime('%Y-%m-%d %H:%M:%S')}"
                await context.bot.send_photo(chat_id=chat_id, photo=random.choice(images), caption=message)

async def handle_photo(update: Update, context):
    photo_file_id = update.effective_message.photo[-1].file_id  # Последний элемент списка - самое большое изображение
    print(f"Received photo with file_id: {photo_file_id}")

def main():
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик текстовых сообщений
    message_handler = MessageHandler(filters.TEXT, handle_message)
    photo_handler = MessageHandler(filters.PHOTO, handle_photo)
    application.add_handler(message_handler)
    application.add_handler(photo_handler)

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()