# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage


class Download(BasePage):

    @classmethod
    def click_btn_browse(cls):
        cls.touch('download_btn_browse.png')

    @classmethod
    def click_btn_download(cls):
        cls.touch('download_btn_download.png')


if __name__ == '__main__':
    print('a')
