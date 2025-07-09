from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def ask(self, question: str, context: str) -> str:
        pass