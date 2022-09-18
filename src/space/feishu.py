#coding:utf-8

import os
import yaml
import json
from common.http import Http
from common.util import Util

from space.space import Space
class Feishu(Space):
    def __init__(self, work_path, domain='', cookie=''):
        conf_file = 'conf/feishu_config.yaml'
        super(Feishu, self).__init__(work_path, conf_file, domain, cookie)

        self.tenant_name = None
        self.user_name = None
        self.space_list = []
        self.now_space_id = None
        self.now_token = None
        self.token_list = []
        self.father_token_dict = dict()
        self.token_to_name = dict()

    def get_user(self, params=''):
        if self.tenant_name is None:
            url = self.url_dict.get('user', None)
            assert url is not None, 'user url not define in config'
            data = self.http.Get(url)
            self.user_name = data['cn_name']
            self.tenant_name = data['tenant_name']
        self.log.info('tenant: {}'.format(self.tenant_name))
        self.log.info('user: {}'.format(self.user_name))
        
    def get_space_list(self,params={'size':24}):
        url = self.url_dict.get('space_list', None)
        assert url is not None, 'space_list url is not in feishu_config'
        data = self.http.Get(url, params=params)
        spaces = data['spaces']
        self.space_list = []
        for space in spaces:
            self.space_list.append((space['space_id'], space['space_name'], space['root_token']))
            self.father_token_dict[space['root_token']] = None
            self.token_to_name[space['root_token']] = space['space_name']
        title_list = [str(idx)+'::'+d[1] for idx, d in  enumerate(self.space_list)]
        self.log.info('\n'+'\n'.join(title_list))
        

    def choose_space(self, idx_str):
        idx = Util().idx_checker(idx_str, 0, len(self.space_list)-1)
        self.now_space_id = self.space_list[idx][0]
        self.now_token=self.space_list[idx][2]
        self.log.info('chose {}'.format(self.space_list[idx][1]))
        self.get_cur_dir()

    def get_cur_dir(self, opt_l=False):
        assert self.now_space_id is not None, '未选择space'
        url = self.url_dict.get('child_list', None)
        assert url is not None, 'child_list url is not in feishu_config'
        params = {
            'space_id': self.now_space_id,
            'wiki_token': self.now_token
        }
        data = self.http.Get(url, params=params)
        self.token_list = []
        for d in data[self.now_token]:
            self.token_list.append((d['wiki_token'], d['title'], d['has_child']))
            self.father_token_dict[d['wiki_token']] = self.now_token
            self.token_to_name[d['wiki_token']] = d['title']
        title_list = [str(idx)+'::'+ (d[1]+'/' if d[2] is True else d[1]) for idx, d in  enumerate(self.token_list)]
        if opt_l is True:
            self.log.info('\n'+'\n'.join(title_list))
        else:
            self.log.info('    '.join(title_list))

    def cd(self, op):
        assert self.now_space_id is not None, '未选择space'
        idx = Util().idx_checker(op, 0, len(self.token_list)-1) if op != '..' else -1
        nex_token = self.father_token_dict[self.now_token] if idx == -1 else self.token_list[idx][0]
        if nex_token == self.now_token:
            self.log.warning('当前已经是根目录')
        else:
            self.now_token = nex_token
            self.init_cur_folder(self.pwd())

    def pwd(self, logprint=True):
        names = []
        now = self.now_token
        while now is not None:
            names.append(self.token_to_name[now])
            now = self.father_token_dict[now]
        tmp_iter = reversed(names)
        pwd_str = '/'.join(list(tmp_iter))
        if logprint:
            self.log.info('当前目录: {}'.format(pwd_str))
        return pwd_str



    def init_user_folder(self):
        self.init_cur_folder(self.tenant_name)

    def export(self, token):
        pass
        

    