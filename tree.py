from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import html
from telegram import Update, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler
import json
import logging
import traceback
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup , ReplyKeyboardMarkup , KeyboardButton
import csv



############################### Bot ############################################

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

DEVELOPER_CHAT_ID = *********




#######################################################################################


# main menu
def start(update,context):
    bot = context.bot
    menu_main = [[InlineKeyboardButton('new Tree', callback_data='m1')],
                 [InlineKeyboardButton('Show Trees', callback_data='m2')],
                 [InlineKeyboardButton('Edit Trees', callback_data='m3')]]
    reply_markup = InlineKeyboardMarkup(menu_main)
    update.message.reply_text('What do you want to do?', reply_markup=reply_markup)



def menu_actions(update,context):
    bot = context.bot
    query = update.callback_query
    
    if query.data == 'm1':

        # update.callback_query.message.reply_text("Enter the Earliest Ancestor:")
        
        update.effective_message("Enter the Earliest Ancestor:")
        with open('Tree.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            text_1 = update.effective_message.text
            writer.writerow([text_1]) 
                   
        




    elif query.data == 'm2':
        # second submenu
        # first submenu
        menu_2 = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
                  [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')]]
        reply_markup = InlineKeyboardMarkup(menu_2)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text='Choose the option:',
                              reply_markup=reply_markup)

def first_menu(update,context):
    bot = context.bot
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def second_menu(update,context):
    bot = context.bot
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=second_menu_message(),
                        reply_markup=second_menu_keyboard())

# and so on for every callback_data option
def first_submenu(update,context):
    bot = context.bot
    pass

def second_submenu(update,context):
    bot = context.bot
    pass

############################ Keyboards #########################################
def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('New Tree'),
                KeyboardButton('Show Trees'),
                KeyboardButton('Edit Trees')
                ]
            ]
        )
    return keyboard

def first_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('bbb'),
                KeyboardButton('ccc'),
                KeyboardButton('main menu')
                ]
            ]
        )
    return keyboard

def second_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('ddd'),
                KeyboardButton('eee'),
                KeyboardButton('main menu')
                ]
            ]
        )
    return keyboard


def third_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        [
            [
                KeyboardButton('ddd'),
                KeyboardButton('eee'),
                KeyboardButton('main menu')
                ]
            ]
        )
    return keyboard



############################# Messages #########################################
def main_menu_message():
  return 'قصد دارید چه کنید؟'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'


################################################################################

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb_string),
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)

def main():
     # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater('**************************************',use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    ############################# Handlers #########################################


    # Register the commands...
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CallbackQueryHandler(menu_actions))

    dp.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dp.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    dp.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
    dp.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))




    11
    # ...and the error handler    
    dp.add_error_handler(error_handler)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
