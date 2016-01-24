from flask import Flask
from flask import request
import xdb

app = Flask(__name__)
db = xdb.DB("db.xdb")

@app.route('/<key>')
def get(key):
    v = db.get(key)
    if v:
        return v
    else:
        return "not found", 404

@app.route('/<key>', methods=['POST'])
def set(key):
    v = request.form['v']
    if v:
        db.set(key, v)
        return "ok"
    else:
        return "empty value", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
