# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Login(BasePage):

    @classmethod
    def click_btn_login(cls):
        # print('aa')
        # Login.touch('login_btn_login.png')
        cls.wait_then_touch('login_btn_login.png')

if __name__ == '__main__':
    print('a')
