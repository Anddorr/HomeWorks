import json, telebot, requests, Buttons as bt
bot = telebot.TeleBot('5268293106:AAH5SmdhhfXmBpyb9yW0AG2QCobmPOriUQM') # @testkhnbot - bot id


def toFixed(numObj):
    return f"{numObj:.{2}f}"


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Wellcome in Currency exchange!', reply_markup=bt.start_buttons())


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'currency exchange' or message.text.lower() == 'again':
        bot.send_message(message.from_user.id, 'Exchange from UZS or to UZS', reply_markup=bt.from_or_to())
        bot.register_next_step_handler(message, exchanger)
    else:
        bot.send_message(message.from_user.id, 'Unknown command')
        bot.register_next_step_handler(message, answer)


def exchanger(message):
    if message.text.lower() == 'from uzs':
        bot.send_message(message.from_user.id, 'To which currency(Example:USD):')
        bot.register_next_step_handler(message, from_uzs)
    elif message.text.lower() == 'to uzs':
        bot.send_message(message.from_user.id, 'From which currency(Example:USD):')
        bot.register_next_step_handler(message, to_uzs)
    else:
        bot.send_message(message.from_user.id, 'Unknown command')
        bot.register_next_step_handler(message, answer)


def from_uzs(message):
    currency = message.text.upper()
    bot.send_message(message.from_user.id, 'Enter quality of UZS:')
    bot.register_next_step_handler(message, result_from, currency)


def result_from(message, currency):
    link = f"https://cbu.uz/ru/arkhiv-kursov-valyut/json/{currency}/"
    info = json.loads(requests.post(url=link).text)
    rate = info[0]['Rate']
    result = float(int(message.text) / float(rate))
    bot.send_message(message.from_user.id, f'Result: {toFixed(result)} {info[0]["CcyNm_EN"]}\nWhat next:', reply_markup=bt.end_buttons())
    bot.register_next_step_handler(message, answer)


def to_uzs(message):
    currency = message.text.upper()
    bot.send_message(message.from_user.id, f'Enter quality of {message.text}:')
    bot.register_next_step_handler(message, result_to, currency)


def result_to(message, currency):
    link = f"https://cbu.uz/ru/arkhiv-kursov-valyut/json/{currency}/"
    info = json.loads(requests.post(url=link).text)
    rate = info[0]['Rate']
    result = float(int(message.text) * float(rate))
    bot.send_message(message.from_user.id, f'Result: {toFixed(result)} UZS\nWhat next:', reply_markup=bt.end_buttons())
    bot.register_next_step_handler(message, answer)


bot.polling(none_stop=True)