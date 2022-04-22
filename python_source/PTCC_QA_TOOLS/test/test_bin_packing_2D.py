import unittest
import array
from src.bin_packing_2D import Bin
from src.bin_packing_2D import Item
from src.bin_packing_2D import get_app


class BinPacking2DTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bs_app = get_app()
        self.doc = self.bs_app.ActiveDocument
        self.bin = None
        self.items = []

    def tearDown(self) -> None:
        self.bin.obj.Delete()
        for i in self.items:
            i.obj.Delete()

    def test_floating_item(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item = Item(self.doc, [0, 150, 0], 25, 50)
        self.items.append(item)
        self.assertEqual(self.bin.is_fit(item), -1)

    def test_contact_fit(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item = Item(self.doc, [0, 150, 0], 25, 50)
        item.obj.Move(array.array("d", item.position), array.array("d", self.bin.position))
        self.items.append(item)
        self.assertTrue(self.bin.is_fit(item))

    def test_not_fit(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item = Item(self.doc, [0, 0, 0], 100, 200)
        self.items.append(item)
        self.assertFalse(self.bin.is_fit(item))

    def test_add_item(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item = Item(self.doc, [0, 150, 0], 25, 50)
        self.items.append(item)
        self.assertTrue(self.bin.add_item(item))

    def test_add_items_fit(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item1 = Item(self.doc, [0, 150, 0], 25, 50)
        item2 = Item(self.doc, [75, 150, 0], 25, 50)
        self.items.append(item1)
        self.items.append(item2)
        self.assertTrue(self.bin.add_item(item1))
        self.assertTrue(self.bin.add_item(item2))

    def test_add_items_fit_above(self):
        self.bin = Bin(self.doc, [0, 0, 0], 50, 100)
        item1 = Item(self.doc, [0, 150, 0], 25, 50)
        item2 = Item(self.doc, [75, 150, 0], 50, 50)
        self.items.append(item1)
        self.items.append(item2)
        self.assertTrue(self.bin.add_item(item1))
        self.assertTrue(self.bin.add_item(item2))
