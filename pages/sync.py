# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class Sync(BasePage):

    window_class_name = 'CShowSyncWnd'

    @classmethod
    def click_sync_local_folder(cls):
        cls.touch('sync_btn_sync_local_folder.png')

    @classmethod
    def click_first_sync_box(cls):
        cls.touch('sync_first_sync_box.png', target_pos=9)

    @classmethod
    def click_btn_delete(cls):
        cls.touch('sync_btn_delete.png')

    @classmethod
    def click_btn_detail(cls):
        cls.touch('sync_btn_detail.png')

    @classmethod
    def click_btn_create_sync(cls):
        cls.touch('sync_btn_create_sync.png')

    @classmethod
    def click_btn_sync_cloud_folder(cls):
        cls.touch('sync_btn_sync_cloud_folder.png')


if __name__ == '__main__':
    print('a')
