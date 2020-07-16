import glob
import time

import uiautomator2 as u2

from cv import *
from ocr import ocr
from utils.Log import color_log as log


class Automator:
    BASE_IMG_PATH = 'tw_img/'
    MAX_COUNTER = 10  # 最大查找重试次数
    CHECK_COUNTER = 3

    def __init__(self):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect()
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False
        self.log = log
        self.failCounter = 0
        self.check_again = True

    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断jgm进程是否在前台, 最多等待20秒，否则唤醒到前台
            if self.d.app_wait("tw.sonet.princessconnect", front=True, timeout=1):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    time.sleep(1)
                self.appRunning = True
                break
            else:
                self.app = self.d.session("tw.sonet.princessconnect")
                self.appRunning = False
                continue

    def find_image(self, image_path, threshold=0.90, try_time=5):
        """
        查找当前屏幕上是否有图像，并返回坐标
        :param image_path: 图像路径
        :param threshold: 阈值
        :return: x, y
        """
        if self.failCounter > try_time:
            self.failCounter = 0
            return -1, -1

        screen = self.d.screenshot(format="opencv")
        result = UIMatcher.template_match(screen, image_path)
        self.log.info("IMAGE: {} -> 相似度: {:.3f}".format(image_path, result['r']))
        if result['r'] > threshold:
            self.failCounter = 0
            self.log.info("查找成功")
            self.log.debug(result)
            return result['x'], result['y']
        else:
            if try_time != 1:  # 排除场景变动检测的提示
                self.log.error("查找失败，正在重试...")
            self.failCounter += 1
            time.sleep(5)
            return self.find_image(image_path, try_time=try_time)

    def find_and_click(self, image_path):
        """
        检测图像并点击，完成点击后再次检测，防止未加载完毕导致的点击无效
        :param image_path: 图像路径
        :return:
        """
        # TODO: 只检测一次，可能有误差->自定义次数
        if self.check_again:
            x, y = self.find_image(image_path)
        else:
            x, y = self.find_image(image_path, try_time=1)

        if x == -1 and y == -1:
            if self.check_again:  # 首次检测
                self.log.error("点击失败")
            elif not self.check_again:  # 变动检测
                self.check_again = True
                self.log.debug("检测到场景变动，点击成功")
        else:
            time.sleep(2)
            self.d.click(x, y)
            time.sleep(2)
            if self.check_again:  # 检测点击生效与否
                self.log.debug("尝试检测场景变动")
                self.check_again = False
                self.find_and_click(image_path)
            elif not self.check_again:  # 点击未生效
                self.log.debug("点击未生效，尝试再次点击")
                self.d.click(x, y)
                self.check_again = True
                time.sleep(3)

    def check_equipment(self, template_path):
        """
        查找装备
        :param template_path: 模板目录
        :return: {'r': 相似度, 'x': x坐标, 'y': y坐标， 'path': 模板路径}
        """
        THRESHOLD = 0.55
        found = None
        return_list = list()

        screen = self.d.screenshot(format="opencv")
        # 遍历所有的图片寻找模板
        for imagePath in glob.glob(template_path + "/*"):
            self.log.debug("> " + imagePath)
            # result = UIMatcher.multi_scale_template_match(screen, imagePath)
            w, h = screen.shape[:2]
            item_w = w / 10
            scale = 128 / item_w  # TODO：128为模板宽，应修改为自动检测
            result = UIMatcher.multi_scale_template_match(
                screen, imagePath, min_scale=scale, max_scale=scale, step=1)

            if result['r'] > THRESHOLD:
                result['path'] = imagePath
                return_list.append(result)
        # 切割物品图标
        ocr.divide(return_list, screen)
        # 切割物品数量, 识别数字
        ocr.ocr(return_list)

        return return_list

    def get_screen_state(self, screen):
        # TODO: 判断当前状态
        pass

    def is_image_exist(self, image_path):
        """
        查找当前屏幕是否存在
        :param image_path: 模板路径
        :return: <bool>
        """
        x, y = self.find_image(image_path)
        return x != -1 and y != -1
