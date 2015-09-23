from lexicon.models import Hanzi
from rest_framework import serializers


class HanziSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hanzi
