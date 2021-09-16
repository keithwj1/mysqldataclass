import unittest
import os
import sys


# TODO REMOVE WHEN THE ACTUAL PACKAGE IS MADE
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from classes.purchaseorder import PurchaseReqList


class TestPurchaseReqList(unittest.TestCase):
    def test_fill(self) -> None:
        cur: PurchaseReqList
        cur = PurchaseReqList()
        cur.fill()
        self.assertGreater(len(cur.objects), 1)


if __name__ == "__main__":
    unittest.main()
