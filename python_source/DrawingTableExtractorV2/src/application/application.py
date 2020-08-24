from abc import ABC, abstractmethod


class Application(ABC):

    @abstractmethod
    def open_document(self, filepath):
        pass

    @abstractmethod
    def create_document(self, filepath):
        pass

    @abstractmethod
    def start_app(self):
        pass

    @abstractmethod
    def stop_app(self):
        pass
