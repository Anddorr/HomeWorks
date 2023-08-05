from telebot import types


def start_buttons():
    sb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currency_exchange = types.KeyboardButton('Currency exchange')
    sb.add(currency_exchange)
    return sb


def from_or_to():
    ft = types.ReplyKeyboardMarkup(resize_keyboard=True)
    from_UZS = types.KeyboardButton('From UZS')
    to_UZS = types.KeyboardButton('To UZS')
    ft.add(from_UZS, to_UZS)
    return ft


def end_buttons():
    eb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    again = types.KeyboardButton('Again')
    eb.add(again)
    return eb
