# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Main(BasePage):

    window_class_name = 'CMainWndWeb_Private'

    @classmethod
    def click_left_btn_sync(cls):
        cls.touch('main_left_sync.png')

    @classmethod
    def click_left_btn_my_space(cls):
        cls.touch('main_left_my_space.png')

    @classmethod
    def click_left_btn_transfer_list(cls):
        cls.touch('main_left_transfer_list.png')

    #################################RIGHT##################

    @classmethod
    def double_click_right_folder_download(cls):
        cls.double_click('folder_download_main.png', is_common_img=True)

    @classmethod
    def click_folder_100(cls):
        cls.touch('folder_100_main.png', is_common_img=True)

    @classmethod
    def click_folder_1k(cls):
        cls.touch('folder_1k_main.png', is_common_img=True)

    @classmethod
    def click_left_btn_download(cls):
        cls.touch('main_btn_download.png')





if __name__ == '__main__':
    print('a')
