#tests functions from baseclass.py

import unittest
import os
import sys


#TODO REMOVE WHEN THE ACTUAL PACKAGE IS MADE
#Exposes baseclass.py to script
PACKAGE_PARENT = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from src.classes.baseclass import DataObject, DataList


class TestDataList(unittest.TestCase):
    def test_set_table(self) -> None:
        cur: DataList
        cur = DataList()
        cur.set_table("abc")
        self.assertEqual(cur.table, "abc")

    def test_generate_query(self) -> None:
        cur: DataList
        cur = DataList()
        query: str
        query = cur.generate_query("TABLE", {"key1": "val1", "key2": "val2"})
        self.assertEqual(query, "SELECT 'key1','key2' FROM TABLE")

    def test_set_query(self) -> None:
        cur: DataList
        cur = DataList()
        cur.set_query("TABLE", {"key1": "val1", "key2": "val2"})
        self.assertEqual(cur.query, "SELECT 'key1','key2' FROM TABLE")

    def test_add_object(self) -> None:
        cur: DataList
        cur = DataList()
        cur_object: DataObject
        cur_object = DataObject("123")
        cur.add_object(cur_object)
        self.assertEqual(cur.objects[0], cur_object)

    def test_create_object(self) -> None:
        cur: DataList
        cur = DataList()
        cur_object = cur.create_object("123")
        self.assertEqual(cur.objects[0], cur_object)

    def test_connection(self) -> None:
        cur: DataList
        cur = DataList()
        with cur.connect() as cnxn:
            with cnxn.cursor() as cursor:
                cursor.close()
            cnxn.close()
        self.assertEqual(1, 1)

    def test_fill_data_from_table(self) -> None:
        # TODO
        pass

    def test_fill(self) -> None:
        # TODO
        pass

    def test_get_with_number(self) -> None:
        cur: DataList
        cur = DataList()
        low: int
        low = 0
        high: int
        high = 5
        for i in range(low, high):
            cur.create_object(str(i))
        for i in range(low, high):
            self.assertIsNotNone(cur.get_with_number(cur.objects, str(i)))

    def test_get_all_with_number(self) -> None:
        cur: DataList
        cur = DataList()
        low: int
        low = 0
        high: int
        high = 5
        loops: int
        loops = 5
        for j in range(0, loops):
            for i in range(low, high):
                cur.create_object(str(i))
        for i in range(low, high):
            self.assertIsNotNone(cur.get_with_number(cur.objects, str(i)))
            self.assertEqual(loops, len(cur.get_all_with_number(cur.objects, str(i))))

    def test_print(self) -> None:
        cur_object: DataObject
        cur_object = DataObject("12321432")
        print(cur_object)


if __name__ == "__main__":
    unittest.main()
