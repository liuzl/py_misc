import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from telebot_router import TeleBot

app = TeleBot(__name__)


@app.route('/command ?(.*)')
def example_command(message, cmd):
    chat_dest = message['chat']['id']
    msg = "Command Recieved: {}".format(cmd)

    app.send_message(chat_dest, msg)


@app.route('(?!/).+')
def parrot(message):
    chat_dest = message['chat']['id']
    user_msg = message['text']
    print(message)
    msg = "Parrot Says: {}".format(user_msg)
    app.send_message(chat_dest, msg)


if __name__ == '__main__':
    app.config['api_key'] = os.getenv("XGOOBOT_TOKEN")
    app.poll(debug=True)
