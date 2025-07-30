from abc import ABC, abstractmethod


class AppPath(ABC):

    @classmethod
    @abstractmethod
    def get_root_path(cls):
        pass
    pass
