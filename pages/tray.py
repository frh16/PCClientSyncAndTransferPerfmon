# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Tray(BasePage):

    @classmethod
    def click_tray_arrow(cls):
        cls.touch('tray_arrow.png')

    @classmethod
    def click_tray_icon(cls, right_click=False):
        cls.touch('tray_icon.png', right_click=right_click)


if __name__ == '__main__':

    # print(Tray.get_img_path())
    Tray.touch('tray_arrow.png')
