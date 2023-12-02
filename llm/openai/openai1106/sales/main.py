import argparse
import json
import os
import sys

from langchain.chat_models import ChatLiteLLM

from salesgpt.agents import SalesGPT

import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = os.getenv("OPENAI_API_BASE")


if __name__ == "__main__":
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Description of your program")

    # Add arguments
    parser.add_argument(
        "--config", type=str, help="Path to agent config file", default=""
    )
    parser.add_argument("--verbose", type=bool, help="Verbosity",
                        default=False)
    parser.add_argument(
        "--max_num_turns",
        type=int,
        help="Maximum number of turns in the sales conversation",
        default=10,
    )

    # Parse arguments
    args = parser.parse_args()

    # Access arguments
    config_path = args.config
    verbose = args.verbose
    max_num_turns = args.max_num_turns

    llm = ChatLiteLLM(temperature=0.2, model_name="gpt-3.5-turbo-instruct")

    if config_path == "":
        print("NO")
        sys.exit()
    else:
        with open(config_path, "r", encoding="UTF-8") as f:
            config = json.load(f)
        print(f"Agent config {config}")
        sales_agent = SalesGPT.from_llm(llm, verbose=verbose, **config)

    sales_agent.seed_agent()
    print("=" * 10)
    cnt = 0
    while cnt != max_num_turns:
        cnt += 1
        if cnt == max_num_turns:
            print("Maximum number of turns reached - ending the conversation.")
            break
        sales_agent.step()

        # end conversation
        if "<END_OF_CALL>" in sales_agent.conversation_history[-1]:
            print("Sales Agent determined it is time to end the conversation.")
            break
        human_input = input("Your response: ")
        sales_agent.human_step(human_input)
        print("=" * 10)
