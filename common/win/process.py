import os


class ProcessTool:
    @staticmethod
    def start_taskmanager():
        # if delete 'start', current thread will be blocked
        os.system(r'start C:\WINDOWS\system32\taskmgr.exe')


if __name__ == '__main__':
    ProcessTool.start_taskmanager()
