#coding:utf-8
import os
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from space.space import Space
from common.log import LogWrapper
def help_info():
    info = \
"""
命令提示:
h / help: 查看本帮助
q / quit: 退出
user: 查看当前登录用户
show space: 查看知识库列表
use $idx: 选择某一本知识库，$idx必须为数字, 可以通过show space查看选项
ls [-l]: 查看当前目录
cd $idx: 进入子目录
cd ..: 返回上级目录
"""
    LogWrapper().info(info)

def user_run(handler):
     while True:
            try:
                input_list = input("FeishuExpoter>>> ").strip().split()
                if len(input_list) == 0:
                    continue
                LogWrapper().info('user input: {}'.format(input_list))
                if len(input_list) > 0 and (input_list[0] == 'q' or input_list[0] == 'quit'):
                    exit(0)
                elif len(input_list) > 0 and (input_list[0] == 'h' or input_list[0] == 'help'):
                    help_info()
                elif len(input_list) == 1 and input_list[0] == 'user':
                    handler.get_user()
                elif len(input_list) == 2 and input_list[0] == 'show' and input_list[1] == 'space':
                    handler.get_space_list()
                elif len(input_list) >= 1 and input_list[0] == 'ls':
                    opt_l = True if len(input_list) == 2 and input_list[1] == '-l' else False
                    handler.get_cur_dir(opt_l)
                elif len(input_list) == 2 and input_list[0] == 'use':
                    handler.choose_space(input_list[1])
                elif len(input_list) == 2 and input_list[0] == 'cd':
                    handler.cd(input_list[1])    
                else:
                    LogWrapper().error('option not define')
            except Exception as e:
                LogWrapper().error(str(e))


def main():
    domain = input('domain (已经添加到user_config可以直接回车): ')
    cookie = input('cookie (已经添加到user_config可以直接回车): ')
    try:
        handler = Space(os.getcwd(), domain, cookie)
        LogWrapper().info('查询已登录用户 ...')
        handler.get_user()
        LogWrapper().info('初始化输出目录 ...')
        handler.init_user_folder()
        LogWrapper().info('初始化知识库目录...')
        handler.get_space_list()
        LogWrapper().info('初始化完成!')
        help_info()
        user_run(handler)
    except AssertionError as e:
        LogWrapper().error(str(e))
if __name__ == "__main__":
    main()
    


        
    