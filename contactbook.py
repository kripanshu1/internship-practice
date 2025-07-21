import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact():
    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()
    contacts = load_contacts()
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print("Contact added successfully.")

def view_contacts():
    contacts = load_contacts()
    if not contacts:
        print("No contacts found.")
        return
    print("\nContacts:")
    for i, contact in enumerate(contacts, start=1):
        print(f"{i}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")
    print()

def search_contacts():
    query = input("Enter name or phone or email to search: ").strip().lower()
    contacts = load_contacts()
    results = [c for c in contacts if query in c['name'].lower() or query in c['phone'] or query in c['email'].lower()]
    if not results:
        print("No matching contacts found.")
        return
    print("\nSearch Results:")
    for i, contact in enumerate(results, start=1):
        print(f"{i}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")
    print()

def update_contact():
    contacts = load_contacts()
    if not contacts:
        print("No contacts to update.")
        return
    view_contacts()
    try:
        index = int(input("Enter the number of the contact to update: "))
        if index < 1 or index > len(contacts):
            print("Invalid contact number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    contact = contacts[index - 1]
    print("Leave blank to keep current value.")
    name = input(f"Enter new name [{contact['name']}]: ").strip()
    phone = input(f"Enter new phone number [{contact['phone']}]: ").strip()
    email = input(f"Enter new email [{contact['email']}]: ").strip()
    if name:
        contact['name'] = name
    if phone:
        contact['phone'] = phone
    if email:
        contact['email'] = email
    save_contacts(contacts)
    print("Contact updated successfully.")

def delete_contact():
    contacts = load_contacts()
    if not contacts:
        print("No contacts to delete.")
        return
    view_contacts()
    try:
        index = int(input("Enter the number of the contact to delete: "))
        if index < 1 or index > len(contacts):
            print("Invalid contact number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    contact = contacts.pop(index - 1)
    save_contacts(contacts)
    print(f"Contact '{contact['name']}' deleted successfully.")

def main():
    while True:
        print("Contact Book Application")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contacts")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            add_contact()
        elif choice == '2':
            view_contacts()
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Exiting Contact Book. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        print()

if __name__ == "__main__":
    main()
