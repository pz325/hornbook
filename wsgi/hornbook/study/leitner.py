DECK_TYPE = (
    ('C', 'Current'),
    ('0', 'Progress_0'),
    ('1', 'Progress_1'),
    ('2', 'Progress_2'),
    ('3', 'Progress_3'),
    ('4', 'Progress_4'),
    ('5', 'Progress_5'),
    ('6', 'Progress_6'),
    ('7', 'Progress_7'),
    ('8', 'Progress_8'),
    ('9', 'Progress_9'),
    ('R', 'Retired'),
    )

DECK_NUMBERS = {
    '0': [0, 2, 5, 9],
    '1': [1, 3, 6, 0],
    '2': [2, 4, 7, 1],
    '3': [3, 5, 8, 2],
    '4': [4, 6, 9, 3],
    '5': [5, 7, 0, 4],
    '6': [6, 8, 1, 5],
    '7': [7, 9, 2, 6],
    '8': [8, 0, 3, 7],
    '9': [9, 1, 4, 8]
}


def decks_to_review(number):
    deck_ids = []
    for i in [str(x) for x in range(0, 10)]:
        if to_review(i, number):
            deck_ids.append(i)
    return deck_ids


def to_review(deck_id, number):
    return number % 10 in DECK_NUMBERS[deck_id]


def is_last_number_on_deck(deck_id, number):
    return number == DECK_NUMBERS[deck_id][-1]
