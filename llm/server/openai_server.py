import uvicorn
import click
from typing import List, Any
from llama_cpp.server.app import create_app, Settings
from llama_cpp import llama_types
from llama_cpp.llama_chat_format import ChatFormatterResponse, register_chat_format

@register_chat_format("zephyr")
def format_zephyr(
    messages: List[llama_types.ChatCompletionRequestMessage],
    **kwargs: Any,
) -> ChatFormatterResponse:
    _template = "<|{role}|>\n{message}</s>\n"
    _prompt = "".join([_template.format(role=msg["role"], message=msg["content"]) for msg in messages])
    _prompt += "<|assistant|>\n"
    print(_prompt)
    return ChatFormatterResponse(prompt=_prompt)

@click.command()
@click.option("--model", default="zephyr-7b-beta-Q4_K_M.gguf", type=str, required=True)
@click.option("--chat-format", default="zephyr", type=str, required=True)
@click.option("--verbose", type=bool, default=False)
@click.option("--cache", type=bool, default=False)
@click.option("--port", type=int, default=2001)
@click.option("--host", type=str, default="0.0.0.0")
def main(model: str, chat_format: str, verbose: bool, cache: bool, port: int, host: str):
    settings = Settings(
        model=model,
        chat_format=chat_format,
        verbose=verbose,
        cache=cache,
    )
    app = create_app(settings=settings)
    uvicorn.run(app, host=host, port=port, log_level="info", reload=False)

if __name__ == "__main__":
    main()
