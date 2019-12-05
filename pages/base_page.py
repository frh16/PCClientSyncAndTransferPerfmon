from airtest.core.api import *
import sys
import os
from common.config import Config
from common.win.win_opt import *
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from pywinauto import mouse

class BasePage():

    img_folder_name = 'None'
    window_class_name = ''

    @classmethod
    def get_img_path(cls, img_name, is_common_img=False):
        if is_common_img:
            img_path = os.path.join(Config.IMG_PATH, 'common')
        else:
            if cls.img_folder_name == BasePage.img_folder_name:
                img_path = os.path.join(Config.IMG_PATH, cls.get_invoke_py_name())
            else:
                img_path = os.path.join(Config.IMG_PATH, cls.img_folder_name)
        return os.path.join(img_path, img_name)

    @classmethod
    def get_invoke_py_name(cls):
        return cls.__name__.lower()
        # return sys._getframe().f_back.f_code.co_filename.split('\\')[-1].split('.')[0]

    @classmethod
    def touch(cls, img, right_click=False, is_common_img=False, target_pos=5):
        touch(Template(cls.get_img_path(img, is_common_img), target_pos=target_pos), right_click=right_click)

    @classmethod
    def wait_then_touch(cls, img, right_click=False, is_common_img=False):
        wait(Template(cls.get_img_path(img, is_common_img)))
        cls.touch(img, right_click, is_common_img)

    @classmethod
    def double_click(cls, img, is_common_img=False):
        if img:
            double_click(Template(cls.get_img_path(img, is_common_img)))

    @classmethod
    def text(cls, input_text):
        text(input_text)
        cls.keyevent('{ENTER}')

    @classmethod
    def keyevent(cls, keycode):
        keyevent(keycode)

    @classmethod
    def move_to(cls, x=0, y=0, align=ALIGN.NONE):
        Win32Tool.move_to(class_name=cls.window_class_name, x=x, y=y, align=align)

    @classmethod
    def click_btn_ok(cls, color='gray'):
        if color == 'gray':
            cls.touch('btn_ok_gray.png', is_common_img=True)
        elif color == 'white':
            cls.touch('btn_ok_white.png', is_common_img=True)
        elif color == 'gray_win':
            cls.touch('btn_ok_gray_win.png', is_common_img=True)

    # @classmethod
    # def move_to_left(cls, class_name, x=0, y=0, align=ALIGN.LEFT):
    #     move_to(class_name, x, y, align)
    #
    # @classmethod
    # def move_to_right(cls, class_name='', x=0, y=0, align=ALIGN.LEFT):
    #     move_to(class_name, x, y, align)

if __name__ == '__main__':
    print(BasePage.get_common_img_path())
