import sys
import io
import unittest
from src.ptcc_module import ImageWriter, CustomDisplay


class ImageWriterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.c_disp = CustomDisplay()
        self.old_stdout = sys.stdout
        sys.stdout = self.buffer = io.StringIO()

    def tearDown(self) -> None:
        sys.stdout = self.old_stdout

    def test_image_folder_not_exist(self):
        ImageWriter("picture_test", self.c_disp)
        self.assertEqual("image folder does not exists.\n", self.buffer.getvalue())

    def test_image_folder_exist(self):
        ImageWriter("image_test", self.c_disp)
        self.assertEqual("", self.buffer.getvalue())

    def test_image_does_not_exist(self):
        img_writer = ImageWriter("image_test", self.c_disp)
        img_writer.define(image_names=["unknown_image1.jpg", "unknown_image2.jpg"], captions=["caption 1", "caption 2"])
        self.assertEqual("Image unknown_image1.jpg does not exists\nImage unknown_image2.jpg does not exists\n", self.buffer.getvalue())

    def test_image_does_exist(self):
        img_writer = ImageWriter("image_test", self.c_disp)
        img_writer.define(image_names=["1.01 SEAL 01.jpg", "2.01 IGU 1.png"], captions=["caption 1", "caption 2"])
        self.assertEqual("", self.buffer.getvalue())

    def test_image_caption_unequal(self):
        img_writer = ImageWriter("image_test", self.c_disp)
        img_writer.define(image_names=["1.01 SEAL 01.jpg", "2.01 IGU 1.png"], captions=["caption 1"])
        self.assertEqual("number of image names and caption names does not match.\n", self.buffer.getvalue())
