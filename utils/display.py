import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_menu():
    print("\n" + "-" * 20)
    print("✨   My Journal  ✨")
    print("-" * 20)
    
    print("\n1. Write a journal entry")
    print("2. View all entries")
    print("3. Search entries")
    print("4. Edit an entry [Not available]")
    print("5. Delete an entry [Not available]")
    print("6. View statistic [Not available]")
    print("7. Exit")
    print()