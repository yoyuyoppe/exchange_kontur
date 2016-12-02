import requests


class KonturApi():
    """
    Взаимодействует с веб-сервисом контура по средствам HTTP запросов. Для связи используется библиотека request
    """
    def __init__(self, url, login, password, key):
        self.url = url
        self.id_box = ''
        self.login = login
        self.password = password
        self.api_key = key
        self.token = ''

    def get_headers(self):
        str_auth = None
        if self.token and self.api_key:
            str_auth = 'KonturEdiAuth konturediauth_api_client_id=' + self.api_key + ', konturediauth_token=' + self.token
        else:
            str_auth = 'KonturEdiAuth konturediauth_api_client_id=' + self.api_key + ', konturediauth_login="' + self.login + '", konturediauth_password="' + self.password + '"'
        return {'Authorization': str_auth}

    def run_requests(self, url_method, type_request='', params={}):
        _value = None
        try:
            if type_request == 'get':
                r = requests.get(self.url + url_method, data=params, headers=self.get_headers())
            elif type_request == 'post':
                r = requests.post(self.url + url_method, data=params, headers=self.get_headers())
        except Exception as e:
            print('ERROR: %s' % e)

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print('ERROR: %s' % e)

        if 'Unauthorized'.lower() in r.text.lower():
            print(r.text)
            _value = None
        else:
            _value = r

        return _value
