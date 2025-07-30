from ..engine_pipe_impl import SimulationEngineImpl
from ..engine_pipe_abstract import EnginePlatform


class UnrealEngineImpl(SimulationEngineImpl):

    @property
    def engine_platform(self) -> str:
        return EnginePlatform.unreal.name
