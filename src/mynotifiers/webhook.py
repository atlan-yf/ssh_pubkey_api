from configparser import ConfigParser
from requests import request

class WebhookNotifier():
    def __init__(self, config: ConfigParser):
        try:
            self.url = config.get('url')
            self.title = config.get('title')
            self.title_key = config.get('title_key')
            self.message_key = config.get('message_key')
        except:
            raise Exception('Webhook notifier requires url and title')

    def send_notification(self, message):
        request('POST', self.url, json={self.title_key: self.title, self.message_key: message})

this_cls = WebhookNotifier # needed for manager to recognize the class