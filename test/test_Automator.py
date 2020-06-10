from unittest import TestCase
from Automator import Automator


class TestAutomator(TestCase):
    def test_check_equipment(self):
        app = Automator()
        path = "test_equipment_img"
        res = app.check_equipment(path)
        print(res)
