from bot.config import ReportBotConfig
import requests


DEFAULT_CONFIG_FILENAME = 'config/bot.conf'


class ReportBot(object):
    def __init__(self, conf_file=DEFAULT_CONFIG_FILENAME):
        self.conf = ReportBotConfig(conf_file)
        self.container_url = self.conf.resource.get_container_url()

    def post(self):
        url = self.conf.dooray.hook_url
        data = self._make_data()
        header = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=header)
        if response.status_code == 200:
            print(data)
            return 'OK'

    def _make_data(self):
        return {
            'botName': self.conf.bot.get_name(),
            'botIconImage': self.conf.resource.get_face_url(),
            'text': self._get_message()
        }

    def _get_message(self):
        message = self.conf.bot.get_message() + '\n'
        message += self.conf.resource.get_pic_url()
        return message
