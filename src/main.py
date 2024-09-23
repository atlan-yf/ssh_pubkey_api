from flask import Flask, request, current_app
from urllib.parse import quote
import os

from util import verifyPubKey, addPubKey
from notifier import NotifierManager
from checker import Checker

app = Flask(__name__)

@app.route('/api/v1/submit', methods=['POST'])
def submit():
    if request.form['pubkey'] is None:
        return 'ERROR'
    else:
        pubkey = request.form['pubkey']
        if verifyPubKey(pubkey):
            pub, otp, rad = current_app.checker.gen_pass(pubkey)
            ver_url = request.host_url + 'api/v1/verify/' + quote(rad) + '?pk=' + quote(pub) + '&op=' + quote(otp)
            current_app.notifier.notify(ver_url)
            return 'OK'
        else:
            return 'ERROR'

@app.route('/api/v1/verify/<code>', methods=['GET'])
def verify(code):
    pk = request.args.get('pk')
    op = request.args.get('op')
    r = current_app.checker.check_pass(pk, op, code)
    if r:
        addPubKey(r)
        return 'OK<br/>The following pubkey has been added:<br/>' + r
    else:
        return 'ERROR'

if __name__ == '__main__':
    with app.app_context():
        if not os.path.isfile('pubkey.config'):
            raise FileNotFoundError('pubkey.config not found')
        app.notifier = NotifierManager('pubkey.config')
        app.checker = Checker()
    app.run(host='0.0.0.0', port=18581)