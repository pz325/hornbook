from study.models import HanziStudyCount
from rest_framework import serializers


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')
