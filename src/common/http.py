import json
from urllib import request
import os
import sys
from common import log
class Http(object):
    def __init__(self, domain='', cookie=''):
        self.log=log.LogWrapper()
        assert domain != '', "domain is not set"
        assert domain.endswith('feishu.cn'), "domain is not end with feishu.cn"
        assert cookie != '', "cookie is not set"
        self.domain = domain
        self.headers = {'cookie': cookie}

    
    def Get(self, url, headers=dict(), params=dict()):
        param_str = '&'.join('{}={}'.format(k, v) for k,v in params.items())
        full_url = self.domain + url + '?' + param_str
        self.headers.update(headers)
        req = request.Request(url=full_url, headers=self.headers)
        
        try:
            r = request.urlopen(req)
            resp_str = r.read()
            resp = json.loads(resp_str)
            code  = resp.get('code')
            assert code == 0, 'http get code != 0, msg: {}'.format(resp.get('msg'))
            data = resp.get('data')
        except Exception as e:
            self.log.error('http get error | full_url: {} | e: {}'.format(full_url, str(e)))
        return data

    def Post(self, url, body):
        pass

    
