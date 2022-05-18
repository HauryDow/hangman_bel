import logging
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import random
import os
import time
from images import *
from images1 import *

def start_command(update, context):
    game_data['state_game'] = True
    game_data['word'] = random_word()
    game_data['spaces'] = ['_'] * len(game_data['word'])
    game_data['life'] = 0
    game_data['letter_aux'] = []
    # print(game_data['word'])
    game(update, context)

def help_command(update, context):
    update.message.reply_text(
        ''' Гэта простая гульня "Вісельнік"
         💀👻💀
        Каманды:
        /start - пачаць новую гульню.
        /stop - спыніць гульню. 
       ''')

def stop_command(update, context):
    game_data['state_game'] = False
    update.message.reply_text('😎 Бот спынены. Адпраўце /start  каб пачаць гульню')

def random_word():
    return words[random.randint(0, len(words) - 1)][:-1]


def display_board(update, context, game_data):
    keyboard = [['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З',],
                ['І', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', ],
                ['Р', 'С', 'Т', 'У', 'Ў', 'Ф', 'Х', 'Ц',],
                [ 'Ш','💀', 'Ы', 'Ь', "'", 'Э', 'Ю', 'Я']]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(
        IMAGES[game_data['life']] + " ".join(game_data['spaces']) + '\n\n' + 'Выбярыце літару 🙂 "Дз" і "Дж" абазначаюцца 2ма літарамі.''',
        reply_markup=reply_markup)

def game(update, context, **kwargs):
    if game_data['state_game']:

        current_letter = update.message.text#.lower()
        if (len(current_letter) > 1):
            display_board(update, context, game_data)
        else:

            letter_index = [i for i in range(len(game_data['word'])) if game_data['word'][i] == current_letter]

            if len(letter_index) <= 0:
                game_data['life'] += 1

                for i in range(len(game_data['letter_aux'])):
                    if game_data['letter_aux'][i] == current_letter:
                        update.message.reply_text('🤓 Літара {} ужо выбіралася'.format(current_letter.upper()))
                        game_data['life'] -= 1
                        break

                game_data['letter_aux'].append(current_letter)

            else:
                for i in letter_index:
                    game_data['spaces'][i] = current_letter

                letter_index = []

            display_board(update, context, game_data)

            if game_data['life'] == 7:
                update.message.reply_text('🤦 Выбачайце, правільнае слова {}. Адпраўце /start каб пачаць новую гульню'.format(game_data['word'].upper()))
                game_data['state_game'] = False

            try:
                game_data['spaces'].index('_')

            except ValueError:
                update.message.reply_text(
                   IMAGES1 + '\n\n' +
                    'Віншуем! \n Ваша слова {}. \n Вы зарабілі {} балаў 🏆'.format(game_data['word'], 100-game_data['life']*10))
                
                game_data['state_game'] = False
    else:
        update.message.reply_text('Адпраўце /start каб пачаць гульню')


game_data = {'state_game': False}

with open('words.txt', 'r') as file:
    words = file.readlines()
