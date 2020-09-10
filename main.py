from telegram.ext import Updater, CommandHandler
from telegram import ChatAction
from pathlib import Path
from manageVPN import check_or_gen_vpn
from managePublicKey import add_public_key
import logging
import configparser
import re

config_file = Path("config.ini")
if config_file.is_file():
    with config_file.open() as f:
        config = configparser.ConfigParser()
        config.read_file(f)
        TOKEN = config.get('DEFAULT', 'Token')
        CHAT_ID = config.get('DEFAULT', 'Chat_Id')
        VPN_DIR = config.get('DEFAULT', 'Vpn_Dir')
        SOCKET_ADDR = config.get('DEFAULT', 'Socket_Addr')
        CHECKER_NEW_VPN = config.get('DEFAULT', 'Vpn_Checker')
        PUBLIC_KEYS_FILE = config.get('DEFAULT', 'Public_keys_file')
else:
    print("config.ini non trovato")
    exit(1)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

regex = re.compile('^ssh-(ed25519|rsa) AAAA[A-Za-z0-9/]+=?=?( [-a-zA-Z.@_]+)?$')


def send_vpn(update, context):
    if context.bot.getChat(chat_id=update.effective_chat.id).type == 'private':
        user_state = context.bot.getChatMember(chat_id=CHAT_ID, user_id=update.effective_user.id).status
        if user_state == 'member' or user_state == 'creator' or user_state == 'administrator':
            current_username = update.message.chat.username
            if current_username:
                vpn_file = check_or_gen_vpn(SOCKET_ADDR, VPN_DIR, CHECKER_NEW_VPN, current_username)
                if vpn_file:
                    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
                    context.bot.send_document(chat_id=update.message.chat_id, document=open(vpn_file, 'rb'),
                                              caption="Before connecting to the VPN wait 1 minutes")
                else:
                    update.message.reply_text("I'm Sorry. Something went wrong :(")
            else:
                update.message.reply_text("I'm Sorry. set Username :(")
        else:
            update.message.reply_text("I'm Sorry. This is not for you!")
    else:
        update.message.reply_text("I'm Sorry. This is Command is only for private chat :)")


def get_public_key(update, context):
    if context.bot.getChat(chat_id=update.effective_chat.id).type == 'private':
        user_state = context.bot.getChatMember(chat_id=CHAT_ID, user_id=update.effective_user.id).status
        if user_state == 'member' or user_state == 'creator':
            current_username = update.message.chat.username
            if current_username:
                public_key = " ".join(context.args)
                if public_key:
                    if regex.fullmatch(public_key) and len(public_key) <= 1024:
                        add_public_key(PUBLIC_KEYS_FILE, current_username, public_key)
                        update.message.reply_text("We have add your public key. Remember only one key per user")
                    else:
                        update.message.reply_text("I'm Sorry. Your Fucking public key has some special character or is too long, only RSA and ED25519")
                else:
                    update.message.reply_text("I'm Sorry. You must write your public key string after the command")
            else:
                update.message.reply_text("I'm Sorry. set Username :(")
        else:
            update.message.reply_text("I'm Sorry. This is not for you!")
    else:
        update.message.reply_text("I'm Sorry. This is Command is only for private chat :)")


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    send_vpn_handler = CommandHandler('sendVPN', send_vpn)
    dispatcher.add_handler(send_vpn_handler)

    get_public_key_handler = CommandHandler('getPublicKey', get_public_key)
    dispatcher.add_handler(get_public_key_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
