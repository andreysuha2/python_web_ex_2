from app.AddressBook import AddressBook
from app.Fields import NameField, PhoneField, BirthdayField, Exceptions, MailField, AdressField
from app.Record import Record
from app.notes import Notebook, Note
from datetime import datetime, timedelta
from app.sort_file import SortFile
from app.interfaces.console.CommandABC import CommandABC
from app.interfaces.console.CommandsList import CommandsList, PseudoNotFoundException
from typing import Tuple

ADDRESS_BOOK = AddressBook(5)
NOTEBOOK = Notebook()

def input_error(handler):
    def inner(self, args):
        try:
            result = handler(self, *args)
            return result
        except KeyError:
            return f"Contact {args[0]} doesn't exist!"
        except ValueError:
            return "You are trying to set invalid value"
        except IndexError:
            return "You are sending invalid count of parameters. Please use help comand for hint"
        except Exceptions.PhoneValidationError as err:
            return str(err)
        except Exceptions.BirthdayValidationError as err:
            return str(err)
        except Exceptions.MailValidationError as err:
            return str(err)
    return inner

class CloseCommand(CommandABC):
    def __init__(self) -> None:
        self._next = False
        self._name = 'Close'
        self._description = '''
            syntax: close
            description: saved data and stoped proccess
            example: close
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        ADDRESS_BOOK.save_book()
        return "Thank you! Your data are saved"

class HelpCommand(CommandABC):
    def __init__(self, commands_list: CommandsList) -> None:
        self.commands_list = commands_list
        self._name = "Help"
        self._description = '''
            syntax: help
            description: help with other commands
            example: help {command}
        '''
    
    def _get_command_print(self, command: CommandABC, pseudos: Tuple[str]):
        return f'''
            name: {command.name}
            pseudos: {", ".join(pseudos)}
            {command.description}
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        command_pseudo = " ".join(args) if len(args) > 1 else None
        if(command_pseudo):
            try:
                command = self.commands_list.get_command(command_pseudo)
                pseudos = self.commands_list.get_key(command_pseudo)
                return self._get_command_print(command, pseudos)
            except PseudoNotFoundException:
                return f'Command {command_pseudo} not found'
        else:
            output = '---COMMANDS HELP---'
            for pseudos, command  in self.commands_list.items():
                output += f'\n{self._get_command_print(command, pseudos)}'
            return output
    
class SearchCommand(CommandABC):
    def __init__(self) -> None:
        self._name = 'Search'
        self._description = '''
            syntax: search {query_string}
            description: searching contact by any field
            example: search Ivan
        '''
    
    @input_error
    def execute(self, *args):
        text = args[0].lower()
        if not len(text) > 2:
            return 'Enter more then 2 simbols to find'
        list = ''
        for cont in AddressBook(1):
            if text in str(cont[2]).lower():
                list += str(cont[2])[1:-1] + '\r\n'
        return list if len(list) > 1 else 'Cant find it'
    
class AddContactCommand(CommandABC):
    def __init__(self) -> None:
        self._name = 'Add contact'
        self._description = '''
            syntax: add contact {name} {phone(s)}
            description: adding number and birthday(optional) to contacts list 
            example: add contact ivan +380999999999 +380777777777 01-01-1990
        '''
    
    @input_error
    def execute(self, *args):
        name, fields = args[0], args[1:]
        if name in ADDRESS_BOOK:
            return f'Contact with name "{name}" already exists.'
        name_field = NameField(name)
        phones_list = []
        errors = []
        birthday = None
        for field in fields:
            try:
                phone = PhoneField(field)
                phones_list.append(phone)
            except Exceptions.PhoneValidationError as phone_error:
                try:
                    birthday = BirthdayField(field)
                except Exceptions.BirthdayValidationError as birthday_error:
                    errors.append(str(phone_error) + '\n')
                    errors.append(str(birthday_error) + '\n')
        if not len(errors):
            record = Record(name_field, phones_list, birthday)
            ADDRESS_BOOK.add_record(record)
            return f'Contact "{name}" added to conctacts.'
        return f'Contact "{name}" can\'t be added:\n{"".join(errors)}'

class RemoveContactCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Remove contact"
        self._description = '''
            syntax: remove contact {name}
            description: removing contact from contacts list
            example: remove ivan
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        name = args[0]
        if name in ADDRESS_BOOK:
            ADDRESS_BOOK.pop(name)
            return f'Contact "{name}" removed from address book'
        return f'Contact "{name}" does\'t exists in address book'
    
class AddPhonesCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Add phones"
        self._description = '''
            syntax: add address {name} {address}
            description: adding address to contact name 
            example: add address ivan Kyiv
        '''
    
    @input_error
    def execute(self, *args) -> str:
        name, phones = args[0], args[1:]
        record = ADDRESS_BOOK.get_record(name)
        if record and len(phones):
            added_phones = []
            missed_phones = []
            invalid_phones = []
            response = ''
            for phone in set(phones):
                try:
                    result = record.add_phone(PhoneField(phone))
                    added_phones.append(phone) if result else missed_phones.append(phone)
                except Exceptions.PhoneValidationError:
                    invalid_phones.append(phone)
            if len(added_phones):
                response += f'Phones {", ".join(added_phones)} added to contact "{name}"\n'
            if len(missed_phones):
                response += f'Phones {", ".join(missed_phones)} already exists for contact "{name}"\n'
            if len(invalid_phones):
                response += f'Phones {", ".join(invalid_phones)} are invalid. For add phone please use format +380XXXXXXXXX'
            return response
        elif record and not len(phones):
            return "You send empty phones list"
        return f'Contact with name {name} doesn\'t exist'

class ChangePhoneCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Change phone"
        self._description = '''
            syntax: change phone {name} {old_phone_number} {new_phone_number}
            description: changing phone number for contact
            example: change phone ivan +380777777777 +380999999999
        '''
    
    @input_error
    def execute(self, *args) -> str:
        name, old_phone, new_phone = args[0], PhoneField(args[1]), PhoneField(args[2])
        record = ADDRESS_BOOK.get_record(name)
        if record:
            return record.update_phone(old_phone, new_phone)
        return f'Contact with name "{name}" doesn\'t exist.'

class RemovePhoneCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Remove phone"
        self._description = '''
            syntax: remove phone {name} {phone_number}
            description: removing contact from contacts list
            example: remove ivan +380999999999
        '''
    
    @input_error
    def execute(self, *args) -> str:
        name, phone = args[0], PhoneField(args[1])
        record = ADDRESS_BOOK.get_record(name)
        if record:
            return record.remove_phone(phone)
        return f'Contact with "{name}" doesn\'t exist.'

class ShowContactCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Show contact"
        self._description = '''
            syntax: show contact {name}
            description: finding all info by contact name
            example: show contact ivan
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        name = args[0]
        return ADDRESS_BOOK.get_record(name) or f'Contact with name "{name}" doesn\'t exist.'
    
class AddBirthdayCommand(CommandABC):
    def __init__(self) -> None:
        self._name = 'Add birthday'
        self._description = '''
            syntax: add birthday {name} {birthday}
            description: add birthday to contact name 
            example: add birthday Ivan 01-01-1970
        '''    
    
    @input_error
    def execute(self, *args) -> str | None:
        birthday = args[1]
        name = args[0]
        obj = BirthdayField(birthday)
        if not ADDRESS_BOOK.get_record(name):
            return name + " not in book" 
        name = ADDRESS_BOOK.get_record(name)
        name.add_birthday(obj)
        ADDRESS_BOOK.add_record(name)
        return name.name.value + ' add birthday ' + birthday

class AddMail(CommandABC):
    def __init__(self) -> None:
        self._name = "Add mail"
        self._description = '''
            syntax: add mail {name} {email}
            description: add mail to contact name
            example: add mail Ivan ivan@mail.com
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        mail = args[1]
        name = args[0]
        mail = mail.lower()
        obj = MailField(mail)
        if not ADDRESS_BOOK.get_record(name):
            return name + " not in book"
        name = ADDRESS_BOOK.get_record(name)
        name.add_mail(obj)
        ADDRESS_BOOK.add_record(name)
        return name.name.value + ' add mail ' + mail

class AddAddress(CommandABC):
    def __init__(self) -> None:
        self._name = "Add address"
        self._description = '''
            syntax: add address {name} {address}
            description: adding address to contact name 
            example: add address ivan Kyiv
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        adress = args[1]
        name = args[0]
        obj = AdressField(adress)
        if not ADDRESS_BOOK.get_record(name):
            return name + " not in book "
        name = ADDRESS_BOOK.get_record(name)
        name.add_adress(obj)
        ADDRESS_BOOK.add_record(name)
        return name.name.value + ' add adress  ' + adress

