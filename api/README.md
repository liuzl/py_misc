# 用python做http接口服务

取代Flask的利器：FastApi

## 安装

```sh
pip install fastapi
pip install uvicorn
```

## 示例

代码：

```python
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def index():
    return {'message': '你已经正确创建FastApi服务！'}
```

运行：

```sh
uvicorn main:app --reload
```
