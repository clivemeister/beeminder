import urllib
import requests
import configparser

# based on https://www.beeminder.com/api

class Beeminder:
    _base_url = 'https://www.beeminder.com/api/v1/'

    # Can initialise either from .ini file or via parameters
    def __init__(self, user="", token="", ini_file=""):
        if len(ini_file)>0:
            config = configparser.ConfigParser()
            config.read(ini_file)
            self.username = config['USER']['username']
            self.auth_token = config['USER']['auth_token']
        else:
            self.auth_token = token
            self.username = user

    def get_user(self):
        return self._call(f'users/{self.username}')

    def get_goals(self):
        return self._call(f'users/{self.username}/goals.json')

    def get_goal(self, goalname):
        result = self._call(f'users/{self.username}/goals/{goalname.strip()}.json')
        return result

    def get_datapoints(self, goalname):
        return self._call(f'users/{self.username}/goals/{goalname}/datapoints.json')

    def create_datapoint(self, goalname, timestamp, value, comment=' ', sendmail='false'):
        values = {'auth_token':self.auth_token, 'timestamp':timestamp, 'value':value, 'comment':comment, 'sendmail':sendmail}
        return self._call(f'users/{self.username}/goals/{goalname.strip()}/datapoints.json', data=values, method='POST')

    def update_road(self, goalname, new_roadall):
        slug = {"roadall": new_roadall}
        return self._call(f'users/{self.username}/goals/{goalname}.json', data=slug, method='PUT')

    def _call(self, endpoint, data=None, method='GET'):
        if data is None:
            data = {}

        if self.auth_token:
            data.update({'auth_token': self.auth_token})
        elif self._access_token:
            data.update({'access_token': self._access_token})

        url = f'{self._base_url}{endpoint}'
        result = None

        if method == 'GET':
            result = requests.get(url, data)

        if method == 'POST':
            result = requests.post(url, data)

        if method == 'PUT':
            result = requests.put(url, data)

        if not result.status_code == requests.codes.ok:
            raise Exception(f'API request {method} {url} failed with code {result.status_code}: {result.text}')

        # self._persist_result(endpoint, result)

        return None if result is None else result.json()