class DaysToBirthday(CommandABC):
    def __init__(self) -> None:
        self._name = "Days to birtday"
        self._description = '''
            syntax: days to birthday {name}
            description: show count days to name birthday
            example: days to birthday Ivan
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        name = args[0]
        if name in ADDRESS_BOOK:
            days = ADDRESS_BOOK[name].days_to_birthday()
            return f'{name} birthday in {days} days' if days else f'You haven\'t record about {name} birthday'
        return f'Contact "{name}" does\'t exists in address book'

class BirthdaysRange(CommandABC):
    def __init__(self) -> None:
        self._name = "Birthdays range"
        self._description = '''
            syntax: birthdays range {X - number of days}
            description: show all contacts during next X days
            example: birthdays range 10
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        current_list = []
        users_range = timedelta(days=int(args[0]))
        today_date = datetime.now().date()
        max_date = today_date + users_range
        birthdays_list = ADDRESS_BOOK.get_birthdays()
        for i in birthdays_list:
            date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date()
            if (date_formated.month < today_date.month) or (date_formated.month == today_date.month and date_formated.day <= today_date.day):
                date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date().replace(year=today_date.year + 1)
            else:
                date_formated = datetime.strptime(i.birthday.value, '%d-%m-%Y').date().replace(year=today_date.year)
            if today_date < date_formated <= max_date:
                current_list.append(i)
        if current_list:
            print(f'In the range from {today_date} to {max_date} birthdays has next user(s):')
            for user in current_list:
                print(user)
        else:
            print(f'There is no birthdays in next {args[0]} days.')
        return 'Please, enter next command.'
    
class ShowAllContacts(CommandABC):
    def __init__(self) -> None:
        self._name = "Show all contacts"
        self._description = '''
            syntax: show all
            description: showing list of contacts
            example: show all
        '''
    
    
    @input_error
    def execute(self, *args) -> str | None:
        if len(args):
            raise IndexError
        if len(ADDRESS_BOOK):
            output = "---CONTACTS--- (Tap enter for next page or print stop for exit)\n"
            for page in ADDRESS_BOOK:
                total_pages, current_page, data = page[0], page[1], page[2]
                page_output = f"Page {current_page} of {total_pages}:\n"
                for record in data:
                    page_output += f"{record}\n"
                print(output)
                print(page_output)
                if current_page < total_pages:
                    inpt = input("pages >>> ")
                    if inpt == 'exit':
                        break
            return "Address book is closed"
        else:
            output += "Contacts are empty"
            return output

class SortFilesCommand(CommandABC):
    def __init__(self) -> None:
        self._name = 'Sort files'
        self._description = '''
            syntax: sort files {path-to-sorted folder}
            description: sort files in your folder
            example: sort files d:/some-folder
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        default_path = args[0]
        organizer = SortFile(default_path)
        organizer.create_directories(organizer.DEFAULT_PATH)
        organizer.arrange(organizer.DEFAULT_PATH)
        return f"folder {default_path} sorted."

class AddNoteCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Add not"
        self._description = '''
            syntax: add note {note} {#hashtag}
            description: This function creates a new note
            example: add note Tim birthday #holiday
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        note_content = ' '.join(str(arg) for arg in args)
        new_note = Note(note_content)
        NOTEBOOK.add(new_note)
        return 'Note added'
    
class UpdateNoteCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Update note"
        self._description = '''
            syntax: update note
            description: This function modifies a note by it`s ID
            example: change note
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        NOTEBOOK.modify()
        return "Note updated successfully."
    
class DeleteNoteCommand(CommandABC):
    def __init__(self) -> None:
        self._name = 'Delete note'
        self._description = '''
            syntax: delete note {ID}
            description: This function deletes a note by it`s ID
            example: delete note 5
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        note_id = int(args[0])
        if note_id in NOTEBOOK.data:
            NOTEBOOK.delete(note_id)
            return 'Note deleted'
        else:
            return 'Note not found'
        
class SearchNoteCommand(CommandABC):
    def __init__(self) -> None:
        self._name = "Search Note"
        self._description = '''
            syntax: searh note {text or tag}
            description: This function searches for notes by part or all word
            example: search birthday
        '''
    
    @input_error
    def execute(self, *args) -> str | None:
        search_query = ' '.join(str(arg) for arg in args)
        if search_query:
            results = NOTEBOOK.search(search_query)
            return results if results else 'No matching notes found.'
        else:
            return 'No search query provided.'