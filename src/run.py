#coding:utf-8
import os
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from space.feishu import Feishu
from common.log import LogWrapper
import traceback
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
        cd : 返回上级目录
        view $idx: 查看目录下指定的文章(PDF)
        view . 查看当前的文章(PDF)
"""
    LogWrapper().info(info)

def user_run(handler):
     while True:
            try:
                op = input("FeishuExpoter>>> ").strip().split()
                if len(op) == 0:
                    continue
                LogWrapper().debug('user input: {}'.format(op))
                if (op[0] == 'q' or op[0] == 'quit') and len(op) == 1:
                    exit(0)
                elif (op[0] == 'h' or op[0] == 'help') and len(op) == 1:
                    help_info()
                elif op[0] == 'user' and len(op) == 1:
                    handler.get_user()
                elif op[0] == 'pwd' and len(op) == 1:
                    handler.pwd()
                elif op[0] == 'show' and op[1] == 'space'and len(op) == 2:
                    # FIXME 可能要考虑 > 24的分页情况
                    handler.show_space()
                elif op[0] == 'ls' and len(op) == 1:
                    handler.ls(False)
                elif op[0] == 'll' and len(op) == 1:
                    handler.ls(True)
                elif op[0] == 'use' and len(op) == 2:
                    handler.choose_space(op[1])
                elif op[0] == 'cd' and len(op) == 2:
                    handler.cd(op[1])
                else:
                    LogWrapper().error('option not define')
            except Exception as e:
                LogWrapper().debug(traceback.format_exc())
                LogWrapper().error(str(e))


def main():
    domain = input('domain (已经添加到user_config可以直接回车): ')
    cookie = input('cookie (已经添加到user_config可以直接回车): ')
    try:
        handler = Feishu(os.getcwd(), domain, cookie)
        LogWrapper().info('查询已登录用户 ...')
        handler.get_user()
        LogWrapper().info('初始化输出目录 ...')
        handler.init_user_folder()
        LogWrapper().info('初始化知识库目录...')
        handler.show_space()
        LogWrapper().info('初始化完成!')
        help_info()
        user_run(handler)
    except AssertionError as e:
        LogWrapper().debug(traceback.format_exc())
        LogWrapper().error(str(e))
if __name__ == "__main__":
    main()
    


        
    