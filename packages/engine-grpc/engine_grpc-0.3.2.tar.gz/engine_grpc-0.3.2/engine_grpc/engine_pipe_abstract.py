from abc import ABC, abstractmethod
from enum import Enum, auto

from .utils.singleton import SingletonABCMeta


class EnginePlatform(Enum):
    unknown = auto()
    unity = auto()
    unity_editor = auto()
    unreal = auto()
    godot = auto()
    blender = auto()  # refer to https://ciesie.com/post/blender_python_rpc/
    blender_2nd = auto()


class EngineAbstract(ABC):
    __metaclass__ = SingletonABCMeta

    @property
    @abstractmethod
    def stub(self):
        pass

    @property
    @abstractmethod
    def channel(self):
        pass

    @property
    @abstractmethod
    def event_loop(self):
        pass

    @property
    @abstractmethod
    def engine_platform(self) -> str:
        raise NotImplementedError
