from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    async def ask(self, diff: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses.")


