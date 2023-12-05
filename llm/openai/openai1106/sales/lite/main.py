import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from prompts import *

client = openai.OpenAI(api_key = os.getenv("OPENAI_API_KEY"), base_url = os.getenv("OPENAI_API_BASE"))

salesperson_name: str = "Ted Lasso"
salesperson_role: str = "Business Development Representative"
company_name: str = "Sleep Haven"
company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers."
company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service."
conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress."
conversation_type: str = "call"

history = []

step = 0

while step < 20:
    step += 1
    prompt = SALES_AGENT_PROMPT_TEMPLATE.format(
        salesperson_name=salesperson_name,
        salesperson_role=salesperson_role,
        company_name=company_name,
        company_business=company_business,
        company_values=company_values,
        conversation_purpose=conversation_purpose,
        conversation_type=conversation_type,
        conversation_history="\n".join(history),
        language="Chinese",
    )

    response = client.chat.completions.create(
        #model="gpt-3.5-turbo-1106",
        model="gpt-4-1106-preview",
        messages=[{
            "role": "user",
            "content": prompt,
        }]
    )
    reply = response.choices[0].message.content
    if "<END_OF_CALL>" in reply:
        print(reply.replace("<END_OF_CALL>", ""))
        break
    print(reply.replace("<END_OF_TURN>", ""))
    if "<END_OF_TURN>" not in reply:
        reply += " <END_OF_TURN>"
    history.append(salesperson_name+": "+reply)
    human_input = input("Your response: ")
    history.append("User: " + human_input + " <END_OF_TURN>")
    #print(response.model_dump_json(indent=2))
