import telebot, DBWork as db, Buttons as bt
from geopy import Nominatim

# Connect to bot
bot = telebot.TeleBot('6694535877:AAE4ERdZlUtXdz9l1u98en6Oud5LZYzd8xU')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')


# Command /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id = message.from_user.id
    # Check
    check_user = db.checker(user_id)
    if check_user:
        products = db.get_pr_id()
        bot.send_message(user_id, f'Wellcome{db.return_name(user_id)}!', reply_markup=bt.remove_button())
        bot.send_message(user_id, 'Choose button on menu', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Greetings! Start registration, enter your name:', reply_markup=bt.remove_button())
        bot.register_next_step_handler(message, get_name)


# Collect name
def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Enter your num!', reply_markup=bt.num_button())
    bot.register_next_step_handler(message, get_num, user_name)


def get_num(message, user_name):
    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'Now send location: ', reply_markup=bt.loc_button())
        bot.register_next_step_handler(message, get_loc, user_name, user_num)
    else:
        bot.send_message(user_id, 'Send your contact about button!')
        bot.register_next_step_handler(message, get_num, user_name)


def get_loc(message, user_name, user_num):
    if message.location:
        user_loc = geolocator.reverse(f'{message.location.longitude}, {message.location.latitude}')
        db.registration(user_id, user_name, user_num, user_loc)
        bot.send_message(user_id, 'You registered', reply_markup=bt.remove_button())
        start_message(message)
    else:
        bot.send_message(user_id, 'Send your location about button')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.from_user.id, 'Help commands:\n'
                                           '/support - info about support\n'
                                           '/change_name - change your account name\n'
                                           '/change_location - change your account location\n'
                                           '/check_location - check your account location')


@bot.message_handler(commands=['support'])
def support_command(message):
    bot.send_message(message.from_user.id, 'Support:\n'
                                           'Contact gmail: TgBot.gmail.com\n'
                                           'Telephone number: +998 90 945 52 40\n')


@bot.message_handler(commands=['change_name'])
def change_name(message):
    where = 'name'
    bot.send_message(user_id, 'Enter new name:')
    bot.register_next_step_handler(message, save_changes, where)


@bot.message_handler(commands=['change_location'])
def change_loc(message):
    where = 'location'
    bot.send_message(user_id, 'Enter new location:', reply_markup=bt.loc_button())
    bot.register_next_step_handler(message, save_changes, where)


def save_changes(message, where):
    if where == 'name':
        db.commit_name(message.text, user_id)
    elif where == 'location':
        user_loc = geolocator.reverse(f'{message.location.longitude}, {message.location.latitude}')
        db.commit_loc(user_loc, user_id)
    bot.send_message(user_id, 'Changes commit')
    start_message(message)


bot.polling(none_stop=True)