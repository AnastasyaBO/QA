import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    start_text = "Для того чтобы перевести валюту, используйте следующий формат:\n <название валюты> <название валютыв котороую хотите перевести> <колличество переводимой валюты>\nЧтобы узнать доступные валюты нажмите --> /values"
    bot.reply_to(message, f'Привет, {message.chat.username}! \n\n{start_text}')


@bot.message_handler(commands=['values'])
def handler_values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot .reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров.")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.send_message(message, f"Не удалось обработать команду \n{e}")
    else:
        summ_ = total_base * int(amount)
        text = f"Цена {amount} {quote} в {base} - {summ_}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)