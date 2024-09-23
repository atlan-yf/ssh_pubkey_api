from configparser import ConfigParser

class NotifierManager:
    def __init__(self, configPath: str):
        with open(configPath, 'r') as f:
            self.config = ConfigParser()
            self.config.read_file(f)
            self.config.items
        self.notifiers = {}
        self.load_notifiers()

    def load_notifiers(self):
        import importlib
        for sec in self.config.sections():
            try:
                notifier_mod = importlib.import_module(f'mynotifiers.{sec}')
                self.notifiers[sec] = notifier_mod.this_cls(self.config[sec])
                print(f"Loaded notifier: {sec}")
            except ImportError as e:
                print(f"Failed to load notifier {sec}\n{e}")

    def notify(self, message):
        for notifier in self.notifiers.values():
            notifier.send_notification(message)

class Notifier:
    def __init__(self, config: ConfigParser):
        self.config = config

    def send_notification(self, message):
        pass