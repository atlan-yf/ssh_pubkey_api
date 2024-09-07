from cryptography.fernet import Fernet
from pyotp import TOTP, random_base32

from datetime import datetime

class Checker:
    def __init__(self):
        self._fernet_key = Fernet.generate_key()
        self._last_gen_time = datetime.now()
        self._known_r = {}

    def _clear_outdated_r(self):
        for r in list(self._known_r.keys()):
            if (datetime.now() - self._known_r[r]).total_seconds() > 1200:
                del self._known_r[r]

    def gen_pass(self, pubkey: str) -> tuple[str, str, str]:
        '''
        return:
            - Encrypted pubkey: str
            - Encrypted OTP: str
            - Encrypted random: str
        '''

        if (datetime.now() - self._last_gen_time).total_seconds() < 1200:
            self._fernet_key = Fernet.generate_key() # reset key every 20 minutes
        self._clear_outdated_r()

        locker = Fernet(self._fernet_key)
        r = random_base32()
        OTP = TOTP(r, interval=1200).now() # 20 minutes
        self._known_r[r] = datetime.now()
        return locker.encrypt(pubkey.encode('utf-8')).decode('utf-8'), \
                locker.encrypt(OTP.encode('utf-8')).decode('utf-8'), \
                r
    
    def check_pass(self, pubkey: str, OTP: str, random: str) -> str | None:
        # make sure the same random is not used twice
        if random not in self._known_r:
            return None
        else:
            del self._known_r[random]
        
        locker = Fernet(self._fernet_key)
        try:
            pubkey = locker.decrypt(pubkey.encode('utf-8')).decode('utf-8')
            OTP = locker.decrypt(OTP.encode('utf-8')).decode('utf-8')
        except:
            return None
        
        return pubkey if TOTP(random, interval=1200).now() == OTP else None
