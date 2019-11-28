import unittest
from case.base_test_case import TestCaseBase # .之前没有case，单独运行此case会报错，暂不知原因

class TestCase(TestCaseBase):

    testCaseID = 222

    def test_run(self):
        print('2222222222222222')







if __name__ == "__main__":
    unittest.main()
