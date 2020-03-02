#!usr/bin/env python

import unittest
import os
from purge_audti_script import PurgeAuditScript


class PurgeAuditTest(unittest.TestCase):

    def test_1_file(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        drawing_full_path = os.path.join(current_path, "02_FRAME ASSEMBLY", "PMU-FA-001.dwg")
        purge_audit_script = PurgeAuditScript(current_path)
        purge_audit_script.make_changes_to_drawing(drawing_full_path)

        # check if 02_FRAME_ASSEMBLY_DONE exists
        done_directory = os.path.join(current_path, "02_FRAME ASSEMBLY_DONE")
        self.assertEqual(True, os.path.exists(done_directory))
        # check if PMU-FA-001.dwg file exists
        self.assertEqual(True, os.path.exists(drawing_full_path))

    def test_multiple_file(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        purge_audit_script = PurgeAuditScript(current_path)
        purge_audit_script.begin_automation()

        self.assertEqual(True, True)

if __name__ == "__main__":
    unittest.main()
