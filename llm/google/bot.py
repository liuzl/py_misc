import os
import json
import traceback
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from telebot import TeleBot  # type: ignore
from telebot.types import BotCommand, Message  # type: ignore

model = "gemini-pro"
url = f"https://googleapis.fmr.wiki/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
headers = {"Content-Type": "application/json"}

def new_session():
    return {
        "history": []
    }

def chat(history: list)->str:
    if history and history[-1]["role"] != "user":
        return "need user input"
    ret = requests.post(url, json.dumps({"contents": history}), headers=headers)
    print(ret.json())
    item = ret.json()
    if 'error' in item:
        print(item)
        return item['message']
    if 'candidates' not in item or len(item['candidates']) == 0:
        return "no candidates"
    if 'content' not in item['candidates'][0]:
        return "no content"
    reply = item['candidates'][0]['content']
    history.append(reply)
    return reply['parts'][0]['text']

def main():
    bot = TeleBot(os.getenv("XGOOBOT_TOKEN"))
    print("bot init done.")
    sessions = {}

    @bot.message_handler(regexp='(?!/).+')
    def gemini(message):
        reply_message = bot.reply_to(
            message,
            "Generating google gemini answer please wait, note, will only keep the last ten messages:"
        )
        print(f"{message.from_user.id}({message.from_user.first_name}): {message.text}")
        session = None
        # restart will lose all TODO
        if str(message.from_user.id) not in sessions:
            session = new_session()
            sessions[str(message.from_user.id)] = session
        else:
            session = sessions[str(message.from_user.id)]
        if len(session["history"]) > 20:
            session["history"] = session["history"][2:]
        if session["history"] and session["history"][-1]["role"] == "user":
            session["history"][-1]["parts"].append({"text": message.text})
        else:
            session["history"].append({"role":"user", "parts":[{"text": message.text}]})
        try:
            bot.reply_to(message, chat(session["history"]))
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, "Something wrong please check the log")
        bot.delete_message(reply_message.chat.id, reply_message.message_id)
    
    print("starting telegram bot.")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
