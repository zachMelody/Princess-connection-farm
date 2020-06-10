import os
import Automator
import time


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
        self.app.find_and_click(img_name)

    def close_announcement(self):
        # 关闭主页公告
        img_name = 'tw_img/btn_main_close.jpg'
        self.app.find_and_click(img_name)

    def enter_guild(self):
        # 进入公会
        img_name = 'tw_img/icon_guild.jpg'
        self.app.find_and_click(img_name)

    def wait_to_enter_guild(self):
        while True:
            if self.app.find_image('tw_img/pic_in_guild.jpg'):
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.d.swipe(0.8, 0.524, 0.804, 0.216)
                self.app.log.info('成功进入公会')
                return
            else:
                time.sleep(3)

    def enter_game(self):
        self.enter_game_step_1()
        self.close_announcement()
        self.enter_guild()
        self.wait_to_enter_guild()

    def getInventory(self):
        app = self.app
        app.check_equipment("equipment_img")


if __name__ == '__main__':
    pcr = PCR()
    # pcr.app.start()
    pcr.enter_game()
