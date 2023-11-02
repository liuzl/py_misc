import uvicorn
from typing import List, Any
from llama_cpp.server.app import create_app, Settings
from llama_cpp import llama_types
from llama_cpp.llama_chat_format import ChatFormatterResponse, register_chat_format

@register_chat_format("zephyr")
def format_zephyr(
    messages: List[llama_types.ChatCompletionRequestMessage],
    **kwargs: Any,
) -> ChatFormatterResponse:
    _template = {
        "system": "<|system|>\n{message}</s>\n",
        "user": "<|user|>\n{message}</s>\n",
        "assistant": "<|assistant|>\n{message}</s>\n",
    }
    
    _prompt= ""
    for message in messages:
        print(message)
        role = message["role"]
        if role in _template:
            _prompt += _template[role].format(message=message["content"])
    
    _prompt += "<|assistant|>\n"
    print(_prompt)
    return ChatFormatterResponse(prompt=_prompt)

if __name__ == "__main__":
    settings = Settings(
        model="/home/zliu/gpt/models/zephyr-7b-beta/ggml-model-Q4_K_M.gguf",
        model_alias="zephyr-7b-beta",
        chat_format="zephyr",
        verbose=True,
    )
    
    app = create_app(settings=settings)

    uvicorn.run(
        app, host="0.0.0.0", port=2001
    )
