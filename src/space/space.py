#coding:utf-8

from common.log import LogWrapper
import os
import yaml
from common.http import Http
from common.util import Util
from abc import abstractmethod

class Space(object):
    def __init__(self, work_path, conf_file, domain='', cookie=''):
        self.work_path = work_path
        self.log=LogWrapper()
        self.config = {}
        with open(os.path.join(self.work_path, 'conf/feishu_config.yaml'), "r") as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            self.config.update(config)
        with open(os.path.join(self.work_path, 'conf/user_config.yaml'), "r") as fin:
            config = yaml.load(fin, Loader=yaml.FullLoader)
            self.config.update(config)
        self.url_dict = self.config.get('url', dict())
        self.cookie = self.config.get('cookie') if cookie == '' else cookie
        self.domain = self.config.get('domain') if domain == '' else domain
        self.http =Http(self.domain, self.cookie)
        self.output_folder = os.path.join(self.work_path, 'output')
        Util().mkdir_if_not_exist(self.output_folder)

    @abstractmethod
    def get_user(self, params):
        pass

    @abstractmethod
    def get_space_list(self, params):
        pass

    @abstractmethod
    def cd(self, op):
        pass
    
    @abstractmethod
    def pwd(self, logprint=True):
        pass

    @abstractmethod
    def init_user_folder(self):
        pass

    def init_cur_folder(self, path=None):
        if path is None:
            path = self.pwd(logprint=False)
        path = os.path.join(self.output_folder, path)
        Util().mkdir_if_not_exist(path)

    @abstractmethod
    def choose_space(self, idx_str):
        pass

    @abstractmethod
    def get_cur_dir(self, opt_l=False):
        pass