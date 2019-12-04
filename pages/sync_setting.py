# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class SyncSetting(BasePage):

    img_folder_name = 'sync_setting'

    @classmethod
    def click_btn_upload_sync(cls):
        cls.touch('sync_setting_btn_upload_sync.png')

    @classmethod
    def click_btn_download_sync(cls):
        cls.touch('sync_setting_btn_download_sync.png')

    # @classmethod
    # def click_btn_ok(cls):
    #     cls.touch('btn_ok_gray.png', is_common_img=True)

if __name__ == '__main__':
    print('a')
