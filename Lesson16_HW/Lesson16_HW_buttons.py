from telebot import types


def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    num = types.KeyboardButton('Send number', request_contact=True)
    kb.add(num)
    return kb


def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    loc = types.KeyboardButton('Send location', request_location=True)
    kb.add(loc)
    return kb


def main_menu_buttons(products_from_db):
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Create permanent buttons
    cart = types.InlineKeyboardButton(text='Cart', callback_data='cart')
    # Create products buttons
    all_products = [types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[2]}') for i in products_from_db]
    kb.row(cart)
    kb.add(*all_products)
    return kb


def remove_button():
    types.ReplyKeyboardRemove()