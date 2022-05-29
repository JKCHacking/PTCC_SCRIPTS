#!usr/bin/env python

from abc import ABC, abstractmethod


class DrawingScript(ABC):

    @abstractmethod
    def begin_automation(self, document, file_name):
        pass
