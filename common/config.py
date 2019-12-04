import os
from common.utils.time import get_time


project_name = 'PCClientSyncAndTransferPerfmon'

def get_root_dir():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find(project_name) + len(project_name)]
    return rootPath

class Config(object):
    RUN_TIME = get_time()

    CASE_FOLDER = 'case'
    LOG_FOLDER = 'log'

    IMG_FOLDER = 'img'
    IMG_PATH = os.path.join(get_root_dir(), IMG_FOLDER)

    TEMP_FOLDER = 'temp'
    TEMP_PATH = os.path.join(get_root_dir(), TEMP_FOLDER)

    DOWNLOAD_DIR = r'D:\_test_data_\download'

    @staticmethod
    def get_log_dir():
        return os.path.join(get_root_dir(), Config.LOG_FOLDER, str(Config.RUN_TIME))


if __name__ == '__main__':
    print(Config.IMG_PATH)