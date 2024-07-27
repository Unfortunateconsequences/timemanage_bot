import os
import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot


BOT_TOKEN = os.getenv(
    'BOT_TOKEN', '6905272038:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

bot = AsyncTeleBot(BOT_TOKEN)
event = asyncio.Event()


async def StartADay(message):
    event.clear()
    time_interval = int(10)
    while not event.is_set():
        await bot.send_message(
            message.chat.id,
            f'Вы начали/продолжаете рабочий день!'
            f'Интервал уведомлений: {time_interval}')
        await asyncio.sleep(time_interval)
        await bot.send_message(
            message.chat.id,
            'Вам пора передохнуть! Бот уходит в сон на 15 минут.')
        await asyncio.sleep(15)


@bot.message_handler(commands=['start'])
async def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Начать рабочий день')
    button2 = telebot.types.KeyboardButton('Закончить рабочий день')
    # button3 = telebot.types.KeyboardButton('')
    # button4 = telebot.types.KeyboardButton('')
    keyboard.row(button1, button2)
    # keyboard.row(button3, button4)
    await bot.send_message(
        message.chat.id,
        'Привет! Выберите кнопку.',
        reply_markup=keyboard
    )


# @bot.message_handler(
#    func=lambda message: message.text == 'Начать рабочий день'
# )
# async def Day_Started(message):
#    task = asyncio.create_task(StartADay(message))


@bot.message_handler(
    func=lambda message: message.text == 'Закончить рабочий день'
)
async def StopADay(message):
    if not event.is_set():
        event.set()
        await bot.send_message(
            message.chat.id,
            'Рабочий день окончен!')
    else:
        await bot.send_message(
            message.chat.id,
            'Вы не начинали рабочий день!')


asyncio.run(bot.polling())
