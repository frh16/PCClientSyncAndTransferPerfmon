from airtest.core.api import *
from data.priority import *
from pages.desktop import Desktop
from pages.login import Login
from pages.main import Main
from pages.sync import Sync
from pages.sync_detail import SyncDetail
from pages.select_local_folder_sync_to_cloud import SelectLocalFolderSyncToCloud
from pages.create_sync_box import CreateSyncBox
from pages.sync_setting import SyncSetting
from common.win.win_opt import *
from common.win.screen import *
from common.win.perfmon import *
from common.config import Config
from common.utils.ocr import *
from common.utils.file import *
from common.utils.opencv_opt import *
from common.utils.excel import ExcelTool
from data.window_class_name import WinClassName
from web.web_utils import WebUtils
import threading
import os
import pythoncom

class SyncManager():

    cur_sync_web_folder = '0.1k'
    cur_transfer_fail_num = 0
    cur_upload_num = 0
    start_sync_time = 0
    is_sync_finish = False

    is_start_monitor = False
    record_perfmon_times = 0
    record_transfer_fail_times = 0

    is_need_record_sync_start_time = False
    sync_start_used_time = 0
    sync_finish_used_time = 0

    @staticmethod
    def create_sync_local_to_cloud():
        SyncManager.login()
        SyncManager.sync_local_folder()

        SelectLocalFolderSyncToCloud.click_folder_100()
        SelectLocalFolderSyncToCloud.click_btn_sync_to_box()
        CreateSyncBox.click_folder_my_space()
        CreateSyncBox.click_advance_setting()
        SyncSetting.click_btn_upload_sync()
        SyncSetting.click_btn_ok()
        CreateSyncBox.click_btn_ok('white')

        SyncManager.start_check_sync_start()

        close_window_by_class_name(WinClassName.SYNC_LOCAL_PATH_NOTICE)


    @staticmethod
    def create_sync_cloud_to_local():
        print('a')

    @staticmethod
    def login():
        if wnd_is_open(Main.window_class_name):
            return
        Desktop.open_soft()
        Login.click_btn_login()

    @staticmethod
    def sync_local_folder():
        wait_wnd_open(Main.window_class_name)
        Main.move_to(align=ALIGN.LEFT)
        Main.click_left_btn_sync()

        SyncManager.show_sync_detail()

        Sync.click_sync_local_folder()
        SelectLocalFolderSyncToCloud.click_this_computer()
        SelectLocalFolderSyncToCloud.click_drive_d()
        SelectLocalFolderSyncToCloud.click_folder_test_data()
        SelectLocalFolderSyncToCloud.click_folder_upload()

    @staticmethod
    def delete_first_sync_box():
        Sync.click_first_sync_box()
        Sync.click_btn_delete()

    @staticmethod
    def show_sync_detail():
        Sync.click_btn_detail()
        SyncDetail.click_tag_synchronizing()
        SyncDetail.move_to(align=ALIGN.RIGHT)
        if SyncDetail.transfer_info_width_when_not_start == -1:
            SyncDetail.transfer_info_width_when_not_start = SyncManager.get_transfer_info_width()

    @staticmethod
    def start_check_sync_start():
        SyncManager.start_sync_time = time.time()
        threading.Thread(target=SyncManager.check_sync_start).start()

    @staticmethod
    def check_sync_start(timeout=10):
        start_time = time.time()

        while True:
            width = SyncManager.get_transfer_info_width()
            cur_time = time.time()
            used_time = cur_time - start_time
            if width != SyncDetail.transfer_info_width_when_not_start:
                # use_time write to excel
                print('start sync used time is: ' + str(used_time))
                SyncManager.sync_start_used_time = used_time

                # start perfmon
                SyncManager.start_monitor()
                SyncManager.start_check_sync_end()
                threading.Thread(target=SyncManager.my_thread).start()
                break
            if used_time > timeout:
                print('check_sync_start time out')
                break

            time.sleep(0.1)

    @staticmethod
    def my_thread():
        excel_tool = ExcelTool.getInstance()
        excel_tool.create_excel('test.xlsx')
        excel_tool.write_line_in_sheet('record', ['同步开始所用时间', SyncManager.sync_start_used_time], 1)

        perfmon = Perfmon.getInstance()
        perfmon.init_control()

        while True:
            print('SyncManager.is_sync_finish===>'+str(SyncManager.is_sync_finish))
            if SyncManager.is_sync_finish:
                excel_tool.write_line_in_sheet('record', ['同步花费时间', SyncManager.sync_finish_used_time], 2)
                excel_tool.save_and_close()
                break

            if SyncManager.is_start_monitor:
                SyncManager.record_perfmon()
                SyncManager.check_sync_fail_num()

            time.sleep(1)

    @staticmethod
    def record_perfmon():
        SyncManager.record_perfmon_times += 1
        excel_tool = ExcelTool.getInstance()
        perfmon = Perfmon.getInstance()
        excel_tool.write_line_in_sheet('perfmon', perfmon.get_taskmanager_data(), SyncManager.record_perfmon_times)
        # if SyncManager.record_perfmon_times > 2:
        #     SyncManager.is_sync_finish = True

    @staticmethod
    def get_transfer_info_width():
        file_path = os.path.join(Config.TEMP_PATH, SyncDetail.TRANSFER_INFO_SCREEN_SHOT_NAME)
        screen_shot(SyncDetail.window_class_name, file_path, SyncDetail.TRANSFER_INFO_RECT)
        width = get_text_width(file_path)
        # print('width======>'+str(width))
        del_file(file_path)
        return width

    @staticmethod
    def start_monitor():
        SyncManager.is_start_monitor = True
        SyncManager.record_perfmon_times = 0
        SyncManager.record_transfer_fail_times = 0
        SyncManager.cur_transfer_fail_num = 0
        SyncManager.cur_upload_num = 0
        SyncManager.is_sync_finish = False

    @staticmethod
    def check_sync_fail_num():
        SyncManager.record_transfer_fail_times += 1

        file_path = os.path.join(Config.TEMP_PATH, SyncDetail.TRANSFER_INFO_SCREEN_SHOT_NAME)
        screen_shot(SyncDetail.window_class_name, file_path, SyncDetail.TRANSFER_INFO_RECT)
        ocr_tool = OCRTool.getInstance()
        str_ocr_result = ocr_tool.get_str_all(file_path)

        import re
        searchObj = re.search('\d+个传输错误', str_ocr_result)
        if searchObj:
            start = searchObj.start()
            end = str_ocr_result.index('个传输错误')
            SyncManager.cur_transfer_fail_num = int(str_ocr_result[start:end])
            print('SyncManager.cur_transfer_fail_num==>' + str(SyncManager.cur_transfer_fail_num))
            excel_tool = ExcelTool.getInstance()
            excel_tool.write_line_in_sheet('传输错误', [SyncManager.cur_transfer_fail_num], SyncManager.record_transfer_fail_times)

        del_file(file_path)

    @staticmethod
    def start_check_sync_end():
        SyncManager.cur_transfer_fail_num = 0
        SyncManager.cur_upload_num = 0
        SyncManager.is_sync_finish = False

        webutils = WebUtils.getInstance()
        webutils.refresh()
        sleep(2)
        webutils.click(['xpath', "//a[text()=" + "\'" + SyncManager.cur_sync_web_folder + "\'" +"]/../../../preceding-sibling::span"])
        threading.Thread(target=SyncManager.check_cur_upload_num).start()


    @staticmethod
    def check_cur_upload_num():
        webutils = WebUtils.getInstance()
        while True:
            sleep(5)
            arrow = webutils.find_element(['xpath', '//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/p[6]/a/i'])
            arrow.click()
            webutils.wait_element(['xpath', '//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/div/p[2]/span[2]'], 10)
            element_num = webutils.find_element(['xpath', '//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/div/p[2]/span[2]'])
            if element_num:
                str_num = element_num.text
                if str_num.find('个文件') > 0:
                    index = str_num.index('个文件')
                    if index > 0:
                        SyncManager.cur_upload_num = int(str_num[0:index])
                        print('SyncManager.cur_upload_num===>'+str(SyncManager.cur_upload_num))

            arrow.click()

            if SyncManager.cur_upload_num + SyncManager.cur_transfer_fail_num == SyncManager.get_total_upload_num():
                SyncManager.sync_finish_used_time = time.time() - SyncManager.start_sync_time
                print('sync_complete_used_time===>' + str(SyncManager.sync_finish_used_time))

                SyncManager.is_sync_finish = True
                SyncManager.release()
                break


    @staticmethod
    def get_total_upload_num():
        if SyncManager.cur_sync_web_folder == '1k':
            return 1000
        elif SyncManager.cur_sync_web_folder == '0.1k':
            return 100
        else:
            return -1

    @staticmethod
    def delete_web_folder():
        webutils = WebUtils.getInstance()
        btn_more = webutils.move_to_element(['class', 'fileMore'])
        time.sleep(0.5)
        btn_delete = webutils.find_element(['class', 'delete'])
        btn_delete.click()
        time.sleep(0.5)
        btn_ok = webutils.find_element(['css', '.dialog-button.confirm-ok.confirm-ok-false.ok'])
        btn_ok.click()


    @staticmethod
    def release():
        # delete sync box
        Sync.click_first_sync_box()
        Sync.click_btn_delete()
        Sync.click_btn_ok()

        # delete web folder after upload finish
        SyncManager.delete_web_folder()

        webutils = WebUtils.getInstance()
        webutils.quit()


if __name__ == '__main__':
    auto_setup(__file__, devices=[
        "Windows:///",
    ])
    # SyncManager.delete_web_folder()
    SyncManager.create_sync_local_to_cloud()
    # SyncManager.start_perfmon()
    # threading.Thread(target=SyncManager.my_thread).start()