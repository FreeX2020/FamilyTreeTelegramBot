from telegram.ext import (
    Updater, InlineQueryHandler,
    CommandHandler, ConversationHandler,
    MessageHandler, Filters,
    PicklePersistence
    )
import requests
import re
import html
from telegram import Update, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler
import json
import logging
import traceback
from telegram.ext import CallbackQueryHandler
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup , KeyboardButton,
    )
import csv
import config



############################### Bot ############################################

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

DEVELOPER_CHAT_ID = 597932770




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
    
##    if query.data == 'm1':
        #Registered the new handler for this!
        # update.callback_query.message.reply_text("Enter the Earliest Ancestor:")
        
##        update.effective_message("Enter the Earliest Ancestor:")
##        with open('Tree.csv', 'w', newline='') as file:
##            writer = csv.writer(file)
##            text_1 = update.effective_message.text
##            writer.writerow([text_1]) 
                   

    if query.data == 'm2':
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
    #context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


def manageCallbacks (update, context):
    query = update.callback_query
    if query.data in ('m2'):
        menu_actions(update, context)
    elif query.data == 'm1_1':
        first_submenu(update, context)
    elif query.data == 'm2_1':
        second_submenu(update, context)
    else:
        query.answer("Nothing found!")


def getRelations ():
    kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = 'Child',
                        callback_data = 'addPersonRelation Child'
                        ),
                    InlineKeyboardButton(
                        text = 'Spouse',
                        callback_data = 'addPersonRelation Spouse'
                        )
                    ],
                [
                    InlineKeyboardButton(
                        text = 'Earlier Ancestor',
                        callback_data = 'addPersonRelation EA'
                        )
                    ]
                ]
            )
    return kb

def getGenders ():
    kb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = 'male',
                        callback_data = 'setgender male'
                        ),
                    InlineKeyboardButton(
                        text = 'female',
                        callback_data = 'setgender female'
                        )
                    ]
                ]
            )
    return kb

class ConversationFirstMenu:

    def entry (update, context):
        context.bot.send_message(
            chat_id = update.callback_query.message.chat_id,
            text = 'Okay, enter the Earliest Ancestor.'
            )
        return 'getEA'

    def setEarliestAncestor (update, context):
        
        Message = update.message
        EarliestAncestor = Message.text
        
        #If user exist get him data else create empty dict
        if Message.from_user.id in context.bot_data:
            data = context.bot_data[Message.from_user.id]
        else:
            data = {}

        #Update user data
        data[EarliestAncestor] = {"relations": {"Earliest Ancestor": None}, "gender": None, "selected": True}
        context.bot_data[Message.from_user.id] = data

        #Save datafile
        context.dispatcher.persistence.flush()

        #Get gender keyboard from getGenders
        keyboard = getGenders()
        
        Message.reply_text(
            "Set the {} gender: ".format(EarliestAncestor),
            reply_markup = keyboard
            )
        return "callbacks"

    def changePersonRelations (update, context):
        Query = update.callback_query

        #Retrieve userdata
        data = context.bot_data[Query.from_user.id]

        #Get selected person
        for personName, personDetails in data.items():
            if personDetails['selected']:
                break

        #Update userdata
        personRelation = Query.data.split()[1]
        if personRelation == 'EA':
            for pN, pD in data.items():
                if "Earliest Ancestor" in pD["relations"]:
                    Query.answer(
                        text = "Earliest ancestor must be one!",
                        show_alert = True
                        )
                    return
        if personRelation == 'EA':
            personRelation = 'Earliest Ancestor'
        personDetails['relations'].append({personRelation: None})
        
        data[personName] = personDetails
        context.bot_data[Query.from_user.id] = data

        #Save changes
        context.dispatcher.persistence.flush()

        options = {
            "Earliest Ancestor": None,
            'Child': 'parent',
            'Spose': 'spouse'
            }

        Query.message.edit_text(
            text = "Enter the name {} for {}".format(options[personRelation], personName)
            )

        return 'setRelation2ndPerson'

    def setRelationFor (update, context):
        Message = update.message

        secondPersonName = Message.text

        data = context.bot_data[Message.from_user.id]

        for personName, personDetails in data.items():
            if personDetails['selected']:
                break

        for index, relation in enumerate(personDetails['relations']):
            for name, secondPerson in relation.items():
                if secondPerson is None:
                    personDetails['relations'][index] = {name: secondPersonName}
                    break

        data[personName] = personDetails
        context.bot_data[Message.from_user.id] = data

        context.dispatcher.persistence.flush()

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = 'Yes!',
                        callback_data = 'haveOtherRelations yes'
                        ),
                    InlineKeyboardButton(
                        text = 'No!',
                        callback_data = 'haveOtherRelations no'
                        )
                    ]
                ]
            )
                
        Message.reply_text(
            text = 'Successfully updated relation {0} to {1}! Have {0} other relations?'.format(personName, secondPersonName),
            reply_markup = keyboard
            )
        
        return 'callbacks'
        
        

    def changePersonGender (update, context):

        Query = update.callback_query


        data = context.bot_data[Query.from_user.id]

        for personName, personDetails in data.items():
            if personDetails['selected']:
                break

        #Update the data
        selectedGender = Query.data.split()[1]
        personDetails['gender'] = selectedGender
        data[personName] = personDetails
        context.bot_data[Query.from_user.id] = data

        #Save datafile
        context.dispatcher.persistence.flush()

        if len(data[personName]['relations'])<1:
            #Retrieve relations keyboard from getRelations
            keyboard = getRelations()

            #Give the user a choice relations for person
            Query.message.edit_text(
                text = 'Select the {} relation:'.format(personName),
                reply_markup = keyboard
                )
            #Change dialog state
            return 'callbacks'

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text = 'Yes!',
                        callback_data = 'haveOtherRelations yes'
                        ),
                    InlineKeyboardButton(
                        text = 'No!',
                        callback_data = 'haveOtherRelations no'
                        )
                    ]
                ]
            )
        Query.message.edit_text(
            text = "Gender saved. Does {} have other relations?".format(personName),
            reply_markup = keyboard
            )
        
        return 'callbacks'

    def newPerson (update, context):
        Message = update.message
        personName = Message.text

        #Get userdata
        data = context.bot_data[Message.from_user.id]
        
        #Add new person to exists
        data[personName] = {"relations": [], 'gender': None, 'selected':True}
        context.bot_data[Message.from_user.id] = data

        #Save datafile
        context.dispatcher.persistence.flush()

        #Get gender keyboard from getGenders
        keyboard = getGenders()

        #Give the user a choice of gender
        Message.reply_text(
            text = 'Select {} gender:'.format(personName),
            reply_markup = keyboard
            )
        
        return 'callbacks'
        
        
    def manageCallbacks (update, context):
        Query = update.callback_query

        options = {"yes": True, 'no': False}

        if Query.data.startswith('setgender'):
            return ConversationFirstMenu.changePersonGender(update, context)
        elif Query.data.startswith('haveOtherRelations'):
            haveOtherRelations = options[Query.data.split()[1]]
            if haveOtherRelations:
                
                #Get relations keyboard from the getRelations
                keyboard = getRelations()
                
                Query.message.edit_text(
                    text = "Select relation:",
                    reply_markup = keyboard
                    )
                return 'callbacks'
            else:
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text = 'Cancel!',
                                callback_data = 'cancel'
                                ),
                            InlineKeyboardButton(
                                text = 'Save!',
                                callback_data = 'save'
                                )
                            ],
                        [
                            InlineKeyboardButton(
                                text = 'New Person!',
                                callback_data = 'newPerson'
                                )
                            ]
                        ]
                    )
                Query.message.edit_text(
                    text = 'What do you want to do:',
                    reply_markup = keyboard
                    )
                return 'callbacks'
        elif Query.data == 'cancel':

            #Delete user data
            context.bot_data[Query.from_user.id] = {}

            #Save changes
            context.dispatcher.persistence.flush()

            Query.message.edit_text(
                text = 'Cancelled!'
                )
            
            #Return quit code from ConversationHandler
            return ConversationHandler.END

        elif Query.data == 'save':

            #Save data
            context.dispatcher.persistence.flush()

            #Retrieve userdata
            data = context.bot_data[Query.from_user.id]

            """
            Here must be code to write .csv file!
            """

            Query.message.edit_text(
                text = 'Saved!'
                )

            #Return quit code from ConversationHandler
            return ConversationHandler.END

        elif Query.data == 'newPerson':

            data = context.bot_data[Query.from_user.id]

            for personName, personDetails in data.items():
                personDetails['selected'] = False

            context.bot_data[Query.from_user.id] = data

            context.dispatcher.persistence.flush()

            Query.message.edit_text(
                text = 'Okay, enter the person name.'
                )

            return 'newPerson'
        elif Query.data.startswith('addPersonRelation'):
            return ConversationFirstMenu.changePersonRelations(update, context)

