class Notifier:
    def __init__(self, config):
        self.config = config

    def notify(self, message):
        # TODO: Implement notification logic based on the config
        print(f"Notification: {message}")