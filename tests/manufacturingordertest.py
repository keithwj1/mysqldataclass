import unittest
import os
import sys


# TODO REMOVE WHEN THE ACTUAL PACKAGE IS MADE
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from classes.manufacturingorder import ManufacturingOrderList, ManufacturingOrder


class TestManufacturingOrderList(unittest.TestCase):
    def test_fill(self) -> None:
        cur: ManufacturingOrderList
        cur = ManufacturingOrderList()
        # REMOVE TO RUN TEST
        # return
        cur.fill()
        self.assertGreater(len(cur.objects), 0)


class TestManufacturingOrder(unittest.TestCase):
    def test_print(self) -> None:
        cur_object: ManufacturingOrder
        cur_object = ManufacturingOrder("1231982731")
        print(cur_object)


if __name__ == "__main__":
    unittest.main()
