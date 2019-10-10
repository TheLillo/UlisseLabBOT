from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from manageVPN import check_or_gen_vpn
import logging
import configparser

config_file = Path("config.ini")
if config_file.is_file():
    with config_file.open() as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        TOKEN = config.get('DEFAULT', 'Token')
        CHAT_ID = config.get('DEFAULT', 'Chat_Id')
        VPN_DIR = config.get('DEFAULT', 'Vpn_Dir')
        # TEMP_DIR = config.get('DEFAULT', 'Temp_Dir')
        SOCKET_ADDR = config.get('DEFAULT', 'Socket_Addr')
else:
    print("config.ini non trovato")
    exit(1)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

all_commands = {}
task = lambda f: all_commands.setdefault(f.__name__, f)


def start(bot, update):
    keyboard = [[InlineKeyboardButton("SendVPN", callback_data='sendVPN')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


@task
def sendVPN(bot, update):
    if bot.getChat(chat_id=update.message.chat_id).type == 'private':
        user_state = bot.getChatMember(chat_id=CHAT_ID, user_id=update.effective_user.id).status
        if user_state == 'member' or user_state == 'creator':
            # vpn_file = check_or_gen_vpn(VPN_DIR, TEMP_DIR, update.message.chat.first_name)
            vpn_file = check_or_gen_vpn(SOCKET_ADDR, VPN_DIR, update.message.chat.first_name)
            if vpn_file:
                bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
                bot.send_document(chat_id=update.message.chat_id, document=open(vpn_file, 'rb'), caption="Before connecting to the VPN wait 1 minutes")
            else:
                bot.send_message(chat_id=update.message.chat_id, text="I'm Sorry. Something went wrong :(")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="I'm Sorry. This is not for you!")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="I'm Sorry. This is Command is only for private chat :)")


def button(bot, update):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))

    all_commands[query.data](bot, update)


def help(bot, update):
    update.message.reply_text("Use /start to use this bot.")


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    #start_handler = CommandHandler('start', start)
    #dispatcher.add_handler(start_handler)

    sendVPN_handler = CommandHandler('sendVPN', sendVPN)
    dispatcher.add_handler(sendVPN_handler)

    #updater.dispatcher.add_handler(CallbackQueryHandler(button))
    #updater.dispatcher.add_handler(CommandHandler('help', help))

    updater.start_polling()


if __name__ == '__main__':
    main()

