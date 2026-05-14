from flask import Flask
from threading import Thread
import logging

app = Flask('')

@app.route('/')
def home():
    return "Clara Bot está Online e Operante! 🚀"

def run():
    # O Render e outras plataformas usam a porta 8080 ou a definida no ambiente
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
