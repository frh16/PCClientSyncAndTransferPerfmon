import win32gui
from win32.lib import win32con
import time
from win32api import GetSystemMetrics

class ALIGN:
    NONE = 0
    LEFT = 1
    RIGHT = 2


SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HIGHT = GetSystemMetrics(1)

def wnd_is_open(class_name):
    hwnd = win32gui.FindWindow(class_name, None)
    if hwnd != 0:
        return True
    return False

def close_window_by_class_name(class_name, time_out=3, interval=1):
    start_time = time.time()
    while True:
        hwnd = win32gui.FindWindow(class_name, None)
        if hwnd != 0:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            break
        else:
            cur_time = time.time()
            if cur_time - start_time >= time_out:
                print('find ' + class_name + ' time out!')
                break
            time.sleep(interval)

def wait_wnd_open(class_name, time_out=10, interval=1):
    start_time = time.time()
    while True:
        hwnd = win32gui.FindWindow(class_name, None)
        if hwnd != 0:
            break
        else:
            cur_time = time.time()
            if cur_time - start_time >= time_out:
                print('wait ' + class_name + ' time out!')
                break
            time.sleep(interval)

def move_to(class_name, x=0, y=0, align=ALIGN.NONE):
    hwnd = win32gui.FindWindow(class_name, None)

    if align != ALIGN.NONE:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        window_width = right - left
        window_hight = bottom - top
        if (align & ALIGN.RIGHT) != 0:
            x = SCREEN_WIDTH - window_width
            y = top
        if (align & ALIGN.LEFT) != 0:
            x = 0
            y = top

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, x, y, 0, 0, win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)

if __name__ == '__main__':
    # move_to('CSyncDetailWnd', align=ALIGN.LEFT)
    # wait_wnd_open('CMainWndWeb_Private')
    hwnd = win32gui.FindWindow('CMainWndWeb_Private', None)
    print('----------'+str(hwnd))