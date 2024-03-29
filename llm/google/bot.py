import os
import json
import base64
import traceback
import requests
import md2tgmd
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from telebot import TeleBot
from telebot.types import Message

model = "gemini-pro"
url = f"https://googleapis.fmr.wiki/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
headers = {"Content-Type": "application/json"}

model_vision = "gemini-pro-vision"
url_vision = f"https://googleapis.fmr.wiki/v1beta/models/{model_vision}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"


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

def vision(prompt: str, images: list)->str:
    data = {
        "contents": [{
            "parts":[{
                "text": prompt
            }] + [{
                "inline_data": {
                    "mime_type":"image/jpeg",
                    "data": base64.b64encode(image_data).decode("utf-8")
                }
            } for image_data in images]
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

    @bot.message_handler(commands=['start', 'clear'])
    def handle_start(message: Message) -> None:
        if str(message.from_user.id) in sessions:
            sessions[str(message.from_user.id)] = {"history": []}
        bot.reply_to(message, "Session cleared.")

    @bot.message_handler(regexp='(?!/).+')
    def gemini_chat_handler(message: Message) -> None:
        reply_message = bot.reply_to(
            message,
            "Generating google gemini answer please wait, only keep the last ten messages"
        )
        print(f"{message.from_user.id}({message.from_user.first_name}): {message.text}")
        session = None
        # restart will lose all TODO
        if str(message.from_user.id) not in sessions:
            session = {"history": []}
            sessions[str(message.from_user.id)] = session
        else:
            session = sessions[str(message.from_user.id)]
        print(len(session["history"]))
        if len(session["history"]) > 20:
            session["history"] = session["history"][2:]
        if session["history"] and session["history"][-1]["role"] == "user":
            session["history"][-1]["parts"] = [{"text": message.text}]
        else:
            session["history"].append({"role":"user", "parts":[{"text": message.text}]})
        
        reply = chat(session["history"])
        try:
            bot.reply_to(message, md2tgmd.escape(reply), parse_mode="MarkdownV2")
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, reply)
        bot.delete_message(reply_message.chat.id, reply_message.message_id)

    @bot.message_handler(content_types=["photo"])
    def gemini_image_handler(message: Message) -> None:
        s = message.caption
        if not s:
            s = "Please describe the image."
        reply_message = bot.reply_to(
            message,
            "Generating google gemini vision answer please wait"
        )
        try:
            max_size_photo = max(message.photo, key=lambda p: p.file_size)
            file_path = bot.get_file(max_size_photo.file_id).file_path
            print(file_path)
            images = [bot.download_file(file_path)]
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, "Something is wrong with reading your image")
        
        reply = vision(s, images)
        try:
            bot.reply_to(message, md2tgmd.escape(reply), parse_mode="MarkdownV2")
        except Exception as e:
            traceback.print_exc()
            bot.reply_to(message, reply)
        bot.delete_message(reply_message.chat.id, reply_message.message_id)

    print("starting telegram bot.")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
