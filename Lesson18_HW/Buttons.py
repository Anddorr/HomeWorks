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


def purchase_or_help():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    purchases = types.KeyboardButton('Start purchase')
    help = types.KeyboardButton('Help')
    kb.add(purchases, help)
    return kb


def to_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu = types.KeyboardButton('/menu')
    help = types.KeyboardButton('/help')
    kb.add(menu, help)
    return kb


def main_menu_buttons(products_from_db):
    kb = types.InlineKeyboardMarkup(row_width=3)
    # Create permanent buttons
    cart = types.InlineKeyboardButton(text='Cart', callback_data='cart')
    # Create products buttons
    all_products = [types.InlineKeyboardButton(text=f'{i[0]}', callback_data=f'{i[0]}') for i in products_from_db]
    kb.row(cart)
    kb.add(*all_products)
    return kb


# Choose count of product
def choose_product_count(amount=1, plus_or_minus=''):
    kb = types.InlineKeyboardMarkup(row_width=3)
    back = types.InlineKeyboardButton(text='Back', callback_data='back')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))
    add_to_cart = types.InlineKeyboardButton(text='Add into cart', callback_data='to_cart')
    if plus_or_minus == 'increment':
        new_amount = int(amount) + 1
        count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    kb.add(minus, count, plus)
    kb.row(back, add_to_cart)
    return kb


# Button for cart
def cart_button():
    kb = types.InlineKeyboardMarkup(row_width=3)
    order = types.InlineKeyboardButton(text='Send an order', callback_data='order')
    clear = types.InlineKeyboardButton(text='Clear cart', callback_data='clear')
    back = types.InlineKeyboardButton(text='Back', callback_data='back')
    kb.add(order)
    kb.add(back, clear)
    return kb