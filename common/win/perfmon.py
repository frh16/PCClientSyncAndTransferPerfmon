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

        cpu_value = cpu_value.split('%')[0]
        mem_value = mem_value.split(' ')[0]
        disk_value = disk_value.split(' ')[0]
        network_value = network_value.split(' ')[0]

        return [cpu_value, mem_value, disk_value, network_value]


if __name__ == '__main__':
    # excel_tool = ExcelTool.getInstance()
    # excel_tool.create_excel('test.xlsx')
    # start_perfmon()
    # time.sleep(5)
    # stop_perfmon()
    # init_control()
    perfmon = Perfmon.getInstance()
    perfmon.init_control()
    print(perfmon.get_taskmanager_data())


