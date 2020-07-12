import cv2
import imutils
import matplotlib.pylab as plt
import numpy as np

from utils import Log

DEBUG = False
ENABLE_CALC_TIME = False

class UIMatcher:
    @staticmethod
    def RotateClockWise90(img):
        trans_img = cv2.transpose(img)
        new_img = cv2.flip(trans_img, 0)
        return new_img

    @staticmethod
    def template_match(screen, template_path):
        """
        模板匹配
        :param screen: 屏幕截图
        :param template_path: 模板路径
        :return: {'r': 相似度, 'x': x坐标, 'y': y坐标}
        """
        res = {'r': 0.0,
               'x': 0,
               'y': 0}

        # 旋转屏幕截图
        if screen.shape[0] > screen.shape[1]:
            screen = UIMatcher.RotateClockWise90(screen)
        height, width = screen.shape[0:2:1]
        raw_screen = screen.copy()  # DEBUG
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        # 读取模板
        template = cv2.imdecode(np.fromfile(template_path, dtype=np.uint8),
                                cv2.IMREAD_GRAYSCALE)
        # 模板匹配
        result = cv2.matchTemplate(template, screen, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        # 计算坐标
        h, w = template.shape[0:2:1]
        res['x'] = max_loc[0] + w / 2
        res['y'] = max_loc[1] + h / 2
        res['r'] = max_val
        # DEBUG
        if DEBUG:
            UIMatcher._plot_boundary(raw_screen, template, max_loc)

        return res

    @staticmethod
    def _plot_boundary(screen, template, max_loc):
        """
        绘制模板在屏幕上的区域
        :param screen: 屏幕截图
        :param template: 模板图像
        :param max_loc: 匹配信息
        :return: void
        """
        h, w = template.shape[0:2:1]
        cv2.rectangle(screen,
                      (int(max_loc[0]), int(max_loc[1])),
                      (int(max_loc[0] + w), int(max_loc[1] + h)),
                      (0, 0, 255), 2)
        plt.cla()
        matched_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
        plt.imshow(matched_screen)
        plt.pause(0.01)

    @staticmethod
    def _multi_scale_template_match(screen, template_path):
        """
        慢的一匹，谁用谁傻逼（我
        -> 然而是因为DEBUG的原因（大概
        :param screen:
        :param template_path:
        :return:
        """
        # result = UIMatcher.template_match(screen, template_path)
        found = None
        # 循环遍历不同的尺度
        for scale in np.linspace(1.4, 0.6, 50)[::-1]:
            # 根据尺度大小对输入图片进行裁剪
            resized = imutils.resize(screen, width=int(screen.shape[1] * scale))
            result = UIMatcher.template_match(resized, template_path)
            # 如果发现一个新的关联值则进行更新
            if found is None or result['r'] > found['r']:
                found = result

        return found

    @staticmethod
    def multi_scale_template_match(screen, template_path, min_scale=0.8, max_scale=1.4, step=40):
        """
        多尺度模板匹配
        :param screen: 屏幕截图
        :param template_path: 模板路径
        :param min_scale: 比例下限
        :param max_scale: 比例上限
        :param step: 比例划分次数（数字越大准确度越高，但是耗时）
        :return: {'r': 相似度, 'x': x坐标, 'y': y坐标}
        """
        if ENABLE_CALC_TIME:
            import time
            start_time = time.time()
            print(start_time)
        # 旋转屏幕截图
        if screen.shape[0] > screen.shape[1]:
            screen = UIMatcher.RotateClockWise90(screen)
        raw_screen = screen.copy()  # DEBUG
        # 读取模板图片
        template = cv2.imread(template_path)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        # 执行边缘检测
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]
        # 显示模板
        if DEBUG:
            plt.imshow(template)
            plt.pause(0.01)
        # 读取测试图片并将其转化为灰度图片
        gray = cv2.cvtColor(raw_screen, cv2.COLOR_BGR2GRAY)
        found = None
        # 循环遍历不同的尺度
        for scale in np.linspace(max_scale, min_scale, step)[::-1]:
            # 根据尺度大小对输入图片进行裁剪
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])
            # 如果裁剪之后的图片小于模板的大小直接退出
            if resized.shape[0] < tH or resized.shape[1] < tW:
                continue
            # 首先进行边缘检测，然后执行模板检测，接着获取最小外接矩形
            edged = cv2.Canny(resized, 50, 200)
            # plt.imshow(edged)
            result = cv2.matchTemplate(template, edged, cv2.TM_CCOEFF_NORMED)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # 结果可视化
            if DEBUG:  # 绘制矩形框并显示结果
                # clone = np.dstack([edged, edged, edged])
                # cv2.rectangle(clone, (maxLoc[0], maxLoc[1]), (maxLoc[0] + tW, maxLoc[1] + tH), (0, 0, 255), 2)
                # plt.imshow(clone)
                # plt.pause(0.01)
                Log.color_log.info("> 比例：%.2f -> 相似度：%.2f", scale, maxVal)

            # 如果发现一个新的关联值则进行更新
            if found is None or maxVal > found[0]:
                found = (maxVal, maxLoc, r)

        # 计算测试图片中模板所在的具体位置，即左上角和右下角的坐标值，并乘上对应的裁剪因子
        (_, maxLoc, r) = found
        (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
        (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

        # 绘制并显示结果
        if DEBUG:
            matched_screen = cv2.rectangle(raw_screen, (startX, startY), (endX, endY), (0, 0, 255), 2)
            matched_screen = cv2.cvtColor(matched_screen, cv2.COLOR_BGR2RGB)
            plt.imshow(matched_screen)
            plt.pause(0.01)
            try:
                plt.imsave("res_" + template_path, matched_screen)
            except FileNotFoundError:
                import os
                os.makedirs("res_" + template_path)
        if ENABLE_CALC_TIME:
            end_time = time.time()
            print(end_time)
            Log.color_log.debug("耗时：%.2f", end_time - start_time)

        # 计算坐标
        res = dict()
        res['x'] = (startX + endX) / 2
        res['y'] = (startY + endY) / 2
        res['r'] = found[0]
        Log.color_log.debug(res)

        return res
