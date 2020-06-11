import os
import time

import Automator
from utils.Log import color_log as log


class PCR:
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

    def close_announcement(self):
        # 关闭主页公告
        img_name = 'tw_img/btn_main_close.jpg'
        log.info("正在关闭主页公告")
        # time.sleep(10)
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
        self.enter_game_step_1()
        self.close_announcement()
        self.enter_guild()
        self.wait_to_enter_guild()

    def get_inventory(self):
        # TODO: 获取库存信息
        app = self.app
        result = app.check_equipment("equipment_img")
        print(result)

    def donate(self):
        # TODO：执行捐赠
        pass

    def _check_donate_status(self):
        # TODO: 检测捐赠状态/物品信息/关卡
        pass


if __name__ == '__main__':
    pcr = PCR()
    pcr.enter_game()
