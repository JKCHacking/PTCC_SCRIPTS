import unittest
import os
from src.mc_py_interface import MCPyScript
from src.constants import Constants


class McPyInterfaceTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_import_image(self):
        script_obj = MCPyScript(os.path.join(Constants.TEST_DIR, "testdata", "test2.xmcd"))
        image_fp_ls = [os.path.join(Constants.TEST_DIR, 'testdata', 'input', 'Deflection Magnitudes', 'Stainless Steel Sheet', 'image_test2_jpg.jpg')]
        script_obj.import_images(image_fp_ls)
        self.assertEquals(True, True)