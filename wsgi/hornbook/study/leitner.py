def get_deck_id(session_count, level):
    deck_id = -1
    if 1 == level:
        deck_id = session_count % 10
    elif 2 == level:
        deck_id = (session_count + 8) % 10
    elif 3 == level:
        deck_id = (session_count + 5) % 10
    elif 4 == level:
        deck_id = (session_count + 1) % 10

    return deck_id
