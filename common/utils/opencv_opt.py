import numpy as np
import os
import cv2
import math

def get_text_rect(img_path):
    src = cv2.imread(img_path)

    # 灰度图
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    # 图像取非
    grayNot = cv2.bitwise_not(gray)
    # 高斯模糊
    blur = cv2.GaussianBlur(grayNot, (7, 7), 0)

    # 二值化
    ret, threImg = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    whereid = np.where(threImg > 0)
    # 交换横纵坐标的顺序，否则下面得到的每个像素点为(y,x)
    whereid = whereid[::-1]
    # 将像素点格式转换为(n_coords, 2)，每个点表示为(x,y)
    coords = np.column_stack(whereid)

    rect = cv2.minAreaRect(coords)
    box = cv2.boxPoints(rect)  # 获取最小外接矩形的4个顶点坐标(ps: cv2.boxPoints(rect) for OpenCV 3.x)
    box = np.int0(box)
    return box

def get_text_width(img_path):
    box = get_text_rect(img_path)
    return box[3][0] - box[0][0]

if __name__ == '__main__':
    width = get_text_width(r'D:\test\test.png')
    print(width)