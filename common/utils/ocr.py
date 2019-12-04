from aip import AipOcr

class OCRTool(object):
    __instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = OCRTool()
        return cls.__instance

    """ 你的 APPID AK SK """
    APP_ID = '17515541'
    API_KEY = 'W56WtGzks4cpGD5Xa8nDPObE'
    SECRET_KEY = 'R649qUjaXC10suETQ79BuKo3EIDYZLoM'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 读取图片 """
    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def get_str_all(self, imgPath):
        words = self.get_str_arr(imgPath)
        result = ''
        for item in words:
            result += item
        return result

    def get_str_arr(self, imgPath):
        image = self.get_file_content(imgPath)
        # words_result_num = self.client.basicGeneral(image).get('words_result_num')
        words_result = self.client.basicGeneral(image).get('words_result')
        result = []
        for item in words_result:
            result.append(item['words'])
        return result

    def is_match(self, str, imgPath):
        str_all = self.get_str_all(imgPath)
        if str in str_all:
            return True
        return False

if __name__ == '__main__':
    # test data
    # img_path = 'D:/test/screenshot.jpg'
    # image = get_file_content(img_path)
    # print(client.basicGeneral(image))
    # print(is_match('您选择的目录不是空目录,系统将在这个目录下以默认设置建立一个空目录!', img_path))
    ocr_tool = OCRTool.getInstance()
    result = ocr_tool.get_str_all(r'D:\test\screenshot.jpg')
    print(result)

