# 1. imports
from datetime import datetime
import os

import mysql.connector
from mysql.connector import Error

# 2. constants
FILENAME = "journal.txt"

# 3. Mood emoji dictionary (defined once globally)
MOOD_EMOJIS = {
    'happy': '😊',
    'sad': '😢',
    'excited': '🤩',
    'tired': '😴',
    'neutral': '😐',
    'angry': '😡',
    'calm': '😌',
    'grateful': '🙏',
    'anxious': '😰',
    'peaceful': '🕊️',
    'energetic': '⚡',
    'stressed': '😫',
    'inspired': '💡',
    'melancholic': '🌧️',
    'lonely': '🌙',
    'hopeful': '🌟',
    'content': '☺️'
}

# 4. Database configuration
db = None
DB_CONFIG = {
    'host' : 'localhost',
    'database' : 'journal_db',
    'user' : 'root', # default XAMPP user
    'password' : '' # default XAMPP password (empty)
}

# 5. utility functions (clear_screen , display_menu)
# ✅
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')

def display_menu():
    # clear_screen()
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

# 6. Database class

class JournalDatabase:
    # Handle all database operation for the journal
    def __init__(self):
        # initialize database connection
        self.connection = None
        self.connect()
        self.create_table_if_not_exists()

    def connect(self):
        while True:
            clear_screen()
            print("\n🛜  Connecting to MySQL database...")
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                if self.connection.is_connected():
                    print("\n>>✅ Connected to MySQL database!")
                    break

            except Error as e:
                print(f"\n>> ❌  Error connecting to MySQL database -> {e}")
                print("\nPlease make sure ;")
                print("• XAMPP is running")
                print("• MySQL service is started")
                print("• Database 'journal_db' exists")

                choice = input("\n>>⚠️  Try again? (y/n): ").lower().strip()
                if choice == 'n':
                    print("📖 Exiting.. See you 👋")
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

    # def get_entry_by_id(self,entry_id):
    #     try:
    #         cursor = self.connectior.cursor(dictionary=True)
    #         cursor.execute("""
    #             SELECT id, entry_text, entry_date, mood, tags, word_count
    #             FROM entries
    #             WHERE id = %s    
    #     """)
    #     except Error as e:


    def search_entries(self, keyword):
        # search entries by keyword in content, mood, or tags (MySQL version)
        try:
            cursor = self.connection.cursor(dictionary = True)

            sql = """
                SELECT id, entry_text, entry_date, mood, tags, word_count
                FROM entries
                WHERE entry_text LIKE %s
                    OR mood LIKE %s
                    OR tags LIKE %s
                ORDER BY entry_date ASC"""

            params = (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')

            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            return results 
        except Error as e:
            print(f"🔴  Error search entries: {e}")
            return []
        

        keyword = input("\n")
        

# 5. core functions
def write_entry(db):

    print("\n> ✍️   Write your journal entry")
    entry_text = input().strip()

    if (not entry_text):
        print(">> 🔴  Entry cannot be empty!")
        return

    print("\n How are you feeling? (happy/sad/excited/tired/neutral)")
    mood = input("> ").strip().lower()

    print("\n Add tags (comma-seperate, e.g., coding,gym,travel)")

    tags_input = input("> ").strip()
    tags = tags_input if tags_input else None

    entry_id = db.add_entry(entry_text, mood, tags)

    if entry_id:
        print(f"\n> 🟢  Entry saved successfully! (ID: {entry_id})")
        if mood:
            print(f"    Mood: {mood}")
        if tags:
            print(f"    Tags: {tags}")
    else:
        print("\n🔴  Failed to save entry to database.")


# ✅
def view_entries(db):
    clear_screen()
    entries = db.get_all_entries()
    
    if not entries:
        print("\n>> 📬  No entries found. Start writing your journal!")
        return

    # Header
    print("\n" + ("•" * 50))
    print(f"\n📖    My Journal > ({len(entries)}) entries   🌟")
    print("•" *50)

    # body
    for entry in entries:

        # Entry ID and date
        print(f"\n📝 Entry #{entry['id']}")
        date_str = entry['entry_date'].strftime("%Y/%m/%d %I:%M %p")
        print(f"📅 {date_str}")

        # Mood with emoji
        if entry['mood']:
            mood_emoji = MOOD_EMOJIS.get(entry['mood'].lower(),'')
            print(f"🎭 Mood : {entry['mood']} {mood_emoji}")
        
        if entry['tags']:
            print(f"🏷️ Tags: {entry['tags']}")

        # wourd count
        if entry.get('word_count'):
            print(f"📊 Words: {entry['word_count']}")

        # Entry content
        print(f"\n{entry['entry_text']}")
        print("-" *40)

    input("\n>>Press ENTER to return to the menu >")
    clear_screen()


def search_entries(db):
    clear_screen()

    keyword = input("\n🔍 Enter search term: ").strip().lower()

    if not keyword:
        print(">>⚠️   Search term cannot be empty!")
        return

    try:
        results = db.search_entries(keyword)

        if(results):
            print(f"\n📖 Found {len(results)} entry(ies) containing '{keyword}'")
            print("-"*40)

            for i,entry in enumerate(results,1):
                print(f"\n--- Entry {i} ---")
                print(f"📝 {entry['entry_text']}")
                
                if entry.get('mood'):
                    print(f"🎭 Mood: {entry['mood']}")

                if entry.get('tags'):
                    print(f"🏷️ Tags: {entry['tags']}")

                print(f"📅 {entry['entry_date']}")
                print("-"*30)

            input("\n>> Press ENTER to return to menu")
            clear_screen()
        else:
            print(f"🟡 No entries found containing '{keyword}'")

    except Exception as e:
        print(f"⚠️   Error : {e}")

def edit_entry(db):
    clear_screen()

    try:
        entries = db.get_all_entries(limit=20)
        if not entries:
            print("\n>> 📫 No entries found to edit!")
            input("\n>> Press ENTER to return to home")
            clear_screen()
            return

        print("\n" + "="*50)
        print("📝 Your Recent Entries:")
        print("="*50)

        for entry in entries:
            print(f"\n ID: {entry['id']}")
            print(f"🗓️  {entry['entry_date'].strftime('%Y %m %d %I %M %p')}")

            preview = entry['entry_text']
            if len(preview) >100:
                preview = preview[:100] + "..."
            print(f"📝 {preview}")
            print("-")*30

        entry_id = input("\n>> ✏️ Enter the ID of the entry you want to edit >").strip()

        if not entry_id.isdigit():
            print("⚠️ Invalid ID! Please enter a valid ID.")
            input("\n>> Press ENTER to return to menu.")
            clear_screen()
            return

        # getting entry from database
        entry = db.get_entry_by_id(int(entry_id))

        if not entry:
            print(f"❌ No entry found with ID: {entry_id}")
            input("\n Press ENTER to return to menu.")
            clear_screen()
            return

        # showing current entry
        print("\n" + "-"*20)
        print(f"")


    except Exception as e:
        print(f"\n🔴 Error editing entry: {e}")
        input("\nPress ENTER to return to menu")
        clear_screen()

def main():
    db = JournalDatabase()

    while(True):
        display_menu()
        choice = int(input("> Enter choice number(1-7): "))

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
            clear_screen()
            print("\n>> 👋 Goodbye! ")
            break

if __name__ == "__main__":
    main()







