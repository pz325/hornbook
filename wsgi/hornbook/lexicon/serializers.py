from lexicon.models import Hanzi
from rest_framework import serializers


class HanziSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hanzi
