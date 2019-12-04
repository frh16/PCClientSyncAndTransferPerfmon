# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class CreateSyncBox(BasePage):

    img_folder_name = 'create_sync_box'

    @classmethod
    def click_folder_my_space(cls):
        cls.touch('box_folder_small_my_space.png', is_common_img=True)

    @classmethod
    def double_click_folder_my_space(cls):
        cls.double_click('box_folder_small_my_space.png', is_common_img=True)

    @classmethod
    def click_advance_setting(cls):
        cls.touch('btn_advance_setting.png')

    @classmethod
    def double_click_folder_download(cls):
        cls.double_click('folder_download_client.png', is_common_img=True)

    @classmethod
    def click_folder_100(cls):
        cls.touch('folder_100_client.png', is_common_img=True)

    @classmethod
    def click_change_path(cls):
        cls.touch('btn_change_path.png', is_common_img=True)

    # @classmethod
    # def click_btn_ok(cls):
    #     cls.touch('btn_ok_white.png', is_common_img=True)

if __name__ == '__main__':
    print('a')
