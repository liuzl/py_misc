from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'message': '你已经正确创建FastApi服务！'}