def ConvCancel (update, context):
    context.bot_data[update.message.from_user.id] = {}
    
    update.message.reply_text(
        text = 'Cancelled!'
        )
    
    return ConversationHandler.END
        
        
        


def main():
     # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    persistence = PicklePersistence('DATA')
    
    updater = Updater(
        token = config.TeleTestToken,
        use_context = True,
        persistence = persistence
        )
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    ###################################################### Handlers #############################################################


    # ________________________________________________ CommandHandlers _________________________________________________________
    
    dp.add_handler(CommandHandler('start',start))

    # _______________________________________________ ConversationHandlers _______________________________________________________

    dp.add_handler(
        ConversationHandler(
            entry_points = [
                CallbackQueryHandler(
                    callback = ConversationFirstMenu.entry,
                    pattern = 'm1'
                    )
                ],
            states = {
                'getEA': [
                    MessageHandler(
                        filters = Filters.text & ~Filters.command,
                        callback = ConversationFirstMenu.setEarliestAncestor
                        )
                    ],
                'callbacks': [
                    CallbackQueryHandler(
                        callback = ConversationFirstMenu.manageCallbacks
                        )
                    ],
                'newPerson': [
                    MessageHandler(
                        filters = Filters.text & ~Filters.command,
                        callback = ConversationFirstMenu.newPerson
                        )
                    ],
                'setRelation2ndPerson': [
                    MessageHandler(
                        filters = Filters.text & ~Filters.command,
                        callback = ConversationFirstMenu.setRelationFor
                        )
                    ]
                },
            fallbacks = [
                CommandHandler(
                    command = 'cancel',
                    callback = ConvCancel
                    )
                ]
            )
        )


    # _______________________________________________ CallbackQueryHandlers ______________________________________________________
    
    dp.add_handler(CallbackQueryHandler(manageCallbacks))


    # ________________________________________________ ErrorHandler _______________________________________________________________
    
    dp.add_error_handler(error_handler)


    
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
