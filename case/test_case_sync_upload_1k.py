import unittest
from case.base_test_case import TestCaseBase # .之前没有case，单独运行此case会报错，暂不知原因
from pages.desktop import Desktop

class TestCase(TestCaseBase):
    testCaseID = 1001

    def test_run(self):
        Desktop.click_shortcut()
        # Tray.click_tray_icon(right_click=True)







if __name__ == "__main__":
    print('a')
