from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.contrib.auth.models import User
from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from study.models import Category
from lexicon.models import Hanzi

from study.serializers import HanziStudyCountSerializer
from study.serializers import HanziStudyRecordSerializer
from study.serializers import UserSerializer
from study.serializers import CategorySerializer

import leitner
import random
import jsonpickle


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_class = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    '''
    detail: pk -- user's id
    '''
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return HanziStudyCount.objects.filter(user=self.request.user)


class HanziStudyRecordViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        '''
        filter by user and category
        '''
        category_key = 'category'
        if category_key in self.request.query_params:
            category_data = self.request.query_params[category_key]
        if category_key in self.request.data:
            category_data = self.request.data[category_key]

        category_instance = get_object_or_404(Category, user=self.request.user, name=category_data)
        return HanziStudyRecord.objects.filter(user=self.request.user, category=category_instance)

    def perform_create(self, serializer):
        hanzi_data = self.request.data['hanzi']
        category_data = self.request.data['category']
        hanzi, _ = Hanzi.objects.get_or_create(content=hanzi_data)
        category = get_object_or_404(Category, user=self.request.user, name=category_data)
        serializer.save(user=self.request.user, hanzi=hanzi, category=category)

    @list_route(methods=['GET', 'POST'])
    def leitner_record(self, request):
        if request.method == 'GET':
            return self._get_leitner_record(request)
        if request.method == 'POST':
            return self._set_leitner_record(request)

    @list_route(methods=['GET'])
    def progress(self, request):
        return self._get_progress(request)

    def _get_progress(self, request):
        all_records = self.get_queryset()

        count_new = all_records.filter(leitner_deck='C').count()
        count_grasped = all_records.filter(leitner_deck='R').count()
        count_studying = all_records.count() - count_new - count_grasped

        ret = {
            'new': count_new,
            'studying': count_studying,
            'grasped': count_grasped,
            }

        return Response(ret)

    def _get_leitner_record(self, request):
        '''
        query parameter: num_retired
        '''
        all_records = self.get_queryset()

        NUM_RETIRED = 10
        num_retired_key = 'num_retired'
        num_retired = int(request.query_params[num_retired_key]) if num_retired_key in request.query_params else NUM_RETIRED
        study_count, _ = HanziStudyCount.objects.get_or_create(user=request.user)
        deck_ids = leitner.decks_to_review(study_count.count)

        ret = []
        ret = ret + [h for h in all_records.filter(leitner_deck='C')]  # current deck
        for i in deck_ids:
            ret = ret + [h for h in all_records.filter(leitner_deck=i)]  # progres deck

        retired_deck = all_records.filter(leitner_deck='R')
        index = range(0, len(retired_deck))
        random.shuffle(index)
        picked_retired = [retired_deck[i] for i in index[:num_retired]]
        for r in picked_retired:
            r.repeat_count += 1
            r.save()
        ret = ret + [h for h in picked_retired]

        serializer = HanziStudyRecordSerializer(ret, many=True, context={'request': request})
        return Response(serializer.data)

    def _set_leitner_record(self, request):
        '''
        {
            "grasped_hanzi": ["u0x2345", "u0x2345"],
            "new_hanzi": ["u0x2345", "u0x2345"],
            "category": "category_name"
        }
        in terms of new_hanzi, if hanzi is new, create a new record; else, set record's leitner deck to 'C'
        '''
        all_records = self.get_queryset()

        grasped_hanzi_key = 'grasped_hanzi'
        new_hanzi_key = 'new_hanzi'
        grasped_hanzi = request.data[grasped_hanzi_key] if grasped_hanzi_key in request.data else []
        new_hanzi = request.data[new_hanzi_key] if new_hanzi_key in request.data else []
        study_count = HanziStudyCount.objects.get(user=request.user)

        grasped_hanzi = jsonpickle.decode(grasped_hanzi)
        new_hanzi = jsonpickle.decode(new_hanzi)

        for hanzi in grasped_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi:
                study_record = all_records.get(hanzi=hanzi_instance)
                # move from Deck Current to Session Deck
                if study_record.leitner_deck == 'C':
                    study_record.leitner_deck = str(study_count.count % 10)
                # move from Session Deck to Deck Retired
                if leitner.is_last_number_on_deck(study_record.leitner_deck, study_count.count):
                    study_record.leitner_deck = 'R'
                study_record.save()

        for hanzi in new_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi:
                study_record = all_records.get(hanzi=hanzi_instance)
                # move to Deck Current
                study_record.leitner_deck = 'C'
                study_record.forget_count += 1
                study_record.save()
            else:
                category_instance = get_object_or_404(Category, user=request.user, name=request.data['category'])
                HanziStudyRecord.objects.create(user=request.user, category=category_instance, hanzi=hanzi_instance)

        # update session count
        study_count.count += 1
        study_count.save()
        return Response(request.data)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
