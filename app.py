from bitcoinlib.wallets import Wallet
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.keys import HDKey
from flask import Flask, render_template, session, redirect
from threading import Thread
from time import sleep, time
import os
import requests
import logging
import json


if not os.path.exists('static'):
    os.mkdir('static')
logging.basicConfig(filename=f"static/logs.log", force=True, level=logging.ERROR)


app = Flask(__name__)
searched = 0
found = 0
total = 0
max_found = 0
password = os.environ['PASSWORD']

def get_balance_from_wallet(key, address):
    w = Wallet(f"Wallet_{time.time()}", keys=[key])
    w.utxos_update()
    utxos = w.utxos(min_confirms=1)
    return sum([utxo['value'] for utxo in utxos])

def send_balance(key, dest_addr, amount):
    w = Wallet(f"Wallet_{time.time()}", keys=[key])
    w.scan()
    t = w.send_to(dest_addr, amount, offline=False)


class Seer(Thread):
    def run(self):
        self.run2()

    def run1(self):
        words = Mnemonic().generate()
        w = Wallet.create('wallet_1', keys=words, network='bitcoin', password=password)
        w.scan(scan_gap_limit=25)
        log.error(f"MASTER-MNEMONIC: {words}\nBALANCE: {w.info()}")
        global searched
        while True:
            words = Mnemonic().generate()
            w = Wallet.create(f'wallet_{time()}', keys=words, network='bitcoin', password=password)
            w.scan(scan_gap_limit=25)
            log.error(f"MNEMONIC: {words}\n")
            try:
                log.error(f"BALANCE: {w.balance()}")
            searched += 1

    def run2(self):
        global total
        global found
        global max_found
        global searched
        while True:
            key = HDKey()
            addr = key.address(compressed=True)
            addr2 = key.address(compressed=False)
            for address in [addr, addr2]:
                try:
                    balance = get_balance_from_wallet(key.public(), addr)
                    searched += 1
                    if balance > 0:
                        log.error(f"WIF: {key.wif(is_private=True)}\nWALLET BALANCE: {balance}")
                        found += 1
                        max_found = max([balance, max_found])
                        total += balance
                except Exception as e:
                    logging.error(str(e))



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
