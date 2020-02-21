import requests

class Browser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        self.login_data ={
            'username': 'test_teacher',
            'password': 'test_teacher'
        }
        self.session = None

    def createSession(self):
        try:
            self.session = requests.Session()
        except:
            print('Exception in creating session')
        return self.session

    def get(self,  url):
        resp = None
        try:
            resp = self.session.get(url, headers = self.headers, allow_redirects=True)
        except:
            print('Exception in get ', url)
        return  resp

    def post(self, url, data):
        resp = None
        try:
            resp =self.session.post(url, data=data, headers = self.headers)
        except:
            print('Exception in post  ', url)
        return resp


    def Login(self, url, login_data=None):
        if not login_data:
            login_data = self.login_data
        return self.post(url,login_data)
