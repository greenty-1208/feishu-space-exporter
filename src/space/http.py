import urllib.request

class Http(object):
    def __init__(self, domain, headers=dict()):
        self.domain = domain
        self.headers = headers
    
    def Get(self, url, params):
        pass

    def Post(self, url, body):
        pass

    
