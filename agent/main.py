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