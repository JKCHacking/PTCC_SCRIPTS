import unittest
import os
from src.util.constants import Constants
from src.ldap_exporter import LdapExporter


class LdapExporterTest(unittest.TestCase):
    def test_convert_ldap_data_001(self):
        expected_data = {
          'design': {
            'ptcc': {
              'ptcc_industry people': {
                '3M Philippines': {
                  '3M Philippines': {
                    'cn': '3M Philippines',
                    'facsimileTelephoneNumber': [
                      '+63 (2) 8145872',
                      '+63 (2) 8420581',
                      '+63 (2) 8501157'
                    ],
                    'telephoneNumber': [
                      '+63 (2) 8133781 to 95',
                      '+63 (2) 8145888'
                    ]
                  }
                }
              }
            }
          }
        }

        testdata = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.txt")
        le = LdapExporter()
        actual_data = le.convert_ldap_data(testdata)
        self.assertEqual(expected_data, actual_data)

    def test_export_data_001(self):
        data_dict = {
            'design': {
                'ptcc': {
                    'ptcc_industry people': {
                        '3M Philippines': {
                            '3M Philippines': {
                                'cn': '3M Philippines',
                                'facsimileTelephoneNumber': [
                                    '+63 (2) 8145872',
                                    '+63 (2) 8420581',
                                    '+63 (2) 8501157'
                                ],
                                'telephoneNumber': [
                                    '+63 (2) 8133781 to 95',
                                    '+63 (2) 8145888'
                                ]
                            }
                        }
                    }
                }
            }
        }
        le = LdapExporter()
        le.file_name = "testdata001.txt"
        le.export_data(data_dict)
