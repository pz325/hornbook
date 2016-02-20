from models.card import Card
from models.study import HanziStudyCount
from models.study import HanziStudyRecord
from models.category import Category
from rest_framework import serializers
from django.contrib.auth.models import User
import django.utils.timezone


class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        files = ('id', 'font_size')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    card = CardSerializer()
    id = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fileds = ('user', 'id', 'display', 'num_retired', 'card')
        read_only_fields = ('card')


class HanziStudyCountSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    category = serializers.SlugRelatedField(slug_field='id', read_only=True)

    class Meta:
        model = HanziStudyCount
        fileds = ('user', 'category', 'count', 'timestamp')


class HanziStudyRecordSerializer(serializers.HyperlinkedModelSerializer):
    hanzi = serializers.CharField()
    category = serializers.SlugRelatedField(slug_field='id', read_only=True)
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
    study_records = serializers.HyperlinkedRelatedField(many=True, view_name='hanzistudyrecord-detail', read_only=True)
    categories = serializers.HyperlinkedRelatedField(many=True, view_name='category-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'study_records', 'categories')
