def write_entry(db):

    print("\n✍🏻 Write your journal entry")

    entry_text = input().strip()

    if not entry_text:
        print("🔴  Entry cannot be empty!")
        return

    print("\n How are you feeling?")
    mood = input().strip().lower()

    print("\nAdd tags (comma-seperated)")
    tags_input = input().strip().lower()

    tags = tags_input if tags_input else None

    # calling add_entry method from JournalDatabase class.
    entry_id = db.add_entry(entry_text, mood, tags)

    if entry_id:
        print(f"\n🟢  Entry saved successfully! (ID: {entry_id})")
    else:
        print("\n🔴  Failed to save entry to database.")