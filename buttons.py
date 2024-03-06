from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# pick_button_1 = InlineKeyboardButton('Дебетові карти', callback_data='deb_card')
# pick_button_2 = InlineKeyboardButton('Кредитні картки', callback_data='cred_card')
pick_button_3 = InlineKeyboardButton('Позики, кредити', callback_data='get_information')

pick = InlineKeyboardMarkup().add(pick_button_3)

number_button = KeyboardButton('Реєстрація', request_contact=True)
request_number = ReplyKeyboardMarkup(resize_keyboard=True).add(number_button)

next_cards_deb = InlineKeyboardButton('Покажи ще компанії', callback_data='deb_card')
next_cards_cred = InlineKeyboardButton('Покажи ще компанії', callback_data='cred_card')
next_cards_other = InlineKeyboardButton('Покажи ще компанії', callback_data='other')
back_button = InlineKeyboardButton('Покажи інші фінансові продукти', callback_data='start_button')

mmenu = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("До головного меню"))
