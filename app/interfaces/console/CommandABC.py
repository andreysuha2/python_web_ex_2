from abc import ABCMeta, abstractmethod

class CommandABC(metaclass=ABCMeta):
    _name = None
    _description = None
    _next = True
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def next(self) -> bool:
        return self._next
    
    @abstractmethod
    def execute(self, *args) -> str | None:
        pass