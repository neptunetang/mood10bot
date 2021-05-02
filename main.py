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

TOKEN = '1694116177:AAFrq-zxQpNEfqUrTo8xlU39mUtwi2aODjk'
URL = "https://data.id.tue.nl/datasets/entity/1145/item/"

HEADERS = {
    'api_token': 'AbTVOcUtsMhJPqWcOPKxp5/kPz7nq/+UBN+YuT3Q988N/URihoXwz69xzxFI5ZRe',
    'resource_id': 'some_identifier',
    'token': 'token_for_identifier'
}


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_message(chatid):
    bot.sendMessage(chatid,
                "Hello, this is a reminder for input: /input, if you have already filled in, please ignore this message! Thank you very much!")


class GoldenArches(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GoldenArches, self).__init__(*args, **kwargs)
        self.indicator = 'registration'
        self.step = 'none'
        self.message = {}
        self.info = {}

    def on_chat_message(self, msg):
        # send_message()

        content_type, chat_type, chat_id = telepot.glance(msg)
        # print(content_type, chat_type, chat_id)
        # print(msg[content_type])
        # t = time.localtime()
        # current_time = time.strftime("%D %H:%M:%S", t)
        # print(current_time)
        self.message['chat_id'] = chat_id

        if self.indicator == 'registration':
            if msg['text'] == '/start':
                flag = True
                for line in open('id.json', 'r'):
                    record = json.loads(line)
                    if record['chatid'] == chat_id:
                        bot.sendMessage(chat_id, 'You are already in the list.')
                        flag = False
                        break
                if flag:
                    mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
                                                  one_time_keyboard=True)
                    bot.sendMessage(chat_id, 'Hi, do you want to register in the test?', reply_markup=mark_up)
                self.step = 'none'
            if msg['text'] == 'yes':
                self.info['chatid'] = chat_id
                mark_up = ReplyKeyboardMarkup(keyboard=[['19:00'], ['19:30'], ['20:00'], ['20:30'], ['21:00']],
                                              one_time_keyboard=True)
                bot.sendMessage(chat_id, "Great, your id is registered!")
                bot.sendMessage(chat_id, "Please choose your preference time in the evening for input",
                                reply_markup=mark_up)
                self.step = 'recordtime'
            elif msg['text'] == 'no':
                bot.sendMessage(chat_id, 'Sorry to hear that. Chat ends.')

            elif self.step == 'recordtime':
                self.info['time'] = msg['text']
                with open('id.json', 'a') as handle:
                    json.dump(self.info, handle)
                    handle.write("\n")
                    handle.close()
                bot.sendMessage(chat_id, "Thank you very much for the input. We will send you a reminder by then. You can also type /input to start your input anytime you want.")
                schedule.every().day.at(self.info["time"]).do(send_message, chatid=chat_id)
                self.step = 'none'
            elif msg['text'] == '/input':
                bot.sendMessage(chat_id, text='Can you send a emoji to represent your day?')
                self.indicator = 'emoji'
        elif self.indicator == 'emoji':
            self.message['emoji'] = msg['text']
            mark_up = ReplyKeyboardMarkup(
                keyboard=[['Not at all'], ['A little bit stressful'], ['Medium level'], ['Very stressful']],
                one_time_keyboard=True)
            bot.sendMessage(chat_id, text='Could you please indicate your stress level?', reply_markup=mark_up)
            self.indicator = 'stress'
        elif self.indicator == 'stress':
            self.message['stress'] = msg['text']
            bot.sendMessage(chat_id,
                            text='Thanks for the input. Do you remember what kind of snacks did you have today? If yes, please specify the name of the snack. If not, please click /no')
            self.indicator = 'snack'
        elif self.indicator == 'snack':
            self.message['snack'] = msg['text']
            bot.sendMessage(chat_id,
                            text='Do you have any comment about your diet today? If not, please click /none')
            self.indicator = 'comment'
        elif self.indicator == 'comment':
            self.message['comment'] = msg['text']
            bot.sendMessage(chat_id,
                            text='Thanks for the input! Do you have any suggestions on the snack bar?(e.g. why (not) try the snack bar? some other kind of snacks?) If not, please click /none')
            self.indicator = 'snackbarsuggest'
        elif self.indicator == 'snackbarsuggest':
            self.message['suggest'] = msg['text']
            #     bot.sendMessage(chat_id, text="Thank you. Can I ask for a picture?")
            #     self.indicator = 'pic'
            # elif self.indicator == 'pic':
            #     file_name = 'pic/' + str(t) + '  ' + str(chat_id) + '.png'
            #     bot.download_file(msg['photo'][-1]['file_id'], file_name)
            #     self.message['picture'] = msg['photo'][-1]['file_id']
            with open('message.json', 'a') as handle:
                json.dump(self.message, handle)
                handle.write("\n")
                handle.close()
            requests.post(url=URL, headers=HEADERS, json=self.message)
            bot.sendMessage(chat_id, 'Message Accepted')
            self.indicator = 'registration'


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GoldenArches, timeout=86400*7),
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
    for line in open('id.json', 'r'):
        print("1")
        record = json.loads(line)
        schedule.every().day.at(record["time"]).do(send_message, chatid=record['chatid'])
    Thread(target=schedule_checker).start()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
