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


def remove_button():
    types.ReplyKeyboardRemove()