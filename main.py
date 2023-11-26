from app.interfaces.console import ConsoleHandler, ConsoleInterface
from app.interfaces.console.CommandsList import CommandsList
from app.interfaces.console import Commands as commands

commands_list = CommandsList()

commands_list.add_command(pseudos=('help',), command=commands.HelpCommand(commands_list=commands_list))
commands_list.add_command(pseudos=('close', 'exit', 'good bye', 'bye'), command=commands.CloseCommand())
commands_list.add_command(pseudos=('search',), command=commands.SearchCommand())
commands_list.add_command(pseudos=('add contact',), command=commands.AddContactCommand())
commands_list.add_command(pseudos=('add phone', 'add phones'), command=commands.AddPhonesCommand())
commands_list.add_command(pseudos=('add birthday', ), command=commands.AddBirthdayCommand())
commands_list.add_command(pseudos=('add address', ), command=commands.AddAddress())
commands_list.add_command(pseudos=('add mail', ), command=commands.AddMail())
commands_list.add_command(pseudos=('remove contact', ), command=commands.RemoveContactCommand())
commands_list.add_command(pseudos=('show contact', ), command=commands.ShowContactCommand())
commands_list.add_command(pseudos=('change phone', ), command=commands.ChangePhoneCommand())
commands_list.add_command(pseudos=('remove phone', ), command=commands.RemovePhoneCommand())
commands_list.add_command(pseudos=('days to birthday',), command=commands.DaysToBirthday())
commands_list.add_command(pseudos=('birthdays range',), command=commands.BirthdaysRange())
commands_list.add_command(pseudos=('show all', ), command=commands.ShowAllContacts())
commands_list.add_command(pseudos=('add note',), command=commands.AddNoteCommand())
commands_list.add_command(pseudos=('update note',), command=commands.UpdateNoteCommand())
commands_list.add_command(pseudos=('delete note',), command=commands.DeleteNoteCommand())
commands_list.add_command(pseudos=('searh note',), command=commands.SearchNoteCommand())
commands_list.add_command(pseudos=('sort file',), command=commands.SortFilesCommand())

INTERFACE_HANDLERS = [ ConsoleHandler(interface=ConsoleInterface(commands_list=commands_list), commands_list=commands_list) ]

def main():
    for handler in INTERFACE_HANDLERS:
        handler.run()

if __name__ == "__main__":
    main()