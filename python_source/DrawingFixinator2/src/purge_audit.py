#!usr/bin/env python

#################################
# Author: Joshnee Kim B. Cunanan
# last Modified: 02 Feb 2020
# Version: 3.0
#################################

from logger import Logger
from drawing_script import DrawingScript


class PurgeAudit(DrawingScript):
    def __init__(self):
        self.logger = Logger().get_logger()

    def begin_automation(self, document, file_name):
        self.__purge_document(document, file_name)
        self.__audit_document(document, file_name)

    def __purge_document(self, document, file_name):
        if document:
            for i in range(0, 5):
                self.logger.info("[ATTEMPT{}]Purging Drawing: {}...".format(i+1, file_name))
                document.PurgeAll()
        self.logger.info("Purging Drawing Done...")

    def __audit_document(self, document, file_name):
        self.logger.info("Auditing Drawing: {}...".format(file_name))
        if document:
            document.AuditInfo(True)
        self.logger.info("Auditing Drawing Done...")
