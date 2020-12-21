import unittest
import os
from src.util.constants import Constants
from src.ldap_exporter import LdapExporter


class LdapExporterTest(unittest.TestCase):
    def test_get_data_001(self):
        '''
            d = {
                "dc=design": {
                    "dc=ptcc": {
                        "ou=ptcc_industry people": {
                            "member": [
                                {
                                    "ou=3M Philippines": {
                                        "member": [
                                            {
                                                "cn=3M Philippines": {
                                                    "facsimileTelephoneNumber": [
                                                        "+63 (2) 8145872",
                                                        "+63 (2) 8420581",
                                                        "+63 (2) 8501157"
                                                    ],
                                                    "telephoneNumber":[
                                                        "+63 (2) 8133781 to 95",
                                                        "+63 (2) 8145888"
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                },
                            ]
                        }
                    }
                }
            }
        '''
        testdata = os.path.join(Constants.TEST_DIR, "testdata", "testdata001.txt")
        le = LdapExporter()
        le.get_data(testdata)
