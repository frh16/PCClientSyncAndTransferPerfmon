# coding:utf-8
import unittest
import os
import sys
import importlib.util
import inspect
import HTMLTestRunner
from common.config import Config
from common.utils.time import get_time

from case.test_case_sync_upload_100 import TestCaseUpload100
from case.test_case_sync_upload_1k import TestCaseUpload1k
from case.test_case_sync_download_100 import TestCaseDownload100



def get_report_file_name():
    return "result_" + Config.RUN_TIME + ".html"


if __name__ == "__main__":

    Config.RUN_TIME = get_time()

    case_path = os.path.join(os.getcwd(), Config.CASE_FOLDER)
    path = os.path.abspath(case_path)
    sys.path.insert(0, path)

    suite = unittest.TestSuite()

    suite.addTest(TestCaseDownload100('test_run'))
    # suite.addTest(TestCaseUpload1k('test_run'))

    # files = os.listdir(Config.CASE_FOLDER)
    # for file in files:
    #     module_name = file.split('.')[0]
    #     if(module_name.startswith('test')):
    #         cur_module = importlib.import_module(module_name)
    #         for name, obj in inspect.getmembers(cur_module):
    #             if inspect.isclass(obj) and name == 'TestCase': # startwith
    #                 suite.addTest(obj('test_run'))

    # discover = unittest.defaultTestLoader.discover(path, pattern='test*.py')
    # suite = unittest.TestSuite()
    # suite.addTest(TestCase('test_run'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

    runner = unittest.TextTestRunner()
    runner.run(suite)



    # html报告文件路径
    # report_path = os.path.join(os.getcwd(), Config.LOG_FOLDER)
    # report_abspath = os.path.join(report_path, get_report_file_name())
    # airtest_log_path = Config.get_log_dir()
    # fp = open(report_abspath, "wb")
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
    #                                        title=u'自动化测试报告,测试结果如下：',
    #                                        description=u'用例执行情况：',
    #                                        detail_log_path=airtest_log_path)
    # runner.run(suite)
    # fp.close()
    sys.exit()