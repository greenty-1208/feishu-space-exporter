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

        self.type_view = {
            'doc': 'docs',
            'dox': 'docx',
            'bas': 'bitable',
            'bmn': 'mind',
            'box': 'upload'

        }

        self.user = None # 用户信息缓存
        self.space_list = [] # 知识库列表
        self.now_space_id = None
        self.now_token = None
        self.sons = [] # 当前目录的子目录列表
        self.fa = dict() # 当前目录的父目录列表, 根目录等于None
        self.doc_info = dict() # 文档信息映射 key: token value: tuple(name, type)

    def get_user(self, params=''):
        """
            获取用户信息
            在线查询，有本地缓存
        """
        if self.user is None:
            url = self.url_dict.get('user', None)
            assert url is not None, 'user url not define in config'
            data = self.http.Get(url)
            self.user = {
                'user_name': data['cn_name'], 
                'tenant': data['tenant_name']
            }
        self.log.info('tenant: {}'.format(self.user['tenant']))
        self.log.info('user: {}'.format(self.user['user_name']))
        
    def set_doc_info(self, token, info):
        self.doc_info[token] = info

    def doc_name(self, token):
        name = self.doc_info[token][0]
        return name if name != '' else '未命名'

    def doc_type(self, token):
        doc_type = self.doc_info[token][1]
        return self.type_view.get(doc_type,'unknown')

    def show_space(self,params={'size':24}):
        """
            打印知识库列表
            更新space_list
            更新fa

        """
        url = self.url_dict.get('space_list', None)
        assert url is not None, 'space_list url is not in feishu_config'
        data = self.http.Get(url, params=params)
        self.space_list = []
        title_list = []
        for idx, space in enumerate(data['spaces']):
            self.space_list.append((space['space_id'], space['root_token']))
            self.fa[space['root_token']] = None
            self.set_doc_info(space['root_token'], (space['space_name'], 'book'))
            title_list.append(str(idx)+"::"+space['space_name'])
        self.log.info('\n'+'\n'.join(title_list))
        

    def choose_space(self, idx_str):
        """
            更新now_space_id, now_token
            创建当前目录
        """
        idx = Util().idx_checker(idx_str, 0, len(self.space_list)-1)

        self.now_space_id, self.now_token = self.space_list[idx]
        self.log.info('chose {}'.format(self.doc_name(self.now_token)))
        self.init_cur_folder(self.pwd())
        self.ls()

    def ls(self, opt_l=False):
        """
            在线查询当前目录的子目录列表并打印
            更新当前目录的sons列表
            更新子目录 info
        """
        assert self.now_space_id is not None, '未选择space'
        url = self.url_dict.get('child_list', None)
        assert url is not None, 'child_list url is not in feishu_config'
        params = {
            'space_id': self.now_space_id,
            'wiki_token': self.now_token
        }
        data = self.http.Get(url, params=params)
        self.sons = []
        title_list = []
        for idx, d in enumerate(data[self.now_token]):
            self.sons.append(d['wiki_token'])
            self.set_doc_info(d['wiki_token'], (d['title'], d['obj_token'][0:3]))
            if opt_l is True:
                title = '{}::\t{}\t{}'.format(str(idx), self.doc_type(d['wiki_token']), self.doc_name(d['wiki_token']))
            else:
                title = '{}::【{}】{}'.format(str(idx), self.doc_type(d['wiki_token']), self.doc_name(d['wiki_token']))
            if d['has_child'] is True:
                title += '/'
            title_list.append(title)

        if opt_l is True:
            self.log.info('\n'+'\n'.join(title_list))
        else:
            self.log.info('    '.join(title_list))

    def cd(self, op):
        """
            更新now_token
            进入子目录的情况
                更新当前目录的fa
                新建当前目录
        """
        assert self.now_space_id is not None, '未选择space'
        if op == '..':
            nex_token = self.fa[self.now_token]
        else:
            idx = Util().idx_checker(op, 0, len(self.sons)-1)
            nex_token = self.sons[idx]
            self.fa[nex_token] = self.now_token

        if nex_token is None:
            self.log.warning('当前已经是根目录')
        else:
            self.now_token = nex_token
            self.init_cur_folder(self.pwd())

    def pwd(self, logprint=True):
        """
            返回token的路径
            输出文件名的路径
        """
        names = []
        tokens = []
        now = self.now_token
        while now is not None:
            names.append(self.doc_name(now))
            tokens.append(now)
            now = self.fa[now]
        
        if logprint:
            self.log.info('当前目录: {}'.format('/'.join(list(reversed(names)))))
        return '/'.join(list(reversed(tokens)))



    def init_user_folder(self):
        self.output_folder = os.path.join(self.output_folder, self.user['tenant'])
        Util().mkdir_if_not_exist(self.output_folder)


    def export(self, token):
        pass
        

    