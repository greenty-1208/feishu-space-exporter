#coding:utf-8

import os
from traceback import print_exc
import yaml

class Space(object):
    def __init__(self, work_path, domain='', cookie=''):
        self.work_path = work_path
        self.config = {}
        with open(os.path.join(self.work_path, 'conf/common_config.yaml'), "r") as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            self.config.update(config)
        with open(os.path.join(self.work_path, 'conf/user_config.yaml'), "r") as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            self.config.update(config)
        print(self.config)
        if cookie != '':
            self.config['cookie'] = cookie
        if domain != '':
            self.config['domain'] = domain
        assert self.conf_check(('domain', 'cookie')) == True
        
        self.url_dict = self.config.get('url', dict())
    
    def conf_check(self, params):
        for param in params:
            assert self.config.get(param) is not None, '{} not in config'.format(param)
        return True

    def get_user(self, params):
        url = self.url_dict.get('user', None)
        assert url != None, 'userinfo url not define in config'
    
    def get_space_list(self, params):
        url = self.url_dict.get('space_list', None)
        assert url != None, 'space_list url not define in config'

    def get_space_info(self, params):
        url = self.url_dict.get('space_info', None)
        assert url != None, 'space_info url not define in config'

    def get_node_child(self, params):
        url = self.url_dict.get('node_child', None)
        assert url != None, 'node_child url not define in config'