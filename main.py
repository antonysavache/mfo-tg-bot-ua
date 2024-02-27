from typing import Dict

from aiogram import Dispatcher, types, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import cards
from buttons import *
from cards import *
from db import db

bot = Bot(token="6716449345:AAGHMvS4zae8_vxO8YtBANeOHBvMm-NzHIw")
dp = Dispatcher(bot, storage=MemoryStorage())
user_cards: Dict[int, int] = {}


@dp.message_handler(commands=["all"])
async def all_message(message: types.Message):
    if message.from_user.id == 340570808:
        users = db.get_all_users()
        text = message.text.split("/all ")[1]
        for i in users:
            try:
                await bot.send_message(chat_id=i[0], text=text, parse_mode='html')
            except:
                pass


@dp.message_handler(text="До головного меню")
async def back_menu(message: types.Message):
    db.check_record(message.from_user.id)

    user_cards[message.from_user.id] = 0
    text_first = 'База, яка знаходиться у моєму розпорядженні, налічує понад 100 фінансових організацій.'
    text_second = 'Готовий допомогти вам в оформленні позики або взяття кредиту.'
    text_third = 'Уточніть будь ласка, яка послуга вас цікавить?'

    # await bot.send_message(chat_id=message.from_user.id, text=text_first, reply_markup=ReplyKeyboardRemove())
    # await bot.send_message(chat_id=message.from_user.id, text=text_second)
    await bot.send_message(chat_id=message.from_user.id, text=text_third, reply_markup=pick)


@dp.message_handler(commands=["start"])
async def bot_start(message: types.Message):
    db.check_record(message.from_user.id)

    start_button = InlineKeyboardButton("✅ Натиснiть для пiдбору пропозицій", callback_data="start_button")
    start = InlineKeyboardMarkup().add(start_button)
    text = f"Доброго дня! Мене звати Тарас Ботович! Спецiалiст у фiнансовiй сферi."
    await bot.send_photo(chat_id=message.from_user.id, photo=open('images/start.png', 'rb'), caption=text, parse_mode='html', reply_markup=start)


@dp.callback_query_handler()
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "start_button":
        user_cards[callback.from_user.id] = 0
        text_first = 'База, яка знаходиться у моєму розпорядженні, налічує понад 100 фінансових організацій.'
        text_second = 'Готовий допомогти вам в оформленні позики або взяття кредиту.'
        text_third = 'Уточніть будь ласка, яка послуга вас цікавить?'

        # await bot.send_message(chat_id=callback.from_user.id, text=text_first)
        # await bot.send_message(chat_id=callback.from_user.id, text=text_second)
        await bot.send_message(chat_id=callback.from_user.id, text=text_third, reply_markup=pick)

    if callback.data == "deb_card":
        text = 'Ось, що вдалося знайти за Вашим запитом. Будь ласка, ознайомтесь: '
        await bot.send_message(chat_id=callback.from_user.id, text=text, reply_markup=mmenu)

        current = user_cards.get(callback.from_user.id)
        if current is None:
            current = 0

        kb = InlineKeyboardMarkup().add(next_cards_deb)

        if len(cards["deb_cards"]) - current > 3:
            plus = 3
        else:
            plus = len(cards["deb_cards"]) - current

        for i in range(current, current+plus):
            text = cards["deb_cards"][i+1]['text']
            await bot.send_photo(chat_id=callback.from_user.id, photo=open(cards['deb_cards'][i+1]['img'], 'rb'), caption=text, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Перейти до оформлення', url=cards["deb_cards"][i+1]['url'])
            ), parse_mode='html')

        user_cards[callback.from_user.id] = current + plus
        if len(cards["deb_cards"]) == current + plus:
            user_cards[callback.from_user.id] = 0
            kb = InlineKeyboardMarkup().add(back_button)
        end_text = 'Чи хочете Ви переглянути інші компанії з бази?'
        await bot.send_message(chat_id=callback.from_user.id, text=end_text, reply_markup=kb)

    if callback.data == "cred_card":
        text = 'Ось, що вдалося знайти за Вашим запитом. Будь ласка, ознайомтесь: '
        await bot.send_message(chat_id=callback.from_user.id, text=text, reply_markup=mmenu)

        current = user_cards.get(callback.from_user.id)
        if current is None:
            current = 0

        kb = InlineKeyboardMarkup().add(next_cards_cred)

        if len(cards["cred_cards"]) - current > 3:
            plus = 3
        else:
            plus = len(cards["cred_cards"]) - current

        for i in range(current, current+plus):
            text = cards["cred_cards"][i+1]['text']
            await bot.send_photo(chat_id=callback.from_user.id, photo=open(cards['cred_cards'][i+1]['img'], 'rb'), caption=text, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Перейти до оформлення', url=cards["cred_cards"][i+1]['url'])
            ), parse_mode='html')

        user_cards[callback.from_user.id] = current + plus
        if len(cards["cred_cards"]) == current + plus:
            user_cards[callback.from_user.id] = 0
            kb = InlineKeyboardMarkup().add(back_button)
        end_text = 'Чи хочете Ви переглянути інші компанії з бази?'
        await bot.send_message(chat_id=callback.from_user.id, text=end_text, reply_markup=kb)


    if callback.data == "other":
        text = 'Ось, що вдалося знайти за Вашим запитом. Будь ласка, ознайомтесь: '
        await bot.send_message(chat_id=callback.from_user.id, text=text, reply_markup=mmenu)

        current = user_cards.get(callback.from_user.id)
        if current is None:
            current = 0

        kb = InlineKeyboardMarkup().add(next_cards_other)

        if len(cards["other"]) - current > 3:
            plus = 3
        else:
            plus = len(cards["other"]) - current

        for i in range(current, current+plus):
            text = cards["other"][i+1]['text']
            await bot.send_photo(chat_id=callback.from_user.id, photo=open(cards['other'][i+1]['img'], 'rb'), caption=text, reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Перейти до оформлення', url=cards["other"][i+1]['url'])
            ), parse_mode='html')

        user_cards[callback.from_user.id] = current+plus
        if len(cards["other"]) == current + plus:
            user_cards[callback.from_user.id] = 0

            kb = InlineKeyboardMarkup().add(back_button)
        end_text = 'Чи хочете Ви переглянути інші компанії з бази?'
        await bot.send_message(chat_id=callback.from_user.id, text=end_text, reply_markup=kb)

    if callback.data == "get_information":
        f_button = InlineKeyboardButton("Бiльщ нiж 20.000 грн", callback_data='pass')
        s_button = InlineKeyboardButton("До 20.000 грн", callback_data='pass')

        kb = InlineKeyboardMarkup().add(f_button).add(s_button)
        await bot.send_message(callback.from_user.id, text="Яка грошова сума Вас цікавить?", reply_markup=kb)

    if callback.data == "pass":
        f_button = InlineKeyboardButton("Завжди відмовляють", callback_data='other')
        s_button = InlineKeyboardButton("Відмов не було", callback_data='other')
        th_button = InlineKeyboardButton("Іноді", callback_data='other')

        kb = InlineKeyboardMarkup().add(f_button).add(s_button).add(th_button)
        await bot.send_message(callback.from_user.id, text="Ви отримували раніше відмови у оформленні позики чи видачі кредиту?", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
