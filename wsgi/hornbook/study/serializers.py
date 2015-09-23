from study.models import HanziStudyCount, HanziStudyRecord
from rest_framework import serializers
from django.contrib.auth.models import User


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

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


class UserStudyRecordSerializer(serializers.ModelSerializer):
    study_records = serializers.PrimaryKeyRelatedField(many=True, queryset=HanziStudyRecord.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'study_records')
