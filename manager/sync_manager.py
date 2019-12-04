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
from common.win.win_opt import Win32Tool
from common.win.screen import *
from common.win.perfmon import *
from common.win.uia_tool import UIATool
from common.config import Config
from common.utils.ocr import *
from common.utils.os_tool import OSTool
from common.utils.opencv_opt import *
from common.utils.excel import ExcelTool
from common.utils.log import Logger
from data.window_class_name import WinClassName
from web.web_utils import WebUtils
import threading
import os
import pythoncom


class SyncManager():

    cur_case_id = '0.1k'
    cur_sync_web_folder = '0.1k'
    is_upload = True
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

    thread_monitor = None
    thread_check_sync_end = None

    my_log = None

    @staticmethod
    def set_case(case_id, is_upload=True):
        SyncManager.cur_case_id = case_id
        SyncManager.cur_sync_web_folder = SyncManager.cur_case_id
        SyncManager.is_upload = is_upload

        log_dir = os.path.join(Config.get_log_dir(), str(SyncManager.cur_case_id))
        OSTool.mkdir(log_dir)
        full_path = os.path.join(log_dir, 'debug.log')
        SyncManager.my_log = Logger(full_path)

    @staticmethod
    def create_sync_upload():
        SyncManager.login()
        SyncManager.sync_local_folder()

        SyncManager.click_folder_by_case()
        SelectLocalFolderSyncToCloud.click_btn_sync_to_box()
        CreateSyncBox.click_folder_my_space()
        CreateSyncBox.click_advance_setting()
        SyncSetting.click_btn_upload_sync()
        SyncSetting.click_btn_ok()
        CreateSyncBox.click_btn_ok('white')

        close_window_by_class_name(WinClassName.SYNC_LOCAL_PATH_NOTICE)

        SyncManager.start_check_sync_start()

        if isinstance(SyncManager.thread_monitor, threading.Thread):
            SyncManager.thread_monitor.join()

        SyncManager.release()

    @staticmethod
    def click_folder_by_case():
        if SyncManager.cur_sync_web_folder == '0.1k':
            SelectLocalFolderSyncToCloud.click_folder_100()
        elif SyncManager.cur_sync_web_folder == '1k':
            SelectLocalFolderSyncToCloud.click_folder_1k()
        elif SyncManager.cur_sync_web_folder == '10k':
            SelectLocalFolderSyncToCloud.click_folder_1k()

    @staticmethod
    def login():
        if Win32Tool.wnd_is_open(Main.window_class_name):
            return
        Desktop.open_soft()
        Login.click_btn_login()

    @staticmethod
    def sync_local_folder():
        SyncManager.move_main_and_sync_detail()

        Sync.click_sync_local_folder()
        SelectLocalFolderSyncToCloud.click_this_computer()
        SelectLocalFolderSyncToCloud.click_drive_d()
        SelectLocalFolderSyncToCloud.click_folder_test_data()
        SelectLocalFolderSyncToCloud.click_folder_upload()

    @staticmethod
    def move_main_and_sync_detail():
        Win32Tool.wait_wnd_open(class_name=Main.window_class_name)
        Main.move_to(align=ALIGN.LEFT)
        Main.click_left_btn_sync()

        SyncManager.show_sync_detail()

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
        cur_thread = threading.Thread(target=SyncManager.check_sync_start)
        cur_thread.start()
        cur_thread.join()

    @staticmethod
    def check_sync_start(timeout=30):
        SyncManager.my_log.info('check_sync_start')

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
                SyncManager.my_log.info('start perfmon')
                SyncManager.start_monitor()
                SyncManager.start_check_sync_end()
                break
            if used_time > timeout:
                print('check_sync_start time out')
                break

            time.sleep(0.1)

    @staticmethod
    def monitor_and_record():

        SyncManager.my_log.info('monitor_and_record')

        log_dir = os.path.join(Config.get_log_dir(), str(SyncManager.cur_case_id))
        OSTool.mkdir(log_dir)
        save_path = os.path.join(log_dir, 'monitor.xlsx')

        excel_tool = ExcelTool.getInstance()
        excel_tool.create_excel(save_path)
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
        OSTool.del_file(file_path)
        return width

    @staticmethod
    def start_monitor():
        SyncManager.is_start_monitor = True
        SyncManager.record_perfmon_times = 0
        SyncManager.record_transfer_fail_times = 0
        SyncManager.cur_transfer_fail_num = 0
        SyncManager.cur_upload_num = 0
        SyncManager.is_sync_finish = False

        SyncManager.thread_monitor = threading.Thread(target=SyncManager.monitor_and_record)
        SyncManager.thread_monitor.start()

    @staticmethod
    def check_sync_fail_num():
        SyncManager.record_transfer_fail_times += 1

        from common.utils.time import get_time
        file_name = get_time() + '.jpg'
        file_path = os.path.join(Config.TEMP_PATH, file_name)
        screen_shot(SyncDetail.window_class_name, file_path, SyncDetail.TRANSFER_INFO_RECT)
        ocr_tool = OCRTool.getInstance()
        words = ocr_tool.get_str_arr(file_path)
        target_word = None
        for word in words:
            if '个传输错误' in word:
                target_word = word
                break
        print('str_ocr_result===>', target_word)

        if target_word:
            import re
            searchObj = re.search('\d+个传输错误', target_word)
            if searchObj:
                start = searchObj.start()
                end = target_word.index('个传输错误')
                SyncManager.cur_transfer_fail_num = int(target_word[start:end])
                print('SyncManager.cur_transfer_fail_num==>' + str(SyncManager.cur_transfer_fail_num))
                excel_tool = ExcelTool.getInstance()
                excel_tool.write_line_in_sheet('传输错误', [SyncManager.cur_transfer_fail_num], SyncManager.record_transfer_fail_times)

        OSTool.del_file(file_path)

    @staticmethod
    def start_check_sync_end():

        SyncManager.my_log.info('start_check_sync_end')

        SyncManager.is_sync_finish = False
        SyncManager.cur_transfer_fail_num = 0

        if SyncManager.is_upload:
            SyncManager.cur_upload_num = 0

            webutils = WebUtils.getInstance()
            webutils.connect()

            SyncManager.refresh_web_select_folder()
            SyncManager.my_log.info('start_check_sync_end222')
            SyncManager.thread_check_sync_end = threading.Thread(target=SyncManager.check_upload_sync_end)
            SyncManager.thread_check_sync_end.start()
        else:
            SyncManager.thread_check_sync_end = threading.Thread(target=SyncManager.check_download_sync_end)
            SyncManager.thread_check_sync_end.start()

    @staticmethod
    def refresh_web_select_folder():
        webutils = WebUtils.getInstance()
        webutils.refresh()
        SyncManager.my_log.info('refresh_web_select_folder111')
        target_element_xpath = "//a[text()=" + "\'" + SyncManager.cur_sync_web_folder + "\'" + "]/../../../preceding-sibling::span"
        webutils.wait_element(['xpath', target_element_xpath], 60)
        SyncManager.my_log.info('refresh_web_select_folder222')
        webutils.click(['xpath', target_element_xpath])

    @staticmethod
    def check_upload_sync_end():

        SyncManager.my_log.info('check_upload_sync_end')

        webutils = WebUtils.getInstance()

        arrow_down_css = '.icon.i-arrow2'
        arrow_up_css = '.icon.i-arrow4'

        # arrow_xpath = '//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/p[6]/a/i'
        target_text_xpath = '//*[@id="file-attr-wraper"]/div/div[2]/div/div[2]/div[1]/div/p[2]/span[2]'
        while True:
            sleep(5)
            try:
                webutils.wait_element(['css', arrow_down_css], 60)
                arrow_down = webutils.find_element(['css', arrow_down_css])
                arrow_down.click()
                webutils.wait_element(['xpath', target_text_xpath], 60)
                element_num = webutils.find_element(['xpath', target_text_xpath])
                if element_num:
                    str_num = element_num.text
                    if str_num.find('个文件') > 0:
                        index = str_num.index('个文件')
                        if index > 0:
                            SyncManager.cur_upload_num = int(str_num[0:index])
                            print('SyncManager.cur_upload_num===>' + str(SyncManager.cur_upload_num))

                arrow_up = webutils.find_element(['css', arrow_up_css])
                arrow_up.click()
            except Exception as e:
                print('exception in check_cur_upload_num: ', e)
                SyncManager.refresh_web_select_folder()

            SyncManager.my_log.info('check_cur_upload_num: ' + str(SyncManager.cur_upload_num))
            SyncManager.my_log.info('cur_transfer_fail_num: ' + str(SyncManager.cur_transfer_fail_num))

            # >= because 'desktop.ini'
            if SyncManager.cur_upload_num + SyncManager.cur_transfer_fail_num >= SyncManager.get_total_num():
                SyncManager.sync_finish_used_time = time.time() - SyncManager.start_sync_time
                print('sync_complete_used_time===>' + str(SyncManager.sync_finish_used_time))
                SyncManager.is_sync_finish = True
                break


    @staticmethod
    def get_total_num():
        if SyncManager.cur_sync_web_folder == '1k':
            return 1000
        elif SyncManager.cur_sync_web_folder == '10k':
            return 10000
        elif SyncManager.cur_sync_web_folder == '100k':
            return 100000
        elif SyncManager.cur_sync_web_folder == '1m':
            return 1000000
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

        Win32Tool.close_wnd(class_name=Sync.window_class_name)
        Win32Tool.close_wnd(class_name=SyncDetail.window_class_name)

        if SyncManager.is_upload:
            # delete web folder after upload finish
            SyncManager.delete_web_folder()

            webutils = WebUtils.getInstance()
            webutils.quit()
        else:
            folder_name = SyncManager.get_download_local_folder_name()
            # Win32Tool.close_wnd(wnd_name=folder_name)

        SyncManager.thread_monitor = None
        SyncManager.thread_check_sync_end = None

    ###############################################

    @staticmethod
    def create_sync_download():
        SyncManager.login()
        SyncManager.sync_cloud_folder()
        SyncManager.click_folder_by_case()
        SyncManager.change_local_sync_path()

        CreateSyncBox.click_advance_setting()
        SyncSetting.click_btn_download_sync()
        SyncSetting.click_btn_ok()
        CreateSyncBox.click_btn_ok('white')
        Win32Tool.close_wnd(class_name=WinClassName.SYNC_LOCAL_PATH_NOTICE)

        SyncManager.start_check_sync_start()

        if isinstance(SyncManager.thread_monitor, threading.Thread):
            SyncManager.thread_monitor.join()

        SyncManager.release()

    @staticmethod
    def sync_cloud_folder():
        SyncManager.move_main_and_sync_detail()

        Sync.click_btn_create_sync()
        Sync.click_btn_sync_cloud_folder()
        CreateSyncBox.double_click_folder_my_space()
        CreateSyncBox.double_click_folder_download()

    @staticmethod
    def change_local_sync_path():
        CreateSyncBox.click_change_path()
        SelectLocalFolderSyncToCloud.click_this_computer()
        SelectLocalFolderSyncToCloud.click_drive_d()
        SelectLocalFolderSyncToCloud.click_folder_test_data()
        SelectLocalFolderSyncToCloud.click_folder_download()
        SelectLocalFolderSyncToCloud.click_btn_create_folder()
        SelectLocalFolderSyncToCloud.text(SyncManager.get_download_local_folder_name())
        SelectLocalFolderSyncToCloud.click_btn_sync_to_box()

    @staticmethod
    def get_download_local_folder_name():
        return str(Config.RUN_TIME) + '_' + str(SyncManager.cur_case_id)

    @staticmethod
    def check_download_sync_end():
        folder_name = SyncManager.get_download_local_folder_name()
        # folder_name = '20191203135939_0.1k'
        target_dir = OSTool.join(Config.DOWNLOAD_DIR, folder_name)
        OSTool.open_dir(target_dir)
        Win32Tool.wait_wnd_open(wnd_name=folder_name)
        Win32Tool.move_to(wnd_name=folder_name, x=Win32Tool.SCREEN_WIDTH)

        while True:
            download_num = UIATool.get_folder_file_num(folder_name)
            print('download_num===>'+str(download_num))
            if download_num + SyncManager.cur_transfer_fail_num >= SyncManager.get_total_num():
                SyncManager.sync_finish_used_time = time.time() - SyncManager.start_sync_time
                print('sync_complete_used_time===>' + str(SyncManager.sync_finish_used_time))
                SyncManager.is_sync_finish = True
                break



if __name__ == '__main__':
    auto_setup(__file__, devices=[
        "Windows:///",
    ])
    # SyncManager.set_case_id('0.1k')
    # SyncManager.create_sync_local_to_cloud()
    # SyncManager.start_monitor()
    SyncManager.start_check_download_sync_end()
