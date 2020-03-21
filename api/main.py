from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'message': '你已经正确创建FastApi服务！'}

@app.get('/items/{item_id}')
async def read_item(item_id: int):
    return {'item_id': item_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get('/item/')
def get_item(skip: int=0, limit: int=10):
    return fake_items_db[skip: skip+limit]
