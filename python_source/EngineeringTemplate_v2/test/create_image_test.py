import unittest
from src.ptcc_module import Controller


class CreateImageTest(unittest.TestCase):
    def test_image_folder_does_not_exists(self):
        EQUATION_ANNOTATION_SPACE = "2in"
        FONT_NAME = "Times New Roman"
        FONT_SIZE = "12pt"
        IMAGE_FOLDER_NAME = "images_not_exists"

        test_controller = Controller(FONT_NAME, FONT_SIZE, EQUATION_ANNOTATION_SPACE, IMAGE_FOLDER_NAME)
        test_controller.create_image(images=["PPPP-CSXX 100 DRAWINGS\\1.01 SEAL 01.jpg", "PPPP-CSXX 100 DRAWINGS\\2.01 IGU 1.png"],
                                     captions=["Drawing Reference: 12.DT.641", "Drawing Reference: 11.PE.603"],
                                     width="300px",
                                     height="300px")
        self.assertEqual(len(test_controller.output.components), 0)

    def test_create_image_normal(self):
        EQUATION_ANNOTATION_SPACE = "2in"
        FONT_NAME = "Times New Roman"
        FONT_SIZE = "12pt"
        IMAGE_FOLDER_NAME = "images"

        test_controller = Controller(FONT_NAME, FONT_SIZE, EQUATION_ANNOTATION_SPACE, IMAGE_FOLDER_NAME)
        test_controller.create_image(images=["PPPP-CSXX 100 DRAWINGS\\1.01 SEAL 01.jpg", "PPPP-CSXX 100 DRAWINGS\\2.01 IGU 1.png"],
                                     captions=["Drawing Reference: 12.DT.641", "Drawing Reference: 11.PE.603"],
                                     width="300px",
                                     height="300px")
        self.assertEqual(len(test_controller.output.components), 1)
        self.assertEqual(len(test_controller.output.components[0].components), 2)

    def test_create_image_unequal(self):
        EQUATION_ANNOTATION_SPACE = "2in"
        FONT_NAME = "Times New Roman"
        FONT_SIZE = "12pt"
        IMAGE_FOLDER_NAME = "images"

        test_controller = Controller(FONT_NAME, FONT_SIZE, EQUATION_ANNOTATION_SPACE, IMAGE_FOLDER_NAME)
        test_controller.create_image(
            images=["PPPP-CSXX 100 DRAWINGS\\2.01 IGU 1.png"],
            captions=["Drawing Reference: 12.DT.641", "Drawing Reference: 11.PE.603"],
            width="300px",
            height="300px")
        self.assertEqual(len(test_controller.output.components), 0)

    def test_create_image_invalid_parameters(self):
        EQUATION_ANNOTATION_SPACE = "2in"
        FONT_NAME = "Times New Roman"
        FONT_SIZE = "12pt"
        IMAGE_FOLDER_NAME = "images"

        test_controller = Controller(FONT_NAME, FONT_SIZE, EQUATION_ANNOTATION_SPACE, IMAGE_FOLDER_NAME)
        test_controller.create_image(
            images="PPPP-CSXX 100 DRAWINGS\\2.01 IGU 1.png",
            captions=["Drawing Reference: 12.DT.641", "Drawing Reference: 11.PE.603"],
            width="300px",
            height="300px")
        self.assertEqual(len(test_controller.output.components), 0)
