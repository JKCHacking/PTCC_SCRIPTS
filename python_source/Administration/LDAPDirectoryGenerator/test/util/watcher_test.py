import unittest
from src.util.watcher import Watcher


class WatcherTest(unittest.TestCase):
    def test_set_value_001(self):
        '''A -> 1'''
        watcher = Watcher("A")
        watcher.set_value("1")
        self.assertTrue(watcher.has_changed())

    def test_set_value_002(self):
        '''1 -> 2'''
        watcher = Watcher("1")
        watcher.set_value("2")
        self.assertFalse(watcher.has_changed())

    def test_set_value_003(self):
        '''1 -> 2'''
        watcher = Watcher("2")
        watcher.set_value("B")
        self.assertTrue(watcher.has_changed())

    def test_set_value_004(self):
        '''B -> B'''
        watcher = Watcher("B")
        watcher.set_value("B")
        self.assertFalse(watcher.has_changed())

    def test_set_value_005(self):
        '''B -> B'''
        watcher = Watcher("B")
        watcher.set_value("C")
        self.assertTrue(watcher.has_changed())

    def test_set_value_006(self):
        '''All in one'''
        watcher = Watcher("A")
        watcher.set_value("1")
        self.assertTrue(watcher.has_changed())
        watcher.set_value("2")
        self.assertFalse(watcher.has_changed())
        watcher.set_value("B")
        self.assertTrue(watcher.has_changed())
        watcher.set_value("B")
        self.assertFalse(watcher.has_changed())
        watcher.set_value("C")
        self.assertTrue(watcher.has_changed())