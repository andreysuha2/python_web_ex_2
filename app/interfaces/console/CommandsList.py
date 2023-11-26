from .CommandABC import CommandABC
from collections import UserDict
from typing import Tuple, List

class CommandsList(UserDict):
    @property
    def pseudos_list(self) -> List[str]:
        return [ pseudo for pseudos in self.data.keys() for pseudo in pseudos ]
    
    def get_key(self, pseudo: str) -> Tuple[str]:
        return next((pseudos for pseudos in self.data.keys() if pseudo in pseudos), None)
    
    def has_command(self, pseudo: str) -> bool:
        return pseudo in self.pseudos_list
    
    def add_command(self, pseudos: Tuple[str], command: CommandABC) -> None:
        for pseudo in pseudos:
            if self.has_command(pseudo):
                raise TryToAddExistingPseudoException
        self.data[pseudos] = command
        
    def get_command(self, pseudo: str) -> CommandABC:
        key = self.get_key(pseudo)
        if key:
            return self.data[key]
        else:
            raise PseudoNotFoundException 
            
class TryToAddExistingPseudoException(Exception):
    pass

class PseudoNotFoundException(Exception):
    pass