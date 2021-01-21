import unittest
import os
from collections import OrderedDict
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

    def test_convert_ldap_data_002(self):
        expected_data = \
        {
          "design": {
            "ptcc": {
              "ptcc_industry people": {
                "08DB ACOUSTIC ENVIRONMENTS": {
                  "facsimileTelephoneNumber": "+63 2 718-0088",
                  "registeredAddress": "23Floor Unit B Summit One Tower, 530 Shaw Blvd., Mandaluyong City, 1552 Metro Manila, Philippines",
                  "telephoneNumber": "+63 2 718-0808",
                  "Joseph N. Tan": {
                    "facsimileTelephoneNumber": [
                      "Telefax: +63 2 533-0808",
                      "+63 2 718-0088"
                    ],
                    "mail": "info@zeroeightdb.com",
                    "mobile": "+63 917 891-8471",
                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                    "telephoneNumber": [
                      "Direct: +63 2 531-0808",
                      "Trunk: +63 2 718-0808"
                    ]
                  },
                  "George Lee": {
                    "facsimileTelephoneNumber": "+63 2 718-0088",
                    "mail": [
                      "zeroeightdb@yahoo.com",
                      "admin@zeroeightdb.com"
                    ],
                    "mobile": "+63 915 880-0088",
                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                    "telephoneNumber": "+63 2 718-0808"
                  }
                }
              }
            }
          }
        }

        testdata = os.path.join(Constants.TEST_DIR, "testdata", "testdata003.txt")
        le = LdapExporter()
        actual_data = le.convert_ldap_data(testdata)
        self.assertEqual(expected_data, actual_data)

    def test_sort_data_001(self):
        """
        this will test the sorting logic of a dictionary
        """
        expected_data_dict = \
            OrderedDict({
                "design": {
                    "ptcc": {
                        "A": {
                            "D": {
                                "D": {},
                                "E": {},
                                "F": {}
                            },
                            "E": {
                                "A": {},
                                "B": {},
                                "C": {}
                            }
                        },
                        "B": {
                            "X": {},
                            "Y": {},
                            "Z": {}
                        },
                        "C": {
                            "L": {
                                "A": {},
                                "B": {},
                                "C": {}
                            },
                            "M": {
                                "A": {},
                                "B": {},
                                "C": {}
                            },
                            "N": {
                                "A": {},
                                "B": {},
                                "C": {}
                            }
                        }
                    }
                }
            })
        raw_data_dict = \
            {
                "design": {
                    "ptcc": {
                        "A": {
                            "E": {
                                "C": {},
                                "B": {},
                                "A": {},
                            },
                            "D": {
                                "F": {},
                                "E": {},
                                "D": {}
                            }
                        },
                        "C": {
                            "N": {
                                "C": {},
                                "B": {},
                                "A": {}
                            },
                            "M": {
                                "C": {},
                                "B": {},
                                "A": {}
                            },
                            "L": {
                                "C": {},
                                "B": {},
                                "A": {}
                            }
                        },
                        "B": {
                            "Z": {},
                            "Y": {},
                            "X": {}
                        }
                    }
                }
            }
        le = LdapExporter()
        actual_data = le.sort_data(raw_data_dict)
        print(actual_data)
        self.assertEqual(expected_data_dict, actual_data)

    def test_sort_data_002(self):
        raw_data_dict = {
            'design': {
                'ptcc': {
                    'ptcc_industry people': {
                        '3M Philippines': {
                            '3M Philippines': {
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
        actual_data = le.sort_data(raw_data_dict)
        print(actual_data)
        # self.assertEqual(expected_data_dict, actual_data)

    def test_sort_data_003(self):
        raw_data_dict = \
            {
                "design": {
                    "ptcc": {
                        "ptcc_industry people": {
                            "08DB ACOUSTIC ENVIRONMENTS": {
                                "facsimileTelephoneNumber": "+63 2 718-0088",
                                "registeredAddress": "23Floor Unit B Summit One Tower, 530 Shaw Blvd., Mandaluyong City, 1552 Metro Manila, Philippines",
                                "telephoneNumber": "+63 2 718-0808",
                                "Joseph N. Tan": {
                                    "facsimileTelephoneNumber": [
                                        "Telefax: +63 2 533-0808",
                                        "+63 2 718-0088"
                                    ],
                                    "mail": "info@zeroeightdb.com",
                                    "mobile": "+63 917 891-8471",
                                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                                    "telephoneNumber": [
                                        "Direct: +63 2 531-0808",
                                        "Trunk: +63 2 718-0808"
                                    ]
                                },
                                "George Lee": {
                                    "facsimileTelephoneNumber": "+63 2 718-0088",
                                    "mail": [
                                        "zeroeightdb@yahoo.com",
                                        "admin@zeroeightdb.com"
                                    ],
                                    "mobile": "+63 915 880-0088",
                                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                                    "telephoneNumber": "+63 2 718-0808"
                                }
                            }
                        }
                    }
                }
            }
        le = LdapExporter()
        actual_data = le.sort_data(raw_data_dict)
        print(actual_data)
        # self.assertEqual(expected_data_dict, actual_data)

    def test_export_data_001(self):
        data_dict = {
            'design': {
                'ptcc': {
                    'ptcc_industry people': {
                        '3M Philippines': {
                            '3M Philippines': {
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
        le.file_name = "testoutput001.txt"
        le.export_data(data_dict)

    def test_export_data_002(self):
        data_dict = \
            {
                "design": {
                    "ptcc": {
                        "ptcc_industry people": {
                            "08DB ACOUSTIC ENVIRONMENTS": {
                                "facsimileTelephoneNumber": "+63 2 718-0088",
                                "registeredAddress": "23Floor Unit B Summit One Tower, 530 Shaw Blvd., Mandaluyong City, 1552 Metro Manila, Philippines",
                                "telephoneNumber": "+63 2 718-0808",
                                "Joseph N. Tan": {
                                    "facsimileTelephoneNumber": [
                                        "Telefax: +63 2 533-0808",
                                        "+63 2 718-0088"
                                    ],
                                    "mail": "info@zeroeightdb.com",
                                    "mobile": "+63 917 891-8471",
                                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                                    "telephoneNumber": [
                                        "Direct: +63 2 531-0808",
                                        "Trunk: +63 2 718-0808"
                                    ]
                                },
                                "George Lee": {
                                    "facsimileTelephoneNumber": "+63 2 718-0088",
                                    "mail": [
                                        "zeroeightdb@yahoo.com",
                                        "admin@zeroeightdb.com"
                                    ],
                                    "mobile": "+63 915 880-0088",
                                    "registeredAddress": "Unit-B 23F Summit One Tower, 530 Shaw Blvd., Mandaluyong City 1552, Metro Manila, Philippines",
                                    "telephoneNumber": "+63 2 718-0808"
                                }
                            }
                        }
                    }
                }
            }

        le = LdapExporter()
        le.file_name = "testoutput002.txt"
        le.export_data(data_dict)


