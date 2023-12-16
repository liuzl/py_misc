import os
import json
import base64
import traceback
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from telebot import TeleBot  # type: ignore
from telebot.types import BotCommand, Message  # type: ignore

model = "gemini-pro"
url = f"https://googleapis.fmr.wiki/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
headers = {"Content-Type": "application/json"}

model_vision = "gemini-pro-vision"
url_vision = f"https://googleapis.fmr.wiki/v1beta/models/{model_vision}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"

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
        print(history)
        return "no content"
    reply = item['candidates'][0]['content']
    history.append(reply)
    return reply['parts'][0]['text']

def vision(prompt: str, image_data: bytes)->str:
    data = {
        "contents": [{
            "parts":[{
                "text": prompt
            }, {
                "inline_data": {
                    "mime_type":"image/jpeg",
                    "data": base64.b64encode(image_data).decode("utf-8")
                }
            }]
        }]
    }
    ret = requests.post(url_vision, json.dumps(data), headers=headers)
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
    return reply['parts'][0]['text']

def main():
    bot = TeleBot(os.getenv("XGOOBOT_TOKEN"))
    print("bot init done.")
    sessions = {}

    @bot.message_handler(regexp='(?!/).+')
    def gemini(message: Message) -> None:
        reply_message = bot.reply_to(
            message,
            "Generating google gemini answer please wait, only keep the last ten messages"
        )
        print(f"{message.from_user.id}({message.from_user.first_name}): {message.text}")
        session = None
        # restart will lose all TODO
        if str(message.from_user.id) not in sessions:
            session = new_session()
            sessions[str(message.from_user.id)] = session
        else:
            session = sessions[str(message.from_user.id)]
        print(len(session["history"]))
        if len(session["history"]) > 20:
            session["history"] = session["history"][2:]
        if session["history"] and session["history"][-1]["role"] == "user":
            #session["history"][-1]["parts"].append({"text": message.text})
            session["history"][-1]["parts"] = [{"text": message.text}]
        else:
            session["history"].append({"role":"user", "parts":[{"text": message.text}]})
        try:
            bot.reply_to(message, chat(session["history"]))
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, "Something wrong please check the log")
        bot.delete_message(reply_message.chat.id, reply_message.message_id)

    @bot.message_handler(content_types=["photo"])
    def gemini_image_handler(message: Message) -> None:
        s = message.caption
        if not s: return
        reply_message = bot.reply_to(
            message,
            "Generating google gemini vision answer please wait"
        )
        try:
            max_size_photo = max(message.photo, key=lambda p: p.file_size)
            file_path = bot.get_file(max_size_photo.file_id).file_path
            print(file_path)
            downloaded_file = bot.download_file(file_path)
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, "Something is wrong with reading your image")
        image_data = open("gemini_temp.jpg", "rb").read()
        try:
            bot.reply_to(message, vision(s, downloaded_file))
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, "Something wrong please check the log")
        bot.delete_message(reply_message.chat.id, reply_message.message_id)


    print("starting telegram bot.")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
