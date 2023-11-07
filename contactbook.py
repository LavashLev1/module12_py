import pickle
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

class Phone(Field):
    def validate(self, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError("Неправильний формат номеру телефона")

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неправильний формат дати (РРРР-ММ-ДД)")

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Field(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_remaining = (next_birthday - today).days
            return days_remaining
        return None

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            self.contacts = []

    def find_contacts(self, search_str):
        matching_contacts = []
        for contact in self.contacts:
            if (
                search_str in contact.name.value
                or search_str in contact.phone.value
                or (contact.birthday and search_str in contact.birthday.value)
            ):
                matching_contacts.append(contact)
        return matching_contacts

    def iterator(self, chunk_size):
        for i in range(0, len(self.contacts), chunk_size):
            yield self.contacts[i:i + chunk_size]

if __name__ == "__main__":
    address_book = AddressBook()
    address_book.load_from_file("address_book.dat")

    while True:
        print("1. Додати контакт")
        print("2. Знайти контакти")
        print("3. Вивести всі контакти")
        print("4. Завершити роботу")

        choice = input("Оберіть опцію: ")

        if choice == "1":
            name = input("Ім'я: ")
            phone = input("Номер телефону: ")
            birthday = input("Дата народження (РРРР-ММ-ДД): ")
            contact = Record(name, phone, birthday)
            address_book.add_contact(contact)
            address_book.save_to_file("address_book.dat")
        elif choice == "2":
            search_str = input("Введіть рядок для пошуку: ")
            matching_contacts = address_book.find_contacts(search_str)
            if matching_contacts:
                print("Знайдені контакти:")
                for contact in matching_contacts:
                    print(f"Ім'я: {contact.name.value}, Телефон: {contact.phone.value}")
            else:
                print("Контакти не знайдені.")
        elif choice == "3":
            for contact_chunk in address_book.iterator(5):
                for contact in contact_chunk:
                    print(f"Ім'я: {contact.name.value}, Телефон: {contact.phone.value}")
        elif choice == "4":
            break
