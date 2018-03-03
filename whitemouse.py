# -*- coding: utf-8 -*-

import traceback, os
from datetime import datetime
import time
from random import uniform, randint
from os import walk
import json
import re
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import error as TelegramError, Bot
import apiai


# Constants
TOKEN_TELEGRAM_FILE = 'telegram_token.ctl'
TOKEN_DIALOGDLOW_FILE = 'dialogflow_token.ctl'
WHITEMOUSE_IMG = 'whitemouse.jpg'
ROTATEWHEEL_URL = 'http://coub.com/view/13cty1'
GIRLS_DIR = r''
PARAMS = \
    {
        "lang" : "ru",
        "telegram_token_filename" : TOKEN_TELEGRAM_FILE,
        "dialogflow_token_filename" : TOKEN_DIALOGDLOW_FILE
    }

# Errors
class GetTokenError(Exception): pass


# CONSOLE LOG
cfromat = "[{0}] {1}{2}"
def print_message(message, level=0):
    level_indent = " " * level
    print(cfromat.format(datetime.now(), level_indent, message))
    
# Utils
def build_version_string():
    """ This function read current version from version.txt and format version string """
    # MAJOR version when you make incompatible API changes
    __MAJOR_VERSION__ = str()
    # MINOR version when you add functionality in a backwards-compatible manner
    __MINOR_VERSION__ = str()
    # PATCH version when you make backwards-compatible bug fixes
    __PATCH_VERSION__ = str()
    with open('version.txt', 'r') as version_file:
        lines = version_file.readlines()
        for line in lines:
            if line.startswith('__MAJOR_VERSION__'):
                __MAJOR_VERSION__ = re.findall('\d+', line)[0]
            if line.startswith('__MINOR_VERSION__'):
                __MINOR_VERSION__ = re.findall('\d+', line)[0]
            if line.startswith('__PATCH_VERSION__'):
                __PATCH_VERSION__ = re.findall('\d+', line)[0]
    _header = "Whitemouse (v{0}.{1}.{2}) {3}".format(__MAJOR_VERSION__, __MINOR_VERSION__, __PATCH_VERSION__,
                                                      datetime.now().strftime("%B %d %Y, %H:%M:%S"))
    return _header

def read_token(source):
    """ This function read token from tokenfile by source """
    fname = PARAMS.get("{}_token_filename".format(source))
    if fname is None: return None
    try:
        with open(fname, 'r') as f:
            token = f.readline()
    except FileNotFoundError as e:
        raise GetTokenError("Token file '{}' not found.".format(fname))
    if token is None or token == "":
        raise GetTokenError("Token is empty. Check token file '{}'!".format(fname))      
    return token


# Commands
def start_command(bot, update):
    """ This is handler for command \start """
    try:
        print_message("Handle command 'start' to chat {}".format(update.message.chat_id))
        MSG = \
        {
            "en" : \
            """
            Hello! I'm whitemouse bot (i was created for the experiences of my creator ). Talk to me or give a command, I will fulfill them!
            """,
            "ru" : \
            """
            Привет! Я белая мышь (я бот и предназначен для тестов моего создателя). Поговори со мной или скинь пару команд, я с удовольствием их выполню!
            """
        }
        try:
            with open(WHITEMOUSE_IMG, 'rb') as f:
                bot.send_photo(chat_id=update.message.chat_id, photo=f, caption=MSG[PARAMS["lang"]], timeout=60)
                return
        except FileNotFoundError:
            print_message("Warning: File {} not found! Send mesasge without photo.".format(WHITEMOUSE_IMG), 2)
        except Exception:
            print_message(traceback.format_exc())
        bot.send_message(chat_id=update.message.chat_id, text=MSG[PARAMS["lang"]])
    except:
        print_message(traceback.format_exc())


def rotatewheel_command(bot, update):
    """ This is handler for command \rotatewheel """
    try:
        print_message("Handle command 'rotatewheel' to chat {}".format(update.message.chat_id))
        MSG = \
        {
            "en" : \
            """
            Sorry, I can not run now. The owner took the wheel!
            """,
            "ru" : \
            """
            Извини, не могу побегать сейчас. Хозяин отобрал колесо!
            """
        }
        try:
            if uniform(0, 1) < 0.8:
                bot.send_message(chat_id=update.message.chat_id, text="OK, BOSS! {}".format(ROTATEWHEEL_URL))
                return
        except Exception:
            print_message(traceback.format_exc())
        bot.send_message(chat_id=update.message.chat_id, text=MSG[PARAMS["lang"]])
    except:
        print_message(traceback.format_exc())


