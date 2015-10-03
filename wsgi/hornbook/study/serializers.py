from study.models import HanziStudyCount, HanziStudyRecord
from rest_framework import serializers
from django.contrib.auth.models import User
# from django.db import models


from lexicon.models import Hanzi


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    # hanzi = serializers.PrimaryKeyRelatedField(queryset=Hanzi.objects.all())
    hanzi = serializers.HyperlinkedRelatedField(view_name='hanzi-detail', lookup_field='content', queryset=Hanzi.objects.all())
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

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


class UserSerializer(serializers.ModelSerializer):
    study_counts = serializers.HyperlinkedIdentityField(view_name='hanzistudycount-detail')
    # study_records = serializers.HyperlinkedRelatedField(many=True, view_name='hanzistudyrecord-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'study_counts')
