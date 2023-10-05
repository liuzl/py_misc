from fastapi import FastAPI,Request
import g4f
from pydantic import BaseModel
import uvicorn
import click

app = FastAPI()


class Item(BaseModel):
    messages: list

@app.post("/v1/chat/completions")
async def root(item:Item):
    print(item.messages)
    messages = item.messages
    response = g4f.ChatCompletion.create(model=g4f.models.gpt_35_turbo, messages=messages)
    print(response)
    return response

@app.api_route("/{path_name:path}", methods=["GET","POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"], include_in_schema=False)
async def catch_all(request: Request, path_name: str):
    return {"request_method": request.method, "path_name": path_name}


@click.command
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, help="Port to bind to")
def main(host: str, port: int):
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()