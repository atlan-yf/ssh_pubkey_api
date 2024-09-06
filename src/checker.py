from cryptography.fernet import Fernet
from pyotp import TOTP, random_base32

class Checker:
    def __init__(self):
        self._fernet_key = Fernet.generate_key()

    def gen_pass(self, pubkey: str) -> tuple[str, str, str]:
        '''
        return:
            - Encrypted pubkey: str
            - Encrypted OTP: str
            - Encrypted random: str
        '''
        locker = Fernet(self._fernet_key)
        r = random_base32()
        OTP = TOTP(r, interval=1200).now() # 20 minutes
        return locker.encrypt(pubkey.encode('utf-8')).decode('utf-8'), \
                locker.encrypt(OTP.encode('utf-8')).decode('utf-8'), \
                r
    
    def check_pass(self, pubkey: str, OTP: str, random: str) -> str | None:
        locker = Fernet(self._fernet_key)
        try:
            pubkey = locker.decrypt(pubkey.encode('utf-8')).decode('utf-8')
            OTP = locker.decrypt(OTP.encode('utf-8')).decode('utf-8')
        except:
            return None
        
        if TOTP(random, interval=1200).now() == OTP:
            self._fernet_key = Fernet.generate_key() # reset key
            return pubkey
        else:
            return None