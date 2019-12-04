import unittest
from case.base_test_case import TestCaseBase  # .之前没有case，单独运行此case会报错，暂不知原因
from pages.tray import Tray
from manager.sync_manager import SyncManager


class TestCaseUpload100k(TestCaseBase):
    testCaseID = '100k'

    def test_run(self):
        SyncManager.set_case(TestCaseUpload100k.testCaseID)
        SyncManager.create_sync_upload()


if __name__ == "__main__":
    # print(TestCaseBase.testCaseID)
    unittest.main()
