from app.interfaces.InterfaceABC import InterfaceHandlerABC, IntrfaceABC
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from app.interfaces.console.CommandsList import CommandsList
from app.interfaces.console.CommandABC import CommandABC
from typing import Tuple
import re

class ConsoleInterface(IntrfaceABC):
    def __init__(self, commands_list: CommandsList) -> None:
        super().__init__()
        self.completer = NestedCompleter.from_nested_dict({ k: None for k in  commands_list.pseudos_list })
        
    def input(self, input_text=">>> "):
        return (prompt(input_text, completer=self.completer)).strip()
    
    def output(self, *args):
        return print(*args)
    
class ConsoleHandler(InterfaceHandlerABC):
    def __init__(self, interface: IntrfaceABC, commands_list: CommandsList):
        super().__init__(interface)
        self.commands_list = commands_list
        
    def __parse_input(self, input_string) -> Tuple[CommandABC, list]:
        searching_pseudo = next((pseudo for pseudo in self.commands_list.pseudos_list if re.search(f"^({pseudo}(\s|$))", input_string)), None)
        if not searching_pseudo:
            raise UndefinedCommandException
        command = self.commands_list.get_command(searching_pseudo)
        args = input_string[len(searching_pseudo) + 1:].split(' ')
        return (command, list(filter(lambda arg: arg, args)))
    
    def __execute_comand(self, command: CommandABC, args: list = []):
        output = command.execute(args)
        if output:
            self.interface.output(output)
        
    
    def run(self):
        print(f'Hello!!! \r\nYoy can use "help" comand ')
        while True:
            try:
                input_string = self.interface.input()
                command, args = self.__parse_input(input_string)
                self.__execute_comand(command, args)
                if not command.next:
                    break
            except KeyboardInterrupt:
                command = self.commands_list.get_command('close')
                self.__execute_comand(command, [])
                break
            except UndefinedCommandException:
                print("We can't find this command, please try again or use help command.")

class UndefinedCommandException(Exception):
    pass