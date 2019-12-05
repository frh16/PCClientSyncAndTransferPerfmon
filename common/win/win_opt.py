import win32gui
import time
import os
from win32.lib import win32con
from win32api import GetSystemMetrics


class ALIGN:
    NONE = 0
    LEFT = 1
    RIGHT = 2

class Win32Tool:

    SCREEN_WIDTH = GetSystemMetrics(0)
    SCREEN_HIGHT = GetSystemMetrics(1)

    @staticmethod
    def find_window(class_name=None, wnd_name=None):
        return win32gui.FindWindow(class_name, wnd_name)

    @staticmethod
    def move_to(class_name=None, wnd_name=None, x=0, y=0, align=ALIGN.NONE):
        hwnd = win32gui.FindWindow(class_name, wnd_name)

        if align != ALIGN.NONE:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            window_width = right - left
            window_hight = bottom - top
            if (align & ALIGN.RIGHT) != 0:
                x = Win32Tool.SCREEN_WIDTH - window_width
                y = top
            if (align & ALIGN.LEFT) != 0:
                x = 0
                y = top

        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)

    @staticmethod
    def wnd_is_open(class_name):
        hwnd = win32gui.FindWindow(class_name, None)
        if hwnd != 0:
            return True
        return False

    @staticmethod
    def wait_wnd_open(class_name=None, wnd_name=None, time_out=10, interval=1):
        start_time = time.time()
        while True:
            hwnd = win32gui.FindWindow(class_name, wnd_name)
            if hwnd != 0:
                break
            else:
                cur_time = time.time()
                if cur_time - start_time >= time_out:
                    print('wait wnd time out! ', class_name, wnd_name)
                    break
                time.sleep(interval)

    @staticmethod
    def close_wnd(class_name=None, wnd_name=None, time_out=3, interval=1):
        start_time = time.time()
        while True:
            hwnd = win32gui.FindWindow(class_name, wnd_name)
            if hwnd != 0:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                break
            else:
                cur_time = time.time()
                if cur_time - start_time >= time_out:
                    print('close wnd time out! ', class_name, wnd_name)
                    break
                time.sleep(interval)

    @staticmethod
    def open_dir(directory):
        os.system("start explorer " + directory)





if __name__ == '__main__':
    # move_to('CSyncDetailWnd', align=ALIGN.LEFT)
    # wait_wnd_open('CMainWndWeb_Private')
    # hwnd = win32gui.FindWindow(None, '20191203135939_0.1k')
    print('----------')
    # Win32Tool.start_taskmanager()