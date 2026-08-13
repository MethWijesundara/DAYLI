from database.journal_database import JournalDatabase
from features.write_entry import write_entry
from features.view_entries import view_entries
# from features.search_entries import search_entries
from utils.display import display_menu
from utils.display import clear_screen


def main():
    clear_screen()
    db = JournalDatabase

    while True:
        display_menu()

        choice = input("Enter choice number (1-7): ").strip()

        if choice == "1":
            write_entry(db)

        elif choice == "2":
            view_entries(db)

        elif choice == "3":
            search_entries(db)

        elif choice == "7":
            print("\n 🙋🏻‍♂️Goodbye!")
            break

if __name__ == "__main__":
    main()
