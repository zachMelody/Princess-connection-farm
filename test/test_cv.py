from unittest import TestCase
from Automator import Automator
from cv import UIMatcher

THRESHOLD = 0.88


class TestUIMatcher(TestCase):
    def test_template_match(self):
        app = Automator()
        screenshot = app.d.screenshot(format="opencv")
        res = UIMatcher.template_match(screenshot, "../tw_img/icon_guild.jpg")
        self.assertLessEqual(THRESHOLD, res['r'])
        self.assertLessEqual(0, res['x'])
        self.assertLessEqual(0, res['y'])
        print(res)

    def test_multi_scale_template_match(self):
        app = Automator()
        screenshot = app.d.screenshot(format="opencv")
        res = UIMatcher.multi_scale_template_match(screenshot, "../equipment_img/115011.webp")
        # res = UIMatcher.multi_scale_template_match(screenshot, "../tw_img/icon_guild.jpg")
        self.assertLessEqual(THRESHOLD, res['r'])
        self.assertLessEqual(0, res['x'])
        self.assertLessEqual(0, res['y'])
        print(res)
