from configparser import ConfigParser

class CommandLineNotifier():
    def __init__(self, config: ConfigParser):
        try:
            self.hint = config.get('hint')
        except:
            self.hint = None

    def send_notification(self, message):
        if self.hint: print(self.hint)
        print(message)

this_cls = CommandLineNotifier # needed for manager to recognize the class