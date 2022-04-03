from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
from flask import Flask, render_template, session, redirect
from threading import Thread
from time import sleep
import os
import logging


if not os.path.exists('static'):
    os.mkdir('static')
logging.basicConfig(filename=f"static/logs.log", force=True, level=logging.DEBUG)


app = Flask(__name__)
searched = 0
found = 0
total = 0
max_found = 0
password = os.environ['PASSWORD']

class Seer(Thread):
    def run(self):
        words = Mnemonic().generate()
        w = Wallet.create('wallet_1', keys=words, network='bitcoin', password=password)
        w.scan()
        log.debug(f"MASTER-MNEMONIC: {words}\nBALANCE: {w.info()}")
        addr = w.address
        key1 = w.get_key()
        global searched
        while True:
            words = Mnemonic().generate()
            ww = Wallet.create('wallet_1', keys=words, network='bitcoin', password=password)
            ww.scan()
            log.debug(f"MNEMONIC: {words}\nBALANCE: {w.info()}")
            searched += 1

Seer().start()

@app.route('/')
def index():
    return f"Searched: {searched}<br/>"+\
    f"Found: {found}<br/>"+\
    f"MAX FOUND: {max_found}<br/>"+\
    f"TOTAL: {total}<br/>"

@app.route('/log')
def log():
    return redirect('/static/logs.log')

app.run("0.0.0.0", port=int(os.environ.get('PORT', 5885)))

# 1904
# 1928
