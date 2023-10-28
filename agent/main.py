import autogen
import os
from dotenv import load_dotenv
_ = load_dotenv()

config_list = autogen.config_list_from_dotenv(
    dotenv_file_path=".env",
    model_api_key_map={
        "gpt-4": {
            "api_base": os.getenv("OPENAI_API_BASE"),
        },
        "gpt-3.5-turbo": {
            "api_base": os.getenv("OPENAI_API_BASE"),
        },
    },
    filter_dict={
        "model": {
            "gpt-4",
            "gpt-3.5-turbo",
        }
    },
)

print(config_list)

assistant = autogen.AssistantAgent("assistant", llm_config={"config_list": config_list})
user_proxy = autogen.UserProxyAgent("user_proxy", code_execution_config={"work_dir": "coding"})
# user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
user_proxy.initiate_chat(assistant, message="今天是农历什么日期？,还有几天过年？请告诉我答案")
