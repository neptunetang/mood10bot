import time
import telepot
import schedule
from threading import Thread
import json
from telepot.loop import MessageLoop
from flask import Flask, request
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup
import requests
import os

TOKEN = '1694116177:AAEj2dOOxmUZLV0d90FCvn8A5f61cwxLh2E'
URL = "https://data.id.tue.nl/datasets/entity/1145/item/"

HEADERS = {
    'api_token': 'AbTVOcUtsMhJPqWcOPKxp5/kPz7nq/+UBN+YuT3Q988N/URihoXwz69xzxFI5ZRe',
    'resource_id':'some_identifier',
    'token': 'token_for_identifier'
}


def send_message():
    for line in open('id.json', 'r'):
        record = json.loads(line)
        bot.sendMessage(record['chat_id'], "hello, this is a reminder for input: \'input")


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


class GoldenArches(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GoldenArches, self).__init__(*args, **kwargs)
        self.indicator = 'record yes/no'
        self.message = {}

    def on_chat_message(self, msg):
        # send_message()

        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id)
        # print(msg[content_type])
        t = time.localtime()
        current_time = time.strftime("%D %H:%M:%S", t)
        # print(current_time)
        self.message['chat_id'] = chat_id
        # self.message['time'] = current_time

        if self.indicator == 'registration':
            if msg['text'] == '/start':
                flag = True
                for line in open('id.json', 'r'):
                    record = json.loads(line)
                    if record['chat_id'] == chat_id:
                        bot.sendMessage(chat_id, 'You are already in the list.')
                        flag = False
                        break

                if flag:
                    mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
                                                  one_time_keyboard=True)
                    bot.sendMessage(chat_id, 'Hi, do you want to register in the test?', reply_markup=mark_up)
                else:
                    self.indicator = 'record yes/no'

            if msg['text'] == 'yes':
                with open('id.json', 'a') as handle:
                    json.dump(self.message, handle)
                    handle.write("\n")
                    handle.close()
                bot.sendMessage(chat_id, "Great, your id is registered!")
                self.indicator = 'record yes/no'
            if msg['text'] == 'no':
                bot.sendMessage(chat_id, 'Sorry to hear that. Chat ends.')

        elif self.indicator == 'record yes/no':
            mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
                                          one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Are you stressful now?', reply_markup=mark_up)
            self.indicator = 'emoji'
        elif self.indicator == 'emoji':
            self.message['stressful'] = msg['text']
            bot.sendMessage(chat_id, text='Ok, thanks for the input. Can you send a emoji?\'ha')
            self.indicator = 'picture'
        elif self.indicator == 'picture':
            self.message['emoji'] = msg['text']
            bot.sendMessage(chat_id, text="Thank you. Can I ask for a picture?")
            self.indicator = 'pic'
        elif self.indicator == 'pic':
            file_name = 'pic/' + str(t) + '  ' + str(chat_id) + '.png'
            bot.download_file(msg['photo'][-1]['file_id'], file_name)
            self.message['picture'] = msg['photo'][-1]['file_id']
            bot.sendMessage(chat_id, text="Do you want to add some comment?")
            self.indicator = 'saysth'
        elif self.indicator == 'saysth':
            self.message['comment'] = msg['text']
            with open('message.json', 'a') as handle:
                json.dump(self.message, handle)
                handle.write("\n")
                handle.close()
            requests.post(url=URL, headers=HEADERS, json=self.message)
            bot.sendMessage(chat_id, 'Message Accepted')
            self.indicator = 'record yes/no'


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GoldenArches, timeout=120),
])
server = Flask(__name__)
MessageLoop(bot).run_as_thread()
print('Listening ...')


# # Keep the program running.
# while 1:
#     time.sleep(10)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://mood10.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    schedule.every().day.at("08:00").do(send_message)
    schedule.every().day.at("14:00").do(send_message)
    schedule.every().day.at("20:00").do(send_message)
    Thread(target=schedule_checker).start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