def getgirl_command(bot, update):
    """ This is handler for command \getgirl """
    try:
        print_message("Handle command 'getgirl' to chat {}".format(update.message.chat_id))
        gfiles = []
        for root, dirs, files in os.walk(GIRLS_DIR):
            gfiles.extend(files)
        girl_photo_filename = gfiles[randint(0, len(gfiles))] if gfiles else "emptydir.err"
        SORRY_MSG = \
        {
            "en" : \
            """
            Sorry, the owner took the photo album from me, hmm ... Why are they to him?
            """,
            "ru" : \
            """
            Извини, хозяин забрал у меня альбом с фото, хм ... зачем они ему?
            """
        }
        MSG = \
        {
            "en" : \
            """
            Catch the picture faster, until the owner sees it!
            """,
            "ru" : \
            """
            Быстрее лови фото, пока хозяин не видит!
            """
        }
        try:
            with open(os.path.join(GIRLS_DIR, girl_photo_filename), 'rb') as f:
                bot.send_photo(chat_id=update.message.chat_id, photo=f, caption=MSG[PARAMS["lang"]])
                return
        except FileNotFoundError:
            print_message("Warning: File {} not found! Send mesasge without photo.".format(girl_photo_filename), 2)
        bot.send_message(chat_id=update.message.chat_id, text=SORRY_MSG[PARAMS["lang"]])
    except:
        print_message(traceback.format_exc())


def cnangelang_command(bot, update):
    """ This is handler for command \changelang """
    try:
        print_message("Handle command 'changelang' to chat {}".format(update.message.chat_id)) 
        MSG = \
        {
            "en" : \
            """
            Current language: Inglish.
            """,
            "ru" : \
            """
            Текущий язык: Русский.
            """
        }
        if PARAMS["lang"] == "ru":
            PARAMS["lang"] = "en"
        else:
            PARAMS["lang"] = "ru"
        bot.send_message(chat_id=update.message.chat_id, text=MSG[PARAMS["lang"]])
    except:
        print_message(traceback.format_exc())


# Messages
def text_message(bot, update):
    """ This is handler for messages from chat """
    try:
        request = PARAMS["dialogflow"].text_request()
        request.lang = 'ru'
        request.session_id = update.message.chat_id
        request.query = update.message.text
        response = json.loads(request.getresponse().read().decode('utf-8'))
        response = response['result']['fulfillment']['speech']
        if response:
            bot.send_message(chat_id=update.message.chat_id, text=response)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='Я не совсем поняла последнее сообщение')
    except:
        print_message(traceback.format_exc())


def photo_message(bot, update):
    """ This is handler for photo in chat """
    try:
        print_message("Handle textmessage from chat {}".format(update.message.chat_id))
        MSG = \
        {
            "en" : \
            """
            Cool!
            """,
            "ru" : \
            """
             руто!
            """
        }
        if PARAMS["lang"] == "ru":
            PARAMS["lang"] = "en"
        else:
            PARAMS["lang"] = "ru"
        bot.send_message(chat_id=update.message.chat_id, text=MSG[PARAMS["lang"]])
    except:
        print_message(traceback.format_exc())


# Manage
def Start():
    """ This is function initialize APIs and set handlers """
    try:
        print_message("Initialize.")
        print_message("Initialize telegram.", 2)
        telegram_token = read_token('telegram')
        print_message("Connect...", 2)
        updater = Updater(token=telegram_token)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start_command))
        dispatcher.add_handler(CommandHandler('changelang', cnangelang_command))
        dispatcher.add_handler(CommandHandler('rotatewheel', rotatewheel_command))
        dispatcher.add_handler(CommandHandler('getgirl', getgirl_command))
        dispatcher.add_handler(MessageHandler(Filters.photo, photo_message))
        dispatcher.add_handler(MessageHandler(Filters.text, text_message))
        print_message("Initialize dialogflow.", 2)
        dialogflow_token = read_token('dialogflow')
        PARAMS["dialogflow"] = apiai.ApiAI(client_access_token=dialogflow_token)
        print_message("Start processing new messages...", 2)
        updater.start_polling(clean=True)
        print_message("Processing new mesages.")
        updater.idle()
    except GetTokenError as error:
        print_message("Error: {}".format(error.args[0]))
    except TelegramError.TelegramError as error:
        print_message("Error: {}".format(error.message))
    except KeyboardInterrupt:
        settings.print_message("Caught KeyboardInterrupt, terminating processing")
    except Exception:
        print_message(traceback.format_exc())


if __name__ == "__main__":
    print_message(build_version_string())
    Start()