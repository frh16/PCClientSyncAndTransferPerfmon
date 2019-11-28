import win32gui
import sys
import os
from common.config import Config
from PyQt5.QtWidgets import QApplication


def screen_shot(wnd_class_name, file_name, area=None):
    app = QApplication(sys.argv)
    CSyncDetailWnd = win32gui.FindWindow(wnd_class_name, None)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(CSyncDetailWnd).toImage()

    if area is None:
        img.save(file_name)
    else:
        cut_img = img.copy(area[0], area[1], area[2], area[3])
        cut_img.save(file_name)


if __name__ == '__main__':
    file_path = os.path.join(Config.TEMP_PATH, 'screenshot_cut.bmp')
    screen_shot('CSyncDetailWnd', file_path, [25, 480, 500, 20])