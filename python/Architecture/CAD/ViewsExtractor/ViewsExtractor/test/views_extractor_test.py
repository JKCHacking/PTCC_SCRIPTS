import unittest
import os
from src.views_extractor import ViewsExtractor
from src.constants import Constants


class ViewsExtractorTest(unittest.TestCase):
    def test_adding_balloon(self):
        ve = ViewsExtractor(Constants.OUTPUT_DIR, ["front", "top", "left"])
        dwg_path = ve.extract_2d_views(os.path.join(Constants.INPUT_DIR, "U001_OPP", "U001_OPP.iam"))

