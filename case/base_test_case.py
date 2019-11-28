import unittest
import airtest.report.report as report
from airtest.core.api import *
from common.config import Config
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
from common.utils.time import get_time
from common.utils.file import *


class TestCaseBase(unittest.TestCase):

    testCaseID = 12345679

    @classmethod
    def setUp(cls):
        print("setup start")

        if not cli_setup():
            if(Config.RUN_TIME == 0):
                Config.RUN_TIME = get_time()
            mkdir(Config.get_log_dir())
            log_dir = os.path.join(Config.get_log_dir(), str(cls.testCaseID))
            auto_setup(__file__, logdir=log_dir, devices=[
                "Windows:///",
            ])

        print("setup end")

    @classmethod
    def tearDown(cls):
        print('teardown start')

        log_dir = os.path.join(Config.get_log_dir(), str(cls.testCaseID))
        # this file is used for report.LogToHtml, get name, path from it, the content is unuseful
        fake_script = os.path.join(log_dir, 'fake.py')
        create_file(fake_script)
        output_file = os.path.join(log_dir, 'log.html')
        rpt = report.LogToHtml(fake_script, log_dir)
        rpt.report(report.HTML_TPL, output_file=output_file)

        print('teardown end')


if __name__ == '__main__':
    # log_dir = os.path.join(Config.get_log_dir(), str(TestCaseBase.testCaseID))
    # print(log_dir)
    if (Config.RUN_TIME == 0):
        Config.RUN_TIME = get_time()
    log_dir = os.path.join(Config.get_log_dir(), str(TestCaseBase.testCaseID))
    mkdir(log_dir)
    fake_script = os.path.join(log_dir, 'fake.py')
    create_file(fake_script)
    # log = 'D:\\work\\workspace\\PycharmProjects\\LDVirtualBoxAutoTest\\log\\20191016224248\\111'
    # output_file = log + '\\' + 'log.html'
    # rpt = report.LogToHtml(script, log)
    # rpt.report(report.HTML_TPL, output_file=output_file)
