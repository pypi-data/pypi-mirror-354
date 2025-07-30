import requests

class Pushover:
    def __init__(self, token, key):
        self.token = token
        self.key = key
        self.url = "https://api.pushover.net/1/messages.json"

    def send_message(self, message):
        data = {
                "token": self.token,
                "user": self.key,
                "message": message
                }
        response = requests.post(url = self.url, data = data)
        if response.status_code != 200:
            print(response)
