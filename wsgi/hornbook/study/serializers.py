from study.models import HanziStudyCount, HanziStudyRecord
from rest_framework import serializers
from django.contrib.auth.models import User
import django.utils.timezone


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    hanzi = serializers.CharField()
    # hanzi = serializers.SlugRelatedField(slug_field='content', queryset=Hanzi.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

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
        depth = 1
        read_only_fields = ('leitner_deck',
                            'leitner_level',
                            'study_date',
                            'revise_date',
                            'status',
                            'repeat_count',
                            'forget_count'
                            )

    def update(self, instance, validated_data):
        instance.revise_date = django.utils.timezone.now
        return instance


class UserSerializer(serializers.ModelSerializer):
    study_counts = serializers.SlugRelatedField(slug_field='count', read_only=True)
    study_records = serializers.HyperlinkedRelatedField(many=True, view_name='hanzistudyrecord-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'study_counts', 'study_records')
