
from airtest.core.api import *
from pages.main import Main
from pages.download import Download
from pages.select_local_folder_sync_to_cloud import SelectLocalFolderSyncToCloud
from manager.login_manager import LoginManager
from common.config import Config
import sys
from common.win.win_opt import *


class TransferManager:

    target_folder = '1k'

    @staticmethod
    def download():
        LoginManager.login()

        Main.click_left_btn_transfer_list()
        Win32Tool.wait_wnd_open(class_name='CShowTransWnd')
        Win32Tool.move_to(class_name='CShowTransWnd', align=ALIGN.RIGHT)

        Main.click_left_btn_my_space()
        Main.double_click_right_folder_download()

        TransferManager.select_folder()

        Main.click_left_btn_download()
        Download.click_btn_browse()
        TransferManager.select_path()
        # Download.click_btn_download()

    @staticmethod
    def select_path():
        SelectLocalFolderSyncToCloud.click_this_computer()
        SelectLocalFolderSyncToCloud.click_drive_d()
        SelectLocalFolderSyncToCloud.click_folder_test_data()
        SelectLocalFolderSyncToCloud.click_folder_download()
        SelectLocalFolderSyncToCloud.click_btn_create_folder()
        SelectLocalFolderSyncToCloud.text(TransferManager.get_download_local_folder_name())
        # SelectLocalFolderSyncToCloud.click_btn_ok(color='gray_win')

    @staticmethod
    def get_download_local_folder_name():
        return str(Config.RUN_TIME) + '_' + str(TransferManager.target_folder)

    @staticmethod
    def select_folder():
        if TransferManager.target_folder == '0.1k':
            Main.click_folder_100()
        elif TransferManager.target_folder == '1k':
            Main.click_folder_1k()


if __name__ == '__main__':
    auto_setup(__file__, devices=[
        "Windows:///",
    ])
    TransferManager.download()
    # time.sleep(2)
    # Main.double_click()
    sys.exit()