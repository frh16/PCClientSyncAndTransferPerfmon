import uiautomation as auto
import sys
import time
import threading
import pythoncom
from common.utils.excel import ExcelTool

class Perfmon():
    __instance = None

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Perfmon()
        return cls.__instance

    def __init__(self):
        self.CPU = ''
        self.MEM = ''
        self.DISK = ''
        self.NETWORK = ''

    def init_control(self):
        task_manager = auto.WindowControl(searchDepth=1, Name='任务管理器')
        TaskManagerMain = task_manager.Control(searchDepth=1, Name='TaskManagerMain')
        empty_window = TaskManagerMain.Control(searchDepth=1, Name='')
        biaoge = empty_window.Control(searchDepth=1, Name='表格')
        chakan = biaoge.Control(searchDepth=1, Name='查看')
        xiangmuliebiao = chakan.Control(searchDepth=1, Name='项目列表')
        yingyong = xiangmuliebiao.Control(searchDepth=1, Name='应用')
        process = yingyong.Control(searchDepth=1, Name='进程: 联想企业网盘')
        # 查看 按类型分组 不小心关闭的话 打开下边这行 注掉上边两行，但是不能这么做，因为还有个进程叫“联想企业网盘”，webtool那个也是这名字...
        # process = xiangmuliebiao.Control(searchDepth=1, Name='进程: 联想企业网盘')
        row_detail = process.Control(searchDepth=1, Name='行详细信息')

        self.CPU = row_detail.EditControl(searchDepth=1, Name='CPU')
        self.MEM = row_detail.EditControl(searchDepth=1, Name='内存')
        self.DISK = row_detail.EditControl(searchDepth=1, Name='磁盘')
        self.NETWORK = row_detail.EditControl(searchDepth=1, Name='网络')

    def get_taskmanager_data(self):
        cpu_value = self.CPU.GetValuePattern().Value
        mem_value = self.MEM.GetValuePattern().Value
        disk_value = self.DISK.GetValuePattern().Value
        network_value = self.NETWORK.GetValuePattern().Value
        return [cpu_value, mem_value, disk_value, network_value]


CPU = None
MEM = None
DISK = None
NETWORK = None

is_stop_thread = False

def init_control():
    task_manager = auto.WindowControl(searchDepth=1, Name='任务管理器')
    TaskManagerMain = task_manager.Control(searchDepth=1, Name='TaskManagerMain')
    empty_window = TaskManagerMain.Control(searchDepth=1, Name='')
    biaoge = empty_window.Control(searchDepth=1, Name='表格')
    chakan = biaoge.Control(searchDepth=1, Name='查看')
    xiangmuliebiao = chakan.Control(searchDepth=1, Name='项目列表')
    yingyong = xiangmuliebiao.Control(searchDepth=1, Name='应用')
    process = yingyong.Control(searchDepth=1, Name='进程: 联想企业网盘')
    # 查看 按类型分组 不小心关闭的话 打开下边这行 注掉上边两行，但是不能这么做，因为还有个进程叫“联想企业网盘”，webtool那个也是这名字...
    # process = xiangmuliebiao.Control(searchDepth=1, Name='进程: 联想企业网盘')
    row_detail = process.Control(searchDepth=1, Name='行详细信息')

    global CPU
    global MEM
    global DISK
    global NETWORK
    CPU = row_detail.EditControl(searchDepth=1, Name='CPU')
    MEM = row_detail.EditControl(searchDepth=1, Name='内存')
    DISK = row_detail.EditControl(searchDepth=1, Name='磁盘')
    NETWORK = row_detail.EditControl(searchDepth=1, Name='网络')

def record_taskmanager_data():
    pythoncom.CoInitialize()

    excel_tool = ExcelTool.getInstance()

    num = 1
    global is_stop_thread
    while True:
        cpu_value = CPU.GetValuePattern().Value
        mem_value = MEM.GetValuePattern().Value
        disk_value = DISK.GetValuePattern().Value
        network_value = NETWORK.GetValuePattern().Value

        excel_tool.write_line_in_sheet('性能', [cpu_value, mem_value, disk_value, network_value], num)
        num += 1

        if is_stop_thread:
            break

        time.sleep(1)

def get_taskmanager_data():
    cpu_value = CPU.GetValuePattern().Value
    mem_value = MEM.GetValuePattern().Value
    disk_value = DISK.GetValuePattern().Value
    network_value = NETWORK.GetValuePattern().Value
    return [cpu_value, mem_value, disk_value, network_value]

def start_perfmon():
    init_control()

    global is_stop_thread
    is_stop_thread = False
    threading.Thread(target=record_taskmanager_data).start()

def stop_perfmon():
    global is_stop_thread
    is_stop_thread = True

def abc():
    pythoncom.CoInitialize()
    perfmon = Perfmon()
    perfmon.init_control()
    print(perfmon.get_taskmanager_data())

if __name__ == '__main__':
    # excel_tool = ExcelTool.getInstance()
    # excel_tool.create_excel('test.xlsx')
    # start_perfmon()
    # time.sleep(5)
    # stop_perfmon()
    # init_control()
    threading.Thread(target=abc).start()



