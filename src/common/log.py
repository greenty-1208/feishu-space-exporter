#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import logging.handlers
import os
import time
from common import singleton



@singleton.singleton
class LogWrapper(object):
    def __init__(self):
        self.logger = logging.getLogger("")

        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}

        # 创建文件目录
        logs_dir = 'output/log'
        if not os.path.exists(logs_dir) or not os.path.isdir(logs_dir):
            os.makedirs(logs_dir)

        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        logfilename = '%s.log' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)

        # 设置输出格式
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        rotatingFileHandler.setFormatter(formatter)

        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)

        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(logging.NOTSET)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


def main():
    log_wrapper = LogWrapper()
    log_wrapper.debug("this is debug")
    log_wrapper.info("this is info")
    log_wrapper.debug("this is debug")
    log_wrapper.error("this is error")
    log_wrapper.warning("this is warning")


if __name__ == '__main__':
    main()