import telebot, Lesson17_DBWork as db, Lesson17_Buttons as bt
from geopy import Nominatim

# Connect to bot
bot = telebot.TeleBot('6694535877:AAE4ERdZlUtXdz9l1u98en6Oud5LZYzd8xU')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
users = {}


# Command /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id = message.from_user.id
    # Check
    check_user = db.checker(user_id)
    if check_user:
        bot.send_message(user_id, f'Wellcome {db.return_name(user_id)}!')
        bot.send_message(user_id, 'What next?', reply_markup=bt.purchase_or_help())
        bot.register_next_step_handler(message, purchase_or_help)
    else:
        bot.send_message(user_id, 'Greetings! Start registration, enter your name:', reply_markup=telebot.types.ReplyKeyboardRemove())
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
        bot.send_message(user_id, 'You registered', reply_markup=telebot.types.ReplyKeyboardRemove())
        start_message(message)
    else:
        bot.send_message(user_id, 'Send your location about button')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)


# Function for choosing purchase or help
def purchase_or_help(message):
    if message.text.lower() == 'help':
        bot.send_message(message.from_user.id, 'Help commands:\n'
                                               '/menu - back to menu\n'
                                               '/support - info about support\n'
                                               '/change_name - change your account name\n'
                                               '/change_location - change your account location\n'
                                               '/check_location - check your account location',
                         reply_markup=bt.to_menu())
    elif message.text.lower() == 'start purchase':
        products = db.get_pr_id()
        bot.send_message(user_id, 'Starting purchase', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Choose button on menu', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message('Undefined command', reply_markup=bt.purchase_or_help())


# Function for call support
@bot.message_handler(commands=['support'])
def support_command(message):
    bot.send_message(message.from_user.id, 'Support:\n'
                                           'Contact gmail: TgBot.gmail.com\n'
                                           'Telephone number: +998 90 945 52 40\n')


# Function for change name
@bot.message_handler(commands=['change_name'])
def change_name(message):
    where = 'name'
    bot.send_message(user_id, 'Enter new name:')
    bot.register_next_step_handler(message, save_changes, where)


# Function for change location
@bot.message_handler(commands=['change_location'])
def change_loc(message):
    where = 'location'
    bot.send_message(user_id, 'Enter new location:', reply_markup=bt.loc_button())
    bot.register_next_step_handler(message, save_changes, where)


# Function for saves changes
def save_changes(message, where):
    if where == 'name':
        db.commit_name(message.text, user_id)
    elif where == 'location':
        user_loc = geolocator.reverse(f'{message.location.longitude}, {message.location.latitude}')
        db.commit_loc(user_loc, user_id)
    bot.send_message(user_id, 'Changes commit', reply_markup=bt.to_menu())


# function for back to menu
@bot.message_handler(commands=['menu'])
def back_to_menu(message):
    start_message(message)


# Function for choose amount of product
@bot.callback_query_handler(lambda call: (call.data,) in db.get_pr_name_id())
def get_user_product(call):
    chat_id = call.message.chat.id
    users[chat_id] = {'pr_name': call.data, 'pr_count': 1}
    message_id = call.message.message_id
    bot.edit_message_text('Choose count', chat_id=chat_id, message_id=message_id, reply_markup=bt.choose_product_count())


# Function for choose action with product
@bot.callback_query_handler(lambda call: call.data in ['back', 'to_cart', 'increment', 'decrement'])
def get_user_count(call):
    chat_id = call.message.chat.id
    if call.data == 'increment':
        count = users[chat_id]['pr_count']
        users[chat_id]['pr_count'] += 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=bt.choose_product_count(count, 'increment'))
    elif call.data == 'decrement':
        count = users[chat_id]['pr_count']
        users[chat_id]['pr_count'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.message_id, reply_markup=bt.choose_product_count(count, 'decrement'))
    elif call.data == 'back':
        products = db.get_pr_id()
        bot.edit_message_text('Choose button on menu:', chat_id=chat_id, message_id=call.message.message_id, reply_markup=bt.main_menu_buttons(products))
    elif call.data == 'to_cart':
        products = db.get_pr_id()
        product_count = users[chat_id]['pr_count']
        user_product = users[chat_id]['pr_name']
        user_total = db.return_price(user_product) * product_count
        db.add_to_cart(chat_id, user_product, product_count, user_total)
        bot.edit_message_text('Your product added to cart\nDo you want anything else:', chat_id=chat_id, message_id=call.message.message_id,
                              reply_markup=bt.main_menu_buttons(products))


bot.polling(none_stop=True)