from utils.display import clear_screen
from config import MOOD_EMOJIS

def view_entries(db):
    clear_screen()

    entries = db.get_all_entries()
    
    if not entries:
        print("\n📪 No entries found. Start writing your journal!")
        return

    print("\n" + ("=" * 60))
    print(f"📖  My Journal | {len(entries)} entries   🌟")
    print("=" *60)

    for entry in entries:
        display_entry(entry)

    input("\nPress ENTER to return to home menu...")
    clear_screen()

def display_entry(entry):
    print(f"\n📝 Entry #{entry['id']}")

    date_str = entry['entry_date'].strftime("%b/%d/%Y • %I:%M %p")
    print(f"{date_str}")

    if entry['mood']:
        mood_emoji = MOOD_EMOJIS.get(entry['mood'].lower(),'')
        print(f"Mood : {entry['mood']} {mood_emoji}")
        
    if entry['tags']:
        print(f"Tags: {entry['tags']}")

    print(f"\n{entry['entry_text']}")

    if entry.get('word_count'):
        print(f"\n • {entry['word_count']} words")

    print("\n" + "-" * 60)

    # input("\n>>Press ENTER to return to the menu >")
    # clear_screen()