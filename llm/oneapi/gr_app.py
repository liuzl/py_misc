import gradio as gr
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")

import gradio as gr 
import json

def transcribe_audio(audio_path, prompt: str) -> str:
    with open(audio_path, 'rb') as audio_data:
        transcription = openai.Audio.transcribe("whisper-1", audio_data, prompt=prompt)
        print(json.dumps(transcription, ensure_ascii=False))
        return transcription['text']

def SpeechToText(audio):
    if audio == None : return "" 
    return transcribe_audio(audio, "Transcribe the following audio into Chinese: \n\n")


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox()
        mic = gr.Audio(source="microphone", type="filepath")
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        chat_history.append((message, message))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

    def get_chatbot_response(x, history):
        if x is None: return x, history
        print(history)
        os.rename(x, x + '.wav')
        history.append(((x + '.wav',), None))
        history.append((SpeechToText(x + '.wav') ,None))
        return x + '.wav', history

    mic.change(get_chatbot_response, [mic, chatbot], [mic, chatbot])

if __name__ == "__main__":
    demo.launch()

