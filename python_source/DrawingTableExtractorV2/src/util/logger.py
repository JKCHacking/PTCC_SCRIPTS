#!/usr/bin/env python3

import logging
import datetime

LOG_FORMAT = "[%(asctime)s.%(msecs)d][%(levelname)s][%(module)s:%(lineno)03d]:"\
    + " %(message)s"


class Logger(object):

    def __init__(self, logger_name):
        self.logger_name = logger_name
        datetime_now = datetime.datetime.now()
        date = datetime_now.date
        month = datetime_now.month
        year = datetime_now.year
        hour = datetime_now.hour
        minute = datetime_now.minute

        logging.basicConfig(filename=f'log_{date}{month}{year}{hour}{minute}.txt', level=logging.INFO)
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(LOG_FORMAT)
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    @staticmethod
    def terminate_logger():
        logging.shutdown()

    def get_logger(self):
        return logging.getLogger(self.logger_name)


def get_logger(logger_name):
    logger = Logger(logger_name)
    return logger.get_logger()
