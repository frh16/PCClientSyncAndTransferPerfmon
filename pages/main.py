# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Main(BasePage):

    window_class_name = 'CMainWndWeb_Private'

    @classmethod
    def click_left_btn_sync(cls):
        cls.touch('main_left_sync.png')

if __name__ == '__main__':
    print('a')
