import unittest
from case.base_test_case import TestCaseBase # .之前没有case，单独运行此case会报错，暂不知原因
from pages.tray import Tray

class TestCase(TestCaseBase):
    testCaseID = 111

    def test_run(self):
        Tray.click_tray_arrow()
        # Tray.click_tray_icon(right_click=True)







if __name__ == "__main__":
    # print(TestCaseBase.testCaseID)
    unittest.main()
