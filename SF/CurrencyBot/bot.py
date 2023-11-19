import telebot
from cfg import TOKEN, CURRENCIES
from extensions import APIException, Convertor


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    text = (f"Welcome, {message.chat.username}\n"
            f"Для просмотра доступных к конвертации валют используй /values\n"
            f"Для конвертации нужной валюты отправь сообщение в формате:\n"
            f"<Что сконвертировать> <Во что сконвертировать> <Количество валюты для конвертации>\n"
            f"‼️❗‼️\n"
            f"Например, 'рубль доллар 50' переведет 50 рублей в доллары.\n"
            f"✅✅✅\n"
            f"Пиши наименование валюты в единственном числе, как указано в примере выше⬆️\n"
            f"Ввод количества валюты обязателен.")
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def show_values(message):
    response = 'Доступные валюты:'
    for currency in CURRENCIES.keys():
        response = '\n'.join((response, currency))
    bot.send_message(message.chat.id, response)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        request = message.text.lower().split()

        if len(request) != 3:
            raise APIException('Некорректное число параметров')

        base, quote, amount = request

        response = Convertor.get_price(base, quote, amount)
        bot.send_message(message.chat.id, response)

    except APIException as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла сторонняя ошибка: {e}')


bot.polling(none_stop=True)
