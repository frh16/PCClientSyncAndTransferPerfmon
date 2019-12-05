# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage


class SelectLocalFolderSyncToCloud(BasePage):

    @classmethod
    def click_this_computer(cls):
        cls.wait_then_touch('this_computer_small.png', is_common_img=True)

    @classmethod
    def click_drive_d(cls):
        cls.touch('drive_d.png', is_common_img=True)

    @classmethod
    def click_folder_test_data(cls):
        cls.touch('folder_test_data.png', is_common_img=True)
        # cls.keyevent('{DOWN}')

    @classmethod
    def click_folder_upload(cls):
        cls.touch('folder_upload.png', is_common_img=True)

    @classmethod
    def click_folder_download(cls):
        # cls.touch('folder_download_win.png', is_common_img=True)
        cls.keyevent('{DOWN}')

    @classmethod
    def click_folder_100(cls):
        cls.touch('folder_100.png', is_common_img=True)

    @classmethod
    def click_folder_1k(cls):
        cls.touch('folder_1k.png', is_common_img=True)

    @classmethod
    def click_folder_10k(cls):
        cls.touch('folder_10k.png', is_common_img=True)

    @classmethod
    def click_folder_100k(cls):
        cls.touch('folder_100k.png', is_common_img=True)

    @classmethod
    def click_folder_1m(cls):
        cls.touch('folder_1m.png', is_common_img=True)

    @classmethod
    def click_btn_sync_to_box(cls):
        cls.touch('btn_sync_to_box.png', is_common_img=True)

    @classmethod
    def click_btn_create_folder(cls):
        cls.touch('btn_create_folder.png', is_common_img=True)

    @classmethod
    def click_folder_my_space(cls):
        cls.touch('box_folder_small_my_space.png', is_common_img=True)


if __name__ == '__main__':
    print('a')
