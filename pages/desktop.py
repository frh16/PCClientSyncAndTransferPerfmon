# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Desktop(BasePage):

    @classmethod
    def click_shortcut(cls):
        cls.touch('desktop_shortcut.png')

    @classmethod
    def open_soft(cls):
        cls.click_shortcut()
        cls.keyevent('{ENTER}')

if __name__ == '__main__':
    print(Tray.get_img_path())
