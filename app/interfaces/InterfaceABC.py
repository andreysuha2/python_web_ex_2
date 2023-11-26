from abc import abstractmethod, ABCMeta

class IntrfaceABC(metaclass=ABCMeta):
    @abstractmethod
    def input(self, *args):
        pass
    
    @abstractmethod
    def output(self, *args):
        pass
    
class InterfaceHandlerABC(metaclass=ABCMeta):
    def __init__(self, interface: IntrfaceABC,):
        self.interface = interface
        
    @abstractmethod 
    def run(self, *args):
        pass