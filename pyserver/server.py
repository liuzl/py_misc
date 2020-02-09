import requests
import json
from flask import Flask, request, Response
app = Flask(__name__, static_folder='ui', static_url_path='')

@app.route("/api", methods=['GET', 'POST'])
def get():
    if request.method == "POST": r = request.form
    else: r = request.args
    t = r.get('text', '')
    if t == "":
        return Response(json.dumps({'status':"error", 'message':"empty input"}))
    return Response(json.dumps({'status':"ok", 'message':t}, ensure_ascii=False),
            mimetype="application/json")


@app.route('/')
def index():
    return app.send_static_file('index.html')#

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002, debug=True)
