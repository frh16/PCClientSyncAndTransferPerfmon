# -*- encoding=utf8 -*-
__author__ = "frh"

from pages.base_page import BasePage

class SyncDetail(BasePage):

    img_folder_name = 'sync_detail'
    window_class_name = 'CSyncDetailWnd'

    transfer_info_width_when_not_start = -1

    TRANSFER_INFO_RECT = [25, 480, 500, 20]
    TRANSFER_INFO_SCREEN_SHOT_NAME = 'screenshot_cut.bmp'

    @classmethod
    def click_tag_synchronizing(cls):
        cls.touch('sync_detail_tag_synchronizing.png')


if __name__ == '__main__':
    print('a')
