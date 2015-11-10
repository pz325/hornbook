from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from study.models import Category
from rest_framework import serializers
from django.contrib.auth.models import User
import django.utils.timezone


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Category
        fileds = ('user', 'name')


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedIdentityField(view_name='user-detail')

    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    hanzi = serializers.CharField()
    category = serializers.CharField()
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = HanziStudyRecord
        fileds = ('haizi',
                  'category',
                  'leitner_deck',
                  'user',
                  'study_date',
                  'revise_date',
                  'status',
                  'repeat_count',
                  'forget_count'
                  )
        depth = 1
        read_only_fields = ('leitner_deck',
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
    categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'study_counts', 'study_records', 'categories')
