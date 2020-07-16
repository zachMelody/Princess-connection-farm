import glob

import cv2
import matplotlib.pylab as plt
import numpy as np
import pytesseract as pt

from cv import UIMatcher


def dilate(image):
    # 处理数字图像
    img = image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # 定义蓝色的上下限
    lower = np.array([0, 0, 0])
    higher = np.array([255, 51, 150])
    # 在图片中提取蓝色的部分
    mask = cv2.inRange(hsv, lower, higher)
    # 和原图像求“与”操作，只保留蓝色
    left = cv2.bitwise_and(img, img, mask=mask)
    # 膨胀
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dst = cv2.dilate(left, kernel)
    return dst


def train():
    i = 0
    for imagePath in glob.glob("res/*"):
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 124,80 160*160j
        crop = gray[124:149, 74:155]
        ret, binary = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        plt.imshow(binary)
        plt.pause(0.01)
        cv2.imwrite("train/" + str(i) + ".tif", binary)
        i += 1


def divide(image_info, screen):
    screen = UIMatcher.RotateClockWise90(screen)
    for image in image_info:
        x0, x1, y0, y1 = image['x0'], image['x1'], image['y0'], image['y1']
        item_img = screen[y0:y1, x0:x1]
        # item_name = re.findall('([0-9]*\.webp)', image['path'])[0]
        # print(item_name)
        # save_path = os.path.join(os.path.abspath(os.path.curdir), 'res', item_name)
        # cv2.imwrite(save_path, item_img)
        image['image'] = item_img


def ocr(image_info):
    for image in image_info:
        item_image = image['image']
        width = item_image.shape[0]
        scale = (124 / 160, 149 / 160, 74 / 160, 155 / 160)
        y0, y1, x0, x1 = (int(pos * width) for pos in scale)
        crop = item_image[y0:y1, x0:x1]
        dilated_crop = dilate(crop)
        # DEBUG
        # plt.imshow(item_image)
        # plt.imshow(crop)
        # plt.imshow(dilated_crop)
        # plt.pause(0.01)
        result_str = pt.image_to_string(dilated_crop, lang='pcr2', config='--psm 6')
        image['amount'] = int(result_str.split('x')[-1])


if __name__ == '__main__':
    ocr(None)
