import urllib.request
import fitz
import os, re
import numpy as np
import openai
import gradio as gr
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

def pdf_to_text(path, start_page=1, end_page=None):
    doc = fitz.open(path)
    total_pages = doc.page_count
    if end_page is None: end_page = total_pages
    
    text_list = []
    for i in range(start_page-1, end_page):
        page = doc.load_page(i)
        text = page.get_text("text").replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)
        text_list.append(text)
    
    doc.close()
    return text_list

def text_to_chunks(texts, word_length=150, start_page=1):
    text_toks = [t.split(' ') for t in texts]
    chunks = []
    
    for idx, words in enumerate(text_toks):
        for i in range(0, len(words), word_length):
            chunk = words[i:i+word_length]
            if (i+word_length) > len(words) and (len(chunk) < word_length) and (
                len(text_toks) != (idx+1)):
                text_toks[idx+1] = chunk + text_toks[idx+1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'[{idx+start_page}]' + ' ' + '"' + chunk + '"'
            chunks.append(chunk)
    return chunks

class SemanticSearch:
    
    def __init__(self):
        self.model = SentenceTransformer('/Users/zliu/models/distiluse-base-multilingual-cased-v1')
        self.fitted = False
        
    
    def fit(self, data, batch=1000, n_neighbors=5):
        print("Fitting...")
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True
    
    
    def __call__(self, text, return_data=True):
        inp_emb = self.model.encode([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]
        
        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors
    
    
    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i:(i+batch)]
            emb_batch = self.model.encode(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings

def load_recommender(path, start_page=1):
    global recommender
    pdf_file = os.path.basename(path)
    embeddings_file = f"{pdf_file}_{start_page}.npy"
    
    '''
    if os.path.isfile(embeddings_file):
        embeddings = np.load(embeddings_file)
        recommender.embeddings = embeddings
        recommender.fit2(n_neighbors=5)
        return "Embeddings loaded from file"
    '''
    
    texts = pdf_to_text(path, start_page=start_page)
    chunks = text_to_chunks(texts, start_page=start_page)
    recommender.fit(chunks)
    np.save(embeddings_file, recommender.embeddings)
    return 'Corpus Loaded.'
    
def generate_text(openAI_key, prompt, engine="gpt-3.5-turbo"):
    openai.api_key = openAI_key
    openai.api_base = "https://openai.fmr.wiki/v1"
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}]
    
    completions = openai.ChatCompletion.create(
        model=engine,
        messages=messages,
        max_tokens=512,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = completions.choices[0].message['content']
    return message

def generate_answer(question, openAI_key):
    topn_chunks = recommender(question)
    prompt = ""
    prompt += 'search results:\n\n'
    for c in topn_chunks:
        prompt += c + '\n\n'
        
    prompt += "Instructions: Compose a comprehensive reply to the query using the search results given. "\
              "Cite each reference using [ Page Number] notation (every result has this number at the beginning). "\
              "Citation should be done at the end of each sentence. If the search results mention multiple subjects "\
              "with the same name, create separate answers for each. Only include information found in the results and "\
              "don't add any additional information. Make sure the answer is correct and don't output false content. "\
              "If the text does not relate to the query, simply state 'Text Not Found in PDF'. Ignore outlier "\
              "search results which has nothing to do with the question. Only answer what is asked. The "\
              "answer should be short and concise. Answer step-by-step. \n\n"
    
    prompt += f"Query: {question}\nAnswer:"
    answer = generate_text(openAI_key, prompt)
    return answer


def question_answer(file, question, openAI_key):
    if openAI_key.strip()=='':
        return '[ERROR]: Please enter you Open AI Key. Get your key here : https://platform.openai.com/account/api-keys'
    if file == None:
        return '[ERROR]: Both URL and PDF is empty. Provide atleast one.'

    old_file_name = file.name
    file_name = file.name
    file_name = file_name[:-12] + file_name[-4:]
    os.rename(old_file_name, file_name)
    load_recommender(file_name)

    if question.strip() == '':
        return '[ERROR]: Question field is empty'

    return generate_answer(question,openAI_key)

recommender = SemanticSearch()
title = '# PDF GPT'
description = """## What is PDF GPT ?
1. The problem is that Open AI has a 4K token limit and cannot take an entire PDF file as input. Additionally, it sometimes returns irrelevant responses due to poor embeddings. ChatGPT cannot directly talk to external data. The solution is PDF GPT, which allows you to chat with an uploaded PDF file using GPT functionalities. The application breaks the document into smaller chunks and generates embeddings using a powerful Deep Averaging Network Encoder. A semantic search is performed on your query, and the top relevant chunks are used to generate a response.
2. The returned response can even cite the page number in square brackets([]) where the information is located, adding credibility to the responses and helping to locate pertinent information quickly. The Responses are much better than the naive responses by Open AI."""

with gr.Blocks() as demo:
    
    gr.Markdown(title)
    gr.Markdown(description)
    
    with gr.Row():
        with gr.Group():
            openAI_key=gr.Textbox(label='Enter your OpenAI API key here')
            file = gr.File(label='Upload your PDF/ Research Paper / Book here', file_types=['.pdf'])
            question = gr.Textbox(label='Enter your question here')
            btn = gr.Button(value='Submit')
            btn.style(full_width=True)
        
        with gr.Group():
            answer = gr.Textbox(label='The answer to your question is :')
        
        btn.click(question_answer, inputs=[file, question, openAI_key], outputs=[answer])
demo.launch(server_port=8080)
