import logging
from aiogram import (Bot, Dispatcher, executor, types)
from config import BOT_TOKEN
from voice import get_voices, text_to_speech

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Хранилище голосов
voices = get_voices()


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    """
    Приветственное сообщение и выбор голоса
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for voice_name in voices.keys():
        keyboard.add(voice_name)
    await message.answer("Привет! Выбери голос для озвучки:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text in voices.keys())
async def voice_selected(message: types.Message):
    """
    Пользователь выбрал голос
    """
    selected_voice = message.text
    # Сохраним выбор в user_data
    await message.answer(f"Голос *{selected_voice}* выбран ✅\nТеперь пришли мне текст для озвучки.", parse_mode="Markdown")
    dp.current_state(user=message.from_user.id).voice = voices[selected_voice]


@dp.message_handler(content_types=["text"])
async def text_to_voice(message: types.Message):
    """
    Генерация озвучки из текста
    """
    user_state = dp.current_state(user=message.from_user.id)
    voice_id = getattr(user_state, "voice", None)

    if not voice_id:
        await message.answer("Сначала выбери голос с помощью клавиатуры ниже 👇")
        return

    await message.answer("⏳ Генерирую озвучку...")

    try:
        audio_data = text_to_speech(message.text, voice_id)

        # Отправляем пользователю аудио как voice
        await bot.send_voice(
            chat_id=message.chat.id,
            voice=audio_data,
            caption="Готово ✅"
        )

    except Exception as e:
        await message.answer(f"Ошибка при генерации: {e}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)