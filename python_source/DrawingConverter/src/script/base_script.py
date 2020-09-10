from abc import ABC, abstractmethod


class BaseScript(ABC):
    @abstractmethod
    def open_file(self, document):
        pass

    @abstractmethod
    def save_file(self, document):
        pass

    @abstractmethod
    def delete_file(self, document):
        pass
