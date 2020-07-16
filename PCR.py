import os
import time

import Automator
from utils.Log import color_log as log


class PCR:
    # TODO: 打开模拟器 -> 连接加速器 -> 打开游戏
    def __init__(self):
        self.app = Automator.Automator()

    @staticmethod
    def start_emulator():
        cmd_str = r"O:\Nox\bin\Nox.exe " \
                  r"-clone:Nox_9  " \
                  r"-package:com.tencent.xriver"
        os.system(cmd_str)

    def check_vpn_ready(self):
        pass

    def enter_game_step_1(self):
        # 按任意键进入
        img_name = 'tw_img/btn_login_liandongziliao.jpg'
        log.info("正在进入游戏")
        x, y = self.app.find_image(img_name)
        self.app.d.click(x + 50, y + 50)
        time.sleep(5)
        log.info("尝试关闭账号绑定窗口")
        self.app.d.click(2, 2)
        time.sleep(5)  # 加载资源需要等待

    def skip_daily_rewards(self):
        img_name = 'tw_img/btn_skip_daily_rewards.jpg'
        log.info("尝试关闭登录奖励窗口")
        self.app.find_and_click(img_name)

    def close_announcement(self):
        # 关闭主页公告
        img_name = 'tw_img/btn_main_close.jpg'
        log.info("正在关闭主页公告")
        self.app.find_and_click(img_name)

    def enter_guild(self):
        # 进入公会
        img_name = 'tw_img/icon_guild.jpg'
        log.info("正在进入公会")
        self.app.find_and_click(img_name)

    def wait_to_enter_guild(self):
        log.info("正在准备公会内容")
        while True:
            if self.app.find_image('tw_img/pic_in_guild.jpg'):
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.log.info('公会准备完成')
                return
            else:
                time.sleep(3)

    def enter_game(self):
        """
        进入到游戏主页
        """
        self.enter_game_step_1()
        self.skip_daily_rewards()
        self.close_announcement()

    def enter_guild_and_donate(self):
        """
        转移到公会进行捐赠
        """
        self.enter_guild()
        self.wait_to_enter_guild()
        self.donate()

    def get_inventory(self):
        # 获取库存信息
        # 96*96 -> 128*128 540*960
        # 比例 [屏幕高]/10/[模板高]
        app = self.app
        result = app.check_equipment("equipment_img")  # 获取物品坐标、ID
        for item in result:
            print("*物品ID：{id} -> 数量：{amount}".format(id=item['path'], amount=item['amount']))
        return result

    def donate(self):
        """
        从当前界面开始捐赠
        """
        # TODO：检测捐赠进度/装备信息
        img_name = "tw_img/btn_donate_available.jpg"  # 检测捐赠状态
        if self.app.is_image_exist(img_name):  # 可捐赠
            self.app.find_and_click(img_name)
            self.app.find_and_click("tw_img/btn_donate_to_max.jpg")
            self.app.find_and_click("tw_img/btn_donate_ok.jpg")
            self.app.find_and_click("tw_img/btn_donate_finish.JPG")
            log.info("捐赠完毕")
        else:
            log.error("未检测到捐赠按钮")


if __name__ == '__main__':
    pcr = PCR()
    res = pcr.get_inventory()
    # print(res)
