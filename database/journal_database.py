import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG

class JournalDatabase:

    # 1. Constructor 
    def __init__(self):
        self.connection = None
        self.connect()
        self.create_table_if_not_exists()


    # 2. Connecting to the database
    def connect(self):
        while True:
            # clear_screen()
            print("\n🛜  Connecting to MySQL database...")
            try:
                self.connection = mysql.connector.connect(**DB_CONFIG)
                if self.connection.is_connected():
                    print("\n✅ Connected to MySQL database!")
                    break

            except Error as e:
                print(f"\n❌  Error connecting to MySQL database -> {e}")
                print("\nPlease make sure ;")
                print("• XAMPP is running")
                print("• MySQL service is started")
                print("• Database 'journal_db' exists")

                choice = input("\n⚠️  Try again? (y/n): ").lower().strip()
                if choice == 'n':
                    print("📖 Exiting.. See you 👋")
                    exit()

    # 3. Creating the table if it doesn't exist on the database (CREATE)
    def create_table_if_not_exists(self):
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


    # 4. Adding an entry to the database (INSERT INTO)
    def add_entry(self, entry_text, mood=None, tags=None):
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

    # 5. Retrieving entries from the database. (SELECT)
    def get_all_entries(self, limit=50):
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
            return []

    # 6. Searching through an entry for a specific keyword.
    def search_entries(self, keyword):
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
        

        # keyword = input("\n")