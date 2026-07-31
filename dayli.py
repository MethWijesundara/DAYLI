from datetime import datetime
import os
# connecting database
import mysql.connector
from mysql.connector import Error

FILENAME = "journal.txt"

# for database
db = None

# database configuration
DB_CONFIG = {
    'host' : 'localhost',
    'database' : 'journal_db',
    'user' : 'root', # default XAMPP user
    'password' : '' # default XAMPP password (empty)
}

class JournalDatabase:
    # Handle all database operation for the journal
    def __init__(self):
        # initialize database connection
        self.connection = None
        self.connect()
        self.create_table_if_not_exists()

    def connect(self):
        # establish database connection
        # try : includes the code that may break
        print("\n>>🛜  Connecting to MySQL database...")
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("\n>> ✅ Connected to MySQL database!")

        # except : contains the code which manages the crisis 
        except Error as e:
            print(f"\n>>❌ Error connecting to MySQL : {e}")
            print("\nPlease make sure:")
            print("(1) XAMPP is running")
            print("(2) MySQL services is started")
            print("(3) Database 'journal_db exists'")
            input("\n> Press ENTER to exit..")
            exit()
    
    def create_table_if_not_exists(self):
        # create the "entries" table if it doesn't exists
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    entry_text TEXT NOT NULL,
                    entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    mood VARCHAR(20) NULL,
                    tags VARCHAR(255) NULL,
                    word_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP        
                )           
            """)
            self.connection.commit()
            cursor.close()

        except Error as e : 
            print(f"❌ Error creating table : {e}")
        
    def add_entry(self, entry_text, mood = None, tags = None):
        # Add a new journal entry
        try:
            cursor = self.connection.cursor()

            # calculate word count
            word_count = len(entry_text.split())

            query = """
                INSERT INTO entries(entry_text, mood, tags, word_count)
                VALUES (%s, %s, %s, %s)
            """
            values = (entry_text, mood, tags, word_count)

            cursor.execute(query,values)
            self.connection.commit()

            entry_id = cursor.lastrowid
            cursor.close()
            return entry_id
        
        except Error as e:
            print(f"❌ Error adding entry: {e}")
            return None

    def get_all_entries(self,limit=50):
        # This function gets all entries, newest ones first
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("""
            SELECT id,entry_text,entry_date,mood,tags,word_count
            FROM entries
            ORDER BY entry_date DESC
            LIMIT %s

            """, (limit,))
            entries = cursor.fetchall()
            cursor.close()
            return entries
        except Error as e:
            print(f"🔴 Error fetching entries : {e}")
        
# 1. search :main menu
def display_menu():
    # clear_screen()
    print("\n" + "=" * 20)
    print("✨ My Journal ✨")
    print("=" * 20)
    print("\n1 - Write a journal entry")
    print("2 - View all entries")
    print("3 - Search entries")
    print("4 - Edit an entry")
    print("5 - Delete an entry")
    print("6 - View statistic")
    print("7 - Exit")
    print()

# WRITE_ENTRY
def write_entry(db): # <-- Pass db as parameter!
    """Write a new journal entry with timestamp"""

    print("\n> ✍️   Write your journal entry")
    entry_text = input().strip()

    if (not entry_text):
        print(">> 🔴  Entry cannot be empty!")
        return

    # get mood and tags (not written)
    # mood
    print("\n How are you feeling? (happy/sad/excited/tired/neutral)")
    # mood = input("\n> Enter your mood [Calm, Happy, Sad, Angry, ...]\n")
    mood = input("> ").strip().lower()

    # if mood not in ['happy' , 'sad' , 'excited' , 'tired' , 'neutral']:
    #     mood = None # Invalid mood, set to None

    # tags
    print("\n Add tags (comma-seperate, e.g., coding,gym,travel)")
    # tags = input("\n> Enter tags [#anxious, #peaceful, #grieving, ...]\n")
    tags_input = input("> ").strip()
    tags = tags_input if tags_input else None # check/learn this line

    # call the method on the db instance
    # save to DATABASE only
    entry_id = db.add_entry(entry_text, mood, tags)

    if entry_id:
        print(f"\n> 🟢  Entry saved successfully! (ID: {entry_id})")
        if mood:
            print(f"    Mood: {mood}")
        if tags:
            print(f"    Tags: {tags}")
    else:
        print("\n🔴  Failed to save entry to database.")

    # ---------------------
    

# (3)
def view_entries(db):
    # Display all entries with formatting
    clear_screen()

    entries = db.get_all_entries()
    
    if not entries:
        print("\n>> 📬  No entries found. Start writing your journal!")
        return

    print(f"\nYour Entries : {len(entries)}")

    for entry in entries:
        print(f"\nEntry {entry['id']}")
        print(f"{entry ['entry_date'].strftime('%Y/%m/%d %I:%M %p')}")

        if entry['mood']:
            mood_emoji = {
                'happy' : '😊',
                'sad' : '😢',
                'excited' : '🤩',
                'tired' : '😴',
                'neutral' : '😐'
            }.get(entry['mood'],'')

            print(f"Mood: {entry['mood']} {mood_emoji}")

        if entry['tags']:
            print(f"Tags : {entry['tags']}")

        print(f"Words : {entry['word_count']}")
        print(entry['entry_text'])

    input("\nPress ENTER to return to the menu")
    clear_screen()
    # works!


# 4. searching for entries (choice 3)
def search_entries():
    """ Search for entries containing a keyword"""

    if not os.path.exists(FILENAME):
        print("\nNo entries to search.")
        return
    keyword = input("\nEnter search term: ").strip().lower()

    if not keyword:
        print("Search term cannot be empty!")
        return
    
    try:
        # with open -- ?
        with open(FILENAME, "r") as file:
            content = file.read()

            # Split entries by the seperator
            entries = content.split("--------------------------------")

            found_entries = []
            # for loop
            for entry in entries:
                # if condition
                if entry.strip() and keyword in entry.lower():
                    found_entries.append(entry.strip())

            # if condition (print + for loop)
            if found_entries:
                # do if true
                print(f"\nFound {len(found_entries)} entry(ies) containing '{keyword}' : ")
                print("="*20)

                # for loop
                for i,entry in enumerate(found_entries,1):
                    print(f"\n--- Entry{i} ---")
                    print(entry)
                    print("-"*20)
            # else (do if false) 
            else:
                print(f"\nNo entries found containing '{keyword}'")
                
    # except runs when something breaks in try -- it's like what to do(except) after crisis(try)
    except Exception as e:
        print(f"\n❌ Error searching entries: {e}")


# (5) main method
def main():
    # (1)
    db = JournalDatabase()

    while(True):
        display_menu()
        choice = int(input("> Enter choice number(1-7): "))

        # writing if conditions to execute certain operations
        # for now, idk what they are executing
        if (choice==1):
            write_entry(db)
        elif (choice==2):
            view_entries(db)
        elif (choice == 3):
            search_entries(db)
        elif (choice ==4):
            edit_entry(db)
        elif (choice == 5):
            delete_entry(db)
        elif(choice == 6):
            show_statistics(db)
        elif (choice == 7):
            print("\n>> 👋 Goodbye! ")
            break



# (6) clear screen
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

# (7) I think you use this so that main function runs first
# entry point of the program
if __name__ == "__main__":
    main()







