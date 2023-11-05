import pickle

class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite

class Contacts:
    def __init__(self):
        self.contacts = []

    def add_contact(self, person: Person):
        self.contacts.append(person)

    def save_to_file(self, filename: str):
        with open(filename, "wb") as file:
            pickle.dump(self.contacts, file)

    @classmethod
    def read_from_file(cls, filename: str):
        contacts = []
        try:
            with open(filename, "rb") as file:
                contacts = pickle.load(file)
        except FileNotFoundError:
            pass
        instance = cls()
        instance.contacts = contacts
        return instance

    def search_contacts(self, query: str):
        results = []
        for contact in self.contacts:
            if (
                query in contact.name
                or query in contact.phone
            ):
                results.append(contact)
        return results

if __name__ == "__main__":
    filename = "contacts.pkl"
    contacts = Contacts.read_from_file(filename)

    while True:
        print("1. Додати контакт")
        print("2. Пошук контакту")
        print("3. Вийти")
        choice = input("Виберіть опцію: ")

        if choice == "1":
            name = input("Ім'я: ")
            email = input("Електронна пошта: ")
            phone = input("Номер телефону: ")
            favorite = input("Обраний контакт (True/False): ").lower() == "true"
            contact = Person(name, email, phone, favorite)
            contacts.add_contact(contact)
            contacts.save_to_file(filename)
            print("Контакт додано.")

        elif choice == "2":
            query = input("Введіть рядок для пошуку: ")
            results = contacts.search_contacts(query)
            if results:
                for result in results:
                    print(f"Ім'я: {result.name}")
                    print(f"Електронна пошта: {result.email}")
                    print(f"Номер телефону: {result.phone}")
                    print(f"Обраний контакт: {result.favorite}")
                    print()
            else:
                print("Збігів не знайдено.")

        elif choice == "3":
            break
