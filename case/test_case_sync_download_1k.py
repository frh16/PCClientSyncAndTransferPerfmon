import unittest
from case.base_test_case import TestCaseBase  # .之前没有case，单独运行此case会报错，暂不知原因
from pages.tray import Tray
from manager.sync_manager import SyncManager


class TestCaseDownload1k(TestCaseBase):
    testCaseID = '1k'

    def test_run(self):
        SyncManager.set_case(TestCaseDownload1k.testCaseID, is_upload=False)
        SyncManager.create_sync_download()


if __name__ == "__main__":
    # print(TestCaseBase.testCaseID)
    unittest.main()
