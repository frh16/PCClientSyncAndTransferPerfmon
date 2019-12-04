import os


class OSTool:

    @staticmethod
    def open_dir(directory):
        os.system("start explorer " + directory)

    @staticmethod
    def mkdir(path):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @staticmethod
    def create_file(file):
        f = open(file, 'w')
        f.close()

    @staticmethod
    def del_file(file):
        if os.path.exists(file):
            os.remove(file)

    @staticmethod
    def join(path, name):
        return os.path.join(path, name)

    # @staticmethod
    # def link_dir(cur_):


if __name__ == '__main__':
    print('test')
    # del_file(r'D:\work\workspace\PycharmProjects\PCClientSyncAndTransferPerfmon\temp\screenshot_cut.bmp')
    a = OSTool.join(r'D:\_test_data_', 'download')
    print(a)