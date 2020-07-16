import glob
import os
import re

import cv2
from PIL import Image

from cv import UIMatcher
from utils.Log import color_log as log


def check_equipment(image, template_path):
    """
    查找装备
    :param template_path: 模板目录
    :return: {'r': 相似度, 'x': x坐标, 'y': y坐标， 'path': 模板路径}
    """
    THRESHOLD = 0.55
    found = None
    return_list = list()

    screen = image
    # 遍历所有的图片寻找模板
    for imagePath in glob.glob(template_path + "/*"):
        log.debug("> " + imagePath)
        # result = UIMatcher.multi_scale_template_match(screen, imagePath)
        h, w = screen.shape[:2]
        item_w = w / 10
        scale = 128 / item_w
        result = UIMatcher.multi_scale_template_match(
            screen, imagePath, min_scale=scale, max_scale=scale, step=1)

        if result['r'] > THRESHOLD:
            result['path'] = imagePath
            return_list.append(result)

    return return_list


def concat(image_info):
    target = Image.new('RGBA', (1600, 900), (255, 255, 255))
    for image in image_info:
        target.paste(Image.open(image['path']), (image['x0'], image['y0'],))
    Image._show(target)


def divide(image_info, screen):
    for image in image_info:
        x0, x1, y0, y1 = image['x0'], image['x1'], image['y0'], image['y1']
        item_img = screen[y0:y1, x0:x1]
        item_name = re.findall('([0-9]*\.webp)', image['path'])[0]
        print(item_name)
        save_path = os.path.join(os.path.abspath(os.path.curdir), 'res', item_name)
        cv2.imwrite(save_path, item_img)


if __name__ == '__main__':
    img = cv2.imread('Screenshot_2020-07-15-09-42-37.png')
    # res = check_equipment(img, '../equipment_img')
    # print(res)
    res = [{'x': 520.0, 'y': 731.0, 'r': 0.552212655544281, 'x0': 440, 'x1': 600, 'y0': 651, 'y1': 811,
            'path': '../equipment_img\\115551.webp'},
           {'x': 340.0, 'y': 731.0, 'r': 0.5510856509208679, 'x0': 260, 'x1': 420, 'y0': 651, 'y1': 811,
            'path': '../equipment_img\\115552.webp'},
           {'x': 880.0, 'y': 556.0, 'r': 0.649354100227356, 'x0': 800, 'x1': 960, 'y0': 476, 'y1': 636,
            'path': '../equipment_img\\115554.webp'},
           {'x': 700.0, 'y': 556.0, 'r': 0.6525304913520813, 'x0': 620, 'x1': 780, 'y0': 476, 'y1': 636,
            'path': '../equipment_img\\115555.webp'},
           {'x': 520.0, 'y': 556.0, 'r': 0.6233869194984436, 'x0': 440, 'x1': 600, 'y0': 476, 'y1': 636,
            'path': '../equipment_img\\115556.webp'},
           {'x': 340.0, 'y': 556.0, 'r': 0.6333774924278259, 'x0': 260, 'x1': 420, 'y0': 476, 'y1': 636,
            'path': '../equipment_img\\115581.webp'},
           {'x': 160.0, 'y': 556.0, 'r': 0.6381028294563293, 'x0': 80, 'x1': 240, 'y0': 476, 'y1': 636,
            'path': '../equipment_img\\115582.webp'},
           {'x': 880.0, 'y': 381.0, 'r': 0.63319993019104, 'x0': 800, 'x1': 960, 'y0': 301, 'y1': 461,
            'path': '../equipment_img\\115583.webp'},
           {'x': 700.0, 'y': 381.0, 'r': 0.6460870504379272, 'x0': 620, 'x1': 780, 'y0': 301, 'y1': 461,
            'path': '../equipment_img\\115584.webp'},
           {'x': 520.0, 'y': 381.0, 'r': 0.6616073846817017, 'x0': 440, 'x1': 600, 'y0': 301, 'y1': 461,
            'path': '../equipment_img\\115585.webp'},
           {'x': 340.0, 'y': 381.0, 'r': 0.6306370496749878, 'x0': 260, 'x1': 420, 'y0': 301, 'y1': 461,
            'path': '../equipment_img\\115586.webp'},
           {'x': 160.0, 'y': 381.0, 'r': 0.6497876644134521, 'x0': 80, 'x1': 240, 'y0': 301, 'y1': 461,
            'path': '../equipment_img\\115611.webp'},
           {'x': 880.0, 'y': 206.0, 'r': 0.646325409412384, 'x0': 800, 'x1': 960, 'y0': 126, 'y1': 286,
            'path': '../equipment_img\\115612.webp'},
           {'x': 700.0, 'y': 206.0, 'r': 0.629291832447052, 'x0': 620, 'x1': 780, 'y0': 126, 'y1': 286,
            'path': '../equipment_img\\115613.webp'},
           {'x': 520.0, 'y': 206.0, 'r': 0.6363018155097961, 'x0': 440, 'x1': 600, 'y0': 126, 'y1': 286,
            'path': '../equipment_img\\115614.webp'},
           {'x': 340.0, 'y': 206.0, 'r': 0.6403923034667969, 'x0': 260, 'x1': 420, 'y0': 126, 'y1': 286,
            'path': '../equipment_img\\115615.webp'},
           {'x': 160.0, 'y': 206.0, 'r': 0.6463441252708435, 'x0': 80, 'x1': 240, 'y0': 126, 'y1': 286,
            'path': '../equipment_img\\115616.webp'}]
    divide(res, img)
