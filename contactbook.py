import pickle

class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def search_contact(self, keyword):
        results = []
        for contact in self.contacts:
            if keyword in contact.name or keyword in contact.phone:
                results.append(contact)
        return results

    def save_to_disk(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_disk(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            # Handle the case when the file doesn't exist yet
            self.contacts = []

# Create an AddressBook instance
address_book = AddressBook()

# Load contacts from disk (if the file exists)
address_book.load_from_disk('address_book.pkl')

while True:
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Save and Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter contact name: ")
        phone = input("Enter contact phone: ")
        contact = Contact(name, phone)
        address_book.add_contact(contact)

    elif choice == '2':
        keyword = input("Enter search keyword: ")
        results = address_book.search_contact(keyword)
        if results:
            for result in results:
                print(f"Name: {result.name}, Phone: {result.phone}")
        else:
            print("No matching contacts found.")

    elif choice == '3':
        address_book.save_to_disk('address_book.pkl')
        break
