#!/usr/bin/env python3

import logging

LOGGER_NAME = "Task_Tracker_Logger"
LOG_FORMAT = "[%(asctime)s.%(msecs)d][%(levelname)s][%(module)s:%(lineno)03d]:"\
    + " %(message)s"

class Logger(object):

    def __init__(self):
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    def terminate_logger(self):
        logging.shutdown()

    def get_logger(self):
        return logging.getLogger(LOGGER_NAME)
