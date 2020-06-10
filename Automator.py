import uiautomator2 as u2
import time
from cv import *
import glob
from utils.Log import color_log as log


class Automator:
    BASE_IMG_PATH = 'tw_img/'
    MAX_COUNTER = 5

    def __init__(self):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect()
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False
        self.log = log
        self.failCounter = 0

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

    def find_image(self, image_path, threshold=0.90):
        """
        查找当前屏幕上是否有图像
        :param image_path: 图像路径
        :param threshold: 阈值
        :return:
        """
        if self.failCounter > Automator.MAX_COUNTER:
            self.failCounter = 0
            return -1, -1

        screen = self.d.screenshot(format="opencv")
        result = UIMatcher.template_match(screen, image_path)
        self.log.info("IMAGE: {} -> 相似度: {:.3f}".format(image_path, result['r']))
        if result['r'] > threshold:
            self.failCounter = 0
            self.log.info("查找成功")
            return result['x'], result['y']
        else:
            self.log.error("查找失败")
            time.sleep(8)
            return self.find_image(image_path)

    def find_and_click(self, image_path):
        x, y = self.find_image(image_path)
        if x == -1 and y == -1:
            self.log.error("点击失败")
        else:
            time.sleep(5)
            self.d.click(x, y)

    def check_equipment(self, template_path):
        """
        查找装备
        :param template_path: 模板目录
        :return: {'r': 相似度, 'x': x坐标, 'y': y坐标， 'path': 模板路径}
        """
        THRESHOLD = 0.3
        found = None
        return_list = list()
        # 遍历所有的图片寻找模板
        for imagePath in glob.glob(template_path + "/*"):
            self.log.debug("> " + imagePath)
            screen = self.d.screenshot(format="opencv")
            result = UIMatcher.multi_scale_template_match(screen, imagePath)

            if result['r'] > THRESHOLD:
                result['path'] = imagePath
                return_list.append(result)

        return return_list

    def get_screen_state(self, screen):
        # TODO: 判断当前状态
        pass
