import xlwings as xw
import threading

class ExcelTool():
    __instance = None

    # lock = threading.RLock()

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = ExcelTool()
        return cls.__instance

    def create_excel(self, file_name):
        self.app = xw.App(visible=False, add_book=False)
        # 添加一个新的工作薄
        self.wb = self.app.books.add()
        self.file_name = file_name
        self.is_active = True

    def enter_sheet(self, sheet_name):
        if isinstance(sheet_name, int):
            if sheet_name > len(self.wb.sheets) -1:
                self.wb.sheets.add('sheet' + str(sheet_name+1))
        elif isinstance(sheet_name, str):
            hasSheet = False
            print(len(self.wb.sheets))
            for sht in self.wb.sheets:
                if sht.name == sheet_name:
                    hasSheet = True
                    break
            if not hasSheet:
                self.wb.sheets.add(sheet_name)

        sheet = self.wb.sheets[sheet_name]
        if not sheet:
            self.wb.sheets.add(sheet_name)

        self.cur_sht = self.wb.sheets[sheet_name]

    def write_line(self, data, row_num):
        self.cur_sht.range('A' + str(row_num)).value = data

    def write_line_in_sheet(self, sheet_name, data, row_num):
        # self.lock.acquire()
        if self.is_active:
            self.enter_sheet(sheet_name)
            self.write_line(data, row_num)
            # self.lock.release()

    def save_and_close(self):
        # self.lock.acquire()
        self.wb.save(self.file_name)
        self.wb.close()
        self.app.quit()
        self.is_active = False

        # if delete following lines, et.exe(EXCEL.exe) will not disappear
        self.wb = None
        self.app = None

        # self.lock.release()

if __name__ == '__main__':
    excel_tool = ExcelTool.getInstance()
    excel_tool.create_excel('test.xlsx')
    excel_tool.write_line_in_sheet('abc', ['123', '123'], 1)
    excel_tool.write_line_in_sheet('def', ['333', '333'], 1)
    excel_tool.write_line_in_sheet('abc', ['aaa'], 2)
    excel_tool.write_line_in_sheet('def', ['bbb'], 2)
    excel_tool.enter_sheet('sheet1')
    excel_tool.cur_sht.delete
    excel_tool.save_and_close()