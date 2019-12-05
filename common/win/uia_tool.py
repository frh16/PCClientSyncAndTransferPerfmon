import uiautomation as auto


class UIATool:

    @staticmethod
    def get_folder_file_num(folder_name):
        window = auto.WindowControl(searchDepth=1, Name=folder_name)
        print(window.NativeWindowHandle)
        control1 = window.Control(searchDepth=6, Name='属性字段')
        control2 = control1.Control(searchDepth=1, RegexName='.* 个项目')
        str_num = control2.Name.split(' ')[0]
        int_num = int(str_num.replace(',', ''))
        return int_num

    @staticmethod
    def test():
        window = auto.WindowControl(searchDepth=1, Name='联想企业网盘')
        dialog = window.WindowControl(searchDepth=2, Name='浏览文件夹')
        control2 = dialog.Control(searchDepth=4, Name='此电脑')
        control2.Click()
        control3 = control2.Control(searchDepth=1, Name='Data(D:)')
        control3.Click()

        print(control2.NativeWindowHandle)
        # abc = control2.GetNextSiblingControl()
        # control2 = control1.Control(searchDepth=1, Name='桌面')
        # print(abc)
        # control1 = window.Control(searchDepth=1, Name='命名空间树状控制项')
        # print(control1)


if __name__ == '__main__':
    # print(UIATool.get_folder_file_num('100k'))
    UIATool.test()