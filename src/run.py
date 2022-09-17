#coding:utf-8
import os
import sys
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from traceback import print_exc
from space.class_def import Space
if __name__ == "__main__":
    domain = input('domain (enter to use user_config setting): ')
    cookie = input('cookie (enter to use user_config setting): ')
    try:
        Space(os.getcwd(), domain, cookie)
    except AssertionError as e:
        print(e)
    # while True:
    #     print("input",end=': ')
    #     input_list = input().strip().split()
    #     print("your input",end=': ')
    #     print(input_list)
    #     if input_list[0] == 'q' or input_list[0] == 'quit':
    #         exit(0)


        
    