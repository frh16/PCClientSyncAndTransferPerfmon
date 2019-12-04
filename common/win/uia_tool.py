import uiautomation as auto


class UIATool:

    @staticmethod
    def get_folder_file_num(folder_name):
        window = auto.WindowControl(searchDepth=1, Name=folder_name)
        control1 = window.Control(searchDepth=6, Name='属性字段')
        control2 = control1.Control(searchDepth=1, RegexName='.* 个项目')
        return int(control2.Name.split(' ')[0])


if __name__ == '__main__':
    print(UIATool.get_folder_file_num('upload'))
