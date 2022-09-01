
from typing import Callable, Dict
from datetime import datetime
from collections import UserDict
from operator import add
from pprint import pprint
import pickle

def _create_date(*, year, month, day):
    return datetime(year=year, month=month, day=day).date()


def _now():
    return datetime.today()  

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Birthday(Field):
    
    @property
    def value(self) -> datetime.date:
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.strptime(value, "%d-%m-%Y")

    def __repr__(self):
        return datetime.strftime(self._value, "%d-%m-%Y")


class Name(Field):
    
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Overriden {value}"


class Phone(Field):
    
    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        self._value = f"Overriden {value}"

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phones: list[Phone] = [phone] if phone is not None else []
        self.birthday = birthday

    def __repr__(self):
        return f"{self.name}, {' '.join(phone.value for phone in self.phones)}, {self.birthday}"

    def add_birthday(self,name: Name, birthday: Birthday = None):
        name = Name(name)
        birthday = birthday[0:2] + "_" + birthday[3:5] + "_" + birthday[6:]
        birthday = Birthday(birthday)
        addres_book.data.get(name.value, []).birthday = birthday
        return "The birthday is recorded"


    def days_to_birthday(self, birthday: Birthday):
        now = _now()
        if self.birthday is not None:
            birthday: datetime.date = self.birthday.value.date()
            next_birthday = _create_date(
                year=now.year, month=birthday.month, day=birthday.day
            )
            if birthday < next_birthday:
                next_birthday = _create_date(
                    year=next_birthday.year + 1,
                    month=next_birthday.month,
                    day=next_birthday.day,
                )
            return (next_birthday - birthday).days
        return None

    def add_phone(self, name: Name, phone: Phone = None):
        name = Name(name)
        phone = Phone(phone)
        addres_book.data.get(name.value, []).phones.append(phone)
        return "The phone is recorded"

    def change_phone(self, old_number: Phone, new_number: Phone):
        try:
            self.phones.remove(old_number)
            self.phones.append(new_number)
        except ValueError:
            return f"{old_number} does not exists"


    def delete_phone(self, phone: Phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f"{phone} does not exists"
    

class AddressBook(UserDict, Record):
    __items_per_page = 15
    filename = 'AddresBook.bin'
    
    
    def items_per_page(self, value):
        self.__items_per_page = value
        
    items_per_page = property(fget=None, fset=items_per_page)

    def add_contact(self, name: Name, phone: Phone = None):
        name = Name(name)
        phone = Phone(phone)
        contact = Record(name=name, phone=phone)
        self.data[name.value] = contact

    def add_record(self, record: "Record"):
        self.data[record.name.value] = record

    def find_by_name(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def find_by_phone(self, phone: str):
        for record in self.data.values():
            if phone in [number.value for number in record.phones]:
                return record
        return None
    

    def write_contacts_to_AddressBook(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.data, file)

    def read_contacts_from_AddresBook(self):
        with open(self.filename, "rb") as file:
            contact = pickle.load(file)
            return contact
            


    def __iter__(self):
        self.page = 0
        return self

    def __next__(self):
        records = list(self.data.items())
        start_index = self.page * self.__items_per_page
        end_index = (self.page + 1) * self.__items_per_page
        self.page += 1
        if len(records) > end_index:
            to_return = records[start_index:end_index]
        else:
            if len(records) > start_index:
                to_return = records[start_index : len(records)]
            else:
                to_return = records[:-1]
        self.page += 1
        return [{record[1]: record[0]} for record in to_return]
    
    def show_all_h(self, *args):
        """Returns all records"""
        all_response = "Contacts book\n"
        contacts = "\n".join(
            f"{username} contacts is {number}" for (username, number) in addres_book.data.items()
            )
        formated_contacts = "Number does not exists? yet!" if contacts == '' else contacts
        return all_response + formated_contacts


addres_book = AddressBook()




from typing import Callable, Dict



def input_error(func):
    def wraper(user_input):
        try:
            return func(user_input)
        except ValueError as e:
            return str(e)       
    return wraper


@input_error
def hello_handler(user_input: str):
    if user_input.strip() == 'hello':
        return 'How can I help you'
    raise ValueError('Bad input!')


@input_error
def add_contact_handler(user_input: str):
    args = user_input.lstrip('add contact')
    try:
        name, phone = args.split(' ')
    except ValueError:
        raise ValueError('Bad input! Give me name and phone please')
    if name == '' or phone == '':
        raise ValueError('Bad input! Give me name and phone please')
    if addres_book.find_by_name(name) == None:
        addres_book.add_contact(name, phone)
        return 'Number was added!'
    raise ValueError(f'{name} alredy in contact book!')

@input_error
def add_phone_handler(user_input: str):
    args = user_input.lstrip('add phone ')
    try:
        name, phone = args.split(' ')
    except ValueError:
        raise ValueError('Bad input! Give me name and phone please')
    if name == '' or phone == '':
        raise ValueError('Bad input! Give me name and phone please')
    if addres_book.find_by_name(name):
        addres_book.add_phone(name, phone)
        return 'Phone was added!'
    raise ValueError(f'{name} alredy in contact book!')


@input_error
def change_phone_handler(user_input: str):
    try:
        args = user_input.lstrip('change phone ')
        phone_olld, phone_new = args.split(' ')
    except ValueError:
        raise ValueError('Bad input! Give me phone_olld and phone_new please')
    if addres_book.find_by_phone == None:
        raise ValueError(f'{phone_olld} does not exists!')
    else:
        addres_book.change_phone(phone_olld, phone_new)
        return 'Number was changed!'


@input_error
def delate_phone_handler(user_input: str):
    phone = user_input.lstrip('delate phone ')
    if addres_book.find_by_phone == None:
        raise ValueError("Bad input! Enter user name")
    else:
        return addres_book.delete_phone(phone)


@input_error
def show_all_handler(user_input: str):
    if user_input.strip() == 'show all':
        contacts = addres_book.show_all_h
        return contacts
    raise ValueError('Bad input')

@input_error
def write_handler(user_input: str):
    if user_input.strip() == 'save':
        addres_book.write_contacts_to_AddressBook()
        return 'Contacts is save'
    raise ValueError('Bad input')

@input_error
def read_contacts_handler(user_input: str):
    if user_input.strip() == 'load':
        addres_book.read_contacts_from_AddresBook()
        return 'Contacts is save'
    raise ValueError('Bad input')

def exit_handler(user_input: str):
    for item in ['good bye', 'close', 'exit']:
        if user_input.strip() == item:
            raise SystemExit('Good bye!')
    

COMMAND_HANDLERS: Dict[str, Callable] = {
    'hello': hello_handler,
    'add contact': add_contact_handler,
    'add phone': add_phone_handler,
    "change phone": change_phone_handler,
    "delate phone": delate_phone_handler,
    'show all': show_all_handler,
    'save': write_handler,
    "load": read_contacts_handler,
    'good bye': exit_handler,
    'close': exit_handler,
    'exit': exit_handler,
}


@input_error
def parse_user_input(user_input: str) -> set[str, str]:
    for command in COMMAND_HANDLERS.keys():  
        if user_input.startswith(command):
            parser = COMMAND_HANDLERS.get(command)
            return parser(user_input)
        else:
            continue
    raise ValueError('Unknown command')



def main():
        while True:
            user_input = input('Enter the command: ').lower()
            try:
                resalt = parse_user_input(user_input)
                print(resalt)
            except SystemExit as e:
                 print(e)
                 break


if __name__ == '__main__':
    main()



