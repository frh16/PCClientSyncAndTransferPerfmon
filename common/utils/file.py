import os

def create_file(file):
    f = open(file, 'w')
    f.close()

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def del_file(file):
    if os.path.exists(file):
        os.remove(file)

if __name__ == '__main__':
    print('test')
    del_file(r'D:\work\workspace\PycharmProjects\PCClientSyncAndTransferPerfmon\temp\screenshot_cut.bmp')