
from pages.desktop import Desktop
from pages.login import Login
from pages.main import Main
from common.win.win_opt import Win32Tool


class LoginManager:

    @staticmethod
    def login():
        if Win32Tool.wnd_is_open(Main.window_class_name):
            return
        Desktop.open_soft()
        Login.click_btn_login()


