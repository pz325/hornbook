from study.models.card import Card
from study.models.category import Category
from study.models.study import HanziStudyCount
from study.models.study import HanziStudyRecord
from django.contrib.auth.models import User
from lexicon.models import Hanzi


def create_one_Card_instance(font_size='font_size'):
    return Card.objects.create(font_size=font_size)


def create_Card_instances(num_to_create):
    font_sizes = []
    for i in range(0, num_to_create):
        font_size = 'font_size' + str(i)
        create_one_Card_instance(font_size)
        font_sizes.append(font_size)
    return font_sizes


def create_one_Category_instance(user, card_id, display='display'):
    return Category.objects.create(user=user, card_id=card_id, display=display)


def create_Category_instances(user, num_to_create):
    displays = []
    for i in range(0, num_to_create):
        display = 'display' + str(i)
        card = create_one_Card_instance()
        Category.objects.create(user=user, card_id=card.id, display=display)
        displays.append(display)

    return displays


def create_one_HanziStudyCount_instance(user, category, count):
    return HanziStudyCount.objects.create(
        user=user,
        category=category,
        count=count
        )


def create_one_User_instance(username):
    return User.objects.create(username=username)


def create_one_HanziStudyRecord_instance(user, category, hanzi):
    hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
    return HanziStudyRecord.objects.create(
        user=user,
        category=category,
        hanzi=hanzi_instance
        )


def create_one_leitner_record(user, category, hanzi, deck_id):
    hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)
    category_instance, _ = Category.objects.get_or_create(user=user, name=category)
    return HanziStudyRecord.objects.create(
        user=user,
        hanzi=hanzi_instance,
        category=category_instance,
        leitner_deck=deck_id)
