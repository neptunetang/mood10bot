# import time
# import telepot
# import schedule
# from threading import Thread
# import json
# from telepot.loop import MessageLoop
# from flask import Flask, request
# from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
# from telepot.delegate import pave_event_space, per_chat_id, create_open
# from telepot.namedtuple import ReplyKeyboardMarkup
# import requests
# import os
# from datetime import datetime
#
# TOKEN = '1694116177:AAEr9gLPK__8YNLUx9KAsRZ1gEHwG4qzkqU'
# URL = "https://data.id.tue.nl/datasets/entity/1145/item/"
# # URL = "https://data.id.tue.nl/datasets/entity/1174/item/"
# MASTER = 234677771
# REGISTERED = []
#
# HEADERS = {
#     'api_token': 'AbTVOcUtsMhJPqWcOPKxp5/kPz7nq/+UBN+YuT3Q988N/URihoXwz69xzxFI5ZRe',
#     # 'api_token': 'OazkjxN7tSIJlA9gB3AjlHswSsKXHwNYkMaZcIpKu5aU+9kXXklDXoeD5vUsoOfy',
#     'resource_id': 'moodteam10',
#     'token': 'token_for_identifier'
# }
#
# def schedule_checker():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)
#
# def send_message(chatid):
#     bot.sendMessage(chatid,
#                 "Hello, this is a reminder for input: /input, if you have already filled in, please ignore this message. Thank you very much!")
#     bot .sendMessage(MASTER, 'reminder for ' + str(chatid) + ' has sent.')
#
# class GoldenArches(telepot.helper.ChatHandler):
#     def __init__(self, *args, **kwargs):
#         super(GoldenArches, self).__init__(*args, **kwargs)
#         self.indicator = 'registration'
#         self.step = 'none'
#         self.message = {}
#         self.info = {}
#
#     def on_chat_message(self, msg):
#         content_type, chat_type, chat_id = telepot.glance(msg)
#         self.message['chat_id'] = chat_id
#
#         if self.indicator == 'registration':
#             if msg['text'] == '/start':
#                 # flag = True
#                 # for i in REGISTERED:
#                 #     if i == chat_id:
#                 #         bot.sendMessage(chat_id, 'You are already in the list. Start input by click on /input')
#                 #         flag = False
#                 #         break
#                 # for line in open('id.json', 'r'):
#                 #     record = json.loads(line)
#                 #     if record['chatid'] == chat_id:
#                 #         bot.sendMessage(chat_id, 'You are already in the list. Start input by click on /input')
#                 #         flag = False
#                 #         break
#                 # if flag:
#                 #     mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
#                 #                                   one_time_keyboard=True)
#                 #     bot.sendMessage(chat_id, 'Hi, we are Data-enabled design Mood Team 10. This is the data-collecting telegram bot run by MoodTeam10. You can contact @NeptuneTang or on our Teams channel if something serious happens. '
#                 #                              'Our research goal is to find out the relationship between stress eating, flavor and mood. Do you want to register in the test?', reply_markup=mark_up)
#                 bot.sendMessage(chat_id, 'Hi, we are Data-enabled design Mood Team 10. This is the data-collecting telegram bot run by MoodTeam10. You can contact @NeptuneTang or on our Teams channel if something serious happens. '
#                                          'Our research goal is to find out the relationship between stress eating, flavor and mood.')
#                 bot.sendMessage(chat_id, 'Select /input if you want to start your input. (reminder /set_reminder will be fixed later:) ')
#
#                 self.step = 'none'
#             # elif msg['text'] == 'yes':
#             #     REGISTERED.append(chat_id)
#             #     # mark_up = ReplyKeyboardMarkup(keyboard=[['19:00'], ['19:30'], ['20:00'], ['20:30'], ['21:00']],
#             #     #                               one_time_keyboard=True)
#             #     # bot.sendMessage(chat_id, "Great, your id is registered!")
#             #     # bot.sendMessage(chat_id, "Please choose your preference time in the evening for input reminder:(现在没用，到时候根据闹铃来设，先随便填！)",
#             #     #                 reply_markup=mark_up)
#             #     bot.sendMessage(chat_id, "Thank you very much for the input. You can type /input to start your input anytime you want.")
#             #     self.step = 'recordtime'
#             # elif msg['text'] == 'no':
#             #     bot.sendMessage(chat_id, 'Sorry to hear that. Chat ends. (If you change your mind, click here to join /start)')
#
#             # elif self.step == 'recordtime':
#             #     self.info['time'] = msg['text']
#             #     # with open('id.json', 'a') as handle:
#             #     #     json.dump(self.info, handle)
#             #     #     handle.write("\n")
#             #     #     handle.close()
#             #     bot.sendMessage(chat_id, "Thank you very much for the input. We will send you a reminder by then. You can also type /input to start your input anytime you want.")
#             #     schedule.every().day.at(self.info["time"]).do(send_message, chatid=chat_id)
#             #     reminder_master = 'user ' + str(self.info['chatid']) + ' has registered, the time is ' + self.info['time']
#             #     bot.sendMessage(MASTER, reminder_master)
#             #     self.step = 'none'
#             elif msg['text'] == '/input':
#                 mark_up = ReplyKeyboardMarkup(
#                     keyboard=[['Not at all'], ['A little bit stressful'], ['Medium level'], ['Very stressful']],
#                     one_time_keyboard=True)
#                 bot.sendMessage(chat_id,
#                                 text='Okay, let\'s get started! Could you please indicate your stress level over the day?',
#                                 reply_markup=mark_up)
#                 self.indicator = 'stress'
#             else:
#                 bot.sendMessage(chat_id,
#                                 text='Invalid input. Try /start if you are not registered yet, or /input if you want to input.')
#
#         elif content_type == 'text' and msg['text'] == '/input':
#             mark_up = ReplyKeyboardMarkup(
#                 keyboard=[['Not at all'], ['A little bit stressful'], ['Medium level'], ['Very stressful']],
#                 one_time_keyboard=True)
#             bot.sendMessage(chat_id,
#                             text='Okay, let\'s get started! Could you please indicate your stress level over the day?',
#                             reply_markup=mark_up)
#             self.indicator = 'stress'
#         elif self.indicator == 'stress':
#             self.message['stress'] = msg['text']
#             bot.sendMessage(chat_id, text='Next, which emoji will you pick for your day?')
#             self.indicator = 'emoji'
#         elif self.indicator == 'emoji':
#             self.message['emoji'] = msg['text']
#             bot.sendMessage(chat_id,
#                             text='Can I have a picture of the snack that you took? If yes, please upload a picture of snack. If not, please click /no')
#             self.indicator = 'snack'
#         elif self.indicator == 'snack':
#             if content_type == 'photo':
#                 file_name = str(chat_id)+'  '+ str(datetime.now().date())+'  '+str(datetime.now().time()) + '.png'
#                 self.message['image'] = file_name
#                 bot.sendPhoto(MASTER, msg['photo'][-1]['file_id'], file_name)
#                 mark_up = ReplyKeyboardMarkup(
#                     keyboard=[['1-not at all(yogurt, banana,...)'], ['2-a little bit crunchy(chocolate,...)'],
#                               ['3-medium crunchy(sweets,...)'], ['4-very crunchy(nuts,apple...)'],
#                               ['5-super crunchy(chips,...)']],
#                     one_time_keyboard=True)
#                 bot.sendMessage(chat_id,
#                                 text='Thanks for the pictrue! Can you indicate the crunchy level(1-5) of your snack? Example are just given for reference, you can judge it on your own.',
#                                 reply_markup=mark_up)
#                 self.step = 'crunchy'
#             elif self.step == 'crunchy':
#                 self.message['crunchy'] = msg['text']
#                 bot.sendMessage(chat_id,
#                                 text='Last question! This is an open question. Any comments are welcome:)')
#                 bot.sendMessage(chat_id,
#                                 text='Do you have any comments? For example, how do you feel after listen to the crunchy sound? If not, please click /none')
#                 self.indicator = 'comment'
#             elif msg['text'] != '/no':
#                 bot.sendMessage(chat_id, "Sorry, please send me a photo via picture, not via document!")
#             else:
#                 self.message['image'] = 'no image input'
#                 bot.sendMessage(chat_id,
#                                 text='Last question! This is an open question. Any comments are welcome:)')
#                 bot.sendMessage(chat_id,
#                                 text='Do you have any comments? For example, how do you feel after listen to the crunchy sound? If not, please click /none')
#                 self.indicator = "comment"
#             # if self.step == 'changing mood':
#             #     self.message['happy_after_snack'] = msg['text']
#             # elif self.step == 'guilty':
#             #     self.message['guilty_after_snack'] = msg['text']
#             # else:
#             #     self.message['snack'] = msg['text']
#             #
#             # if msg['text'] == '/no' or self.step == 'guilty':
#             #     bot.sendMessage(chat_id,
#             #                 text='Do you have any comment about your diet today?(e.g. very good/eating too much/...) If not, please click /none')
#             #     self.indicator = 'comment'
#             #     self.step = 'none'
#             # elif self.step == 'changing mood':
#             #     mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
#             #                                   one_time_keyboard=True)
#             #     bot.sendMessage(chat_id,
#             #                     text='Do you feel burdened after eating?', reply_markup=mark_up)
#             #     self.step = 'guilty'
#             # else:
#             #     mark_up = ReplyKeyboardMarkup(keyboard=[['yes'], ['no']],
#             #                                   one_time_keyboard=True)
#             #     bot.sendMessage(chat_id,
#             #                     text='Are you feeling happy after you had these snacks?', reply_markup=mark_up)
#             #     self.step = 'changing mood'
#
#         elif self.indicator == 'comment':
#             self.message['comment'] = msg['text']
#             #     bot.sendMessage(chat_id, text="Thank you. Can I ask for a picture?")
#             #     self.indicator = 'pic'
#             # elif self.indicator == 'pic':
#             #     file_name = 'pic/' + str(t) + '  ' + str(chat_id) + '.png'
#             #     bot.download_file(msg['photo'][-1]['file_id'], file_name)
#             #     self.message['picture'] = msg['photo'][-1]['file_id']
#             # with open('message.json', 'a') as handle:
#             #     json.dump(self.message, handle)
#             #     handle.write("\n")
#             #     handle.close()
#             requests.post(url=URL, headers=HEADERS, json=self.message)
#             bot.sendMessage(chat_id, 'Message Accepted. Thank you very much again for the input. Have a nice day:)')
#             reminder_master = 'user ' + str(chat_id) + ' has completed today\'s input'
#             bot.sendMessage(MASTER, reminder_master)
#             self.indicator = 'registration'
#
#
#
# bot = telepot.DelegatorBot(TOKEN, [
#     pave_event_space()(
#         per_chat_id(), create_open, GoldenArches, timeout=86400),
# ])
# server = Flask(__name__)
# MessageLoop(bot).run_as_thread()
# print('Listening ...')
#
# @server.route('/' + TOKEN, methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://mood10.herokuapp.com/' + TOKEN)
#     return "!", 200
#
#
# if __name__ == "__main__":
#     # for line in open('id.json', 'r'):
#     #     record = json.loads(line)
#         # 群发消息
#         # bot.sendMessage(record['chatid'], "Thank you for participation. We are now preparing for the deployment so the bot will be stopped.")
#     # schedule.every().day.at(record["time"]).do(send_message, chatid=record['chatid'])
#     # Thread(target=schedule_checker).start()
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

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

TOKEN = '1694116177:AAEr9gLPK__8YNLUx9KAsRZ1gEHwG4qzkqU'
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