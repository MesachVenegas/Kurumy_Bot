from flask import Flask
from threading import Thread

app =Flask('')


@app.route('/')
def home():
    return "Hola estoy en linea"


def run():
    app.run(host='0.0.0.0', port=8080)


def start_check():
    t = Thread(target=run)
    t.start()