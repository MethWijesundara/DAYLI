# 1. imports
from datetime import datetime
import os



# 2. constants
FILENAME = "journal.txt"

# 3. Mood emoji dictionary (defined once globally)


# 4. Database configuration
db = None

# 5. utility functions (clear_screen , display_menu)
# ✅
def clear_screen():
    os.system('cls' if os.name=='nt' else 'clear')



# 6. Database class

class JournalDatabase:
    # Handle all database operation for the journal
    def __init__(self):
        

    def connect(self):
        


    def create_table_if_not_exists(self):
        # create the "entries" table if it doesn't exists
        
        
    def add_entry(self, entry_text, mood = None, tags = None):
        # Add a new journal entry
        

    def get_all_entries(self,limit=50):
        # This function gets all entries, newest ones first
        

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
        
        

# 5. core functions



# ✅



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







