import os
from common import log, singleton

@singleton.singleton
class Util(object):
    def __init__(self):
        self.log = log.LogWrapper()

    def mkdir_if_not_exist(self, path):
        # TODO add log
        if not os.path.exists(path) or not os.path.isdir(path):
            os.makedirs(path)
            self.log.info('mkdir -p {}'.format(path)) 
        else:
            self.log.info('{} is already exist'.format(path)) 

    def idx_checker(self, op, min_range, max_range):
        idx = int(op)
        assert idx >= min_range and idx <= max_range, '超出可选范围 {} ~ {}'.format(min_range, max_range)
        return idx
        