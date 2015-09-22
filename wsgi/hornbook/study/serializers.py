from study.models import HanziStudyCount, HanziStudyRecord
from rest_framework import serializers


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HanziStudyRecord
        fileds = ('haizi',
            'leitner_deck',
            'leitner_level',
            'user',
            'study_date',
            'revise_date',
            'status',
            'repeat_count',
            'forget_count'
        )
