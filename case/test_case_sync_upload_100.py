import unittest
from case.base_test_case import TestCaseBase # .之前没有case，单独运行此case会报错，暂不知原因
from pages.tray import Tray
from manager.sync_manager import SyncManager

class TestCaseUpload100(TestCaseBase):
    testCaseID = '0.1k'

    def test_run(self):
        SyncManager.set_case_id(TestCaseUpload100.testCaseID)
        SyncManager.create_sync_local_to_cloud()





if __name__ == "__main__":
    # print(TestCaseBase.testCaseID)
    unittest.main()
