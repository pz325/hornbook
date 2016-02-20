from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.contrib.auth.models import User
from models.study import HanziStudyCount
from models.study import HanziStudyRecord
from models.category import Category
from models.log import StudySessionContentLog
from models.log import StudySessionResultLog
from lexicon.models import Hanzi
from models.card import Card

from serializers import HanziStudyCountSerializer
from serializers import HanziStudyRecordSerializer
from serializers import UserSerializer
from serializers import CategorySerializer
from serializers import CardSerializer

import models.leitner as leitner

import random
import jsonpickle
import logging
log = logging.getLogger('hornbook')


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    login required, so by default, filtering against the current user
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_class = (permissions.IsAuthenticated,)

    # def perform_create(self, serializer):
    #     print('==== perform_create ====')
    #     print(self.request.data)
    #     card_id = self.request.data['card_id']
    #     card_instance = get_object_or_404(Card, id=card_id)
    #     serializer.save(user=self.request.user, card=card_instance)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    '''
    detail: pk -- category id  e.g. api/study/hanzi_study_count/1"

    login required, so by default, filtering against the current user
    '''
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        '''
        required 'category_id' is part of POST body
        '''
        category_id = None
        if 'category_id' in self.request.data:
            category_id = self.request.data['category_id']
        category_instance = get_object_or_404(Category, id=category_id)
        serializer.save(user=self.request.user, category=category_instance)

    def get_queryset(self):
        '''
        filter by user, and category if asked
        '''
        queryset = self.queryset.filter(user=self.request.user)
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            category_instance = get_object_or_404(Category, id=category_id)
            queryset = self.queryset.filter(category=category_instance)

        return queryset


class HanziStudyRecordViewSet(viewsets.ModelViewSet):
    '''
    login required, so by default, filtering against the current user
    '''
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        '''
        filter by user, and category if provided
        '''
        queryset = self.queryset.filter(user=self.request.user)
        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            category_instance = get_object_or_404(Category, id=category_id)
            queryset = self.queryset.filter(category=category_instance)
        return queryset

    def perform_create(self, serializer):
        '''
        required fields in the POST data:
            hanzi
            category
        '''
        category_id = None
        if 'category_id' in self.request.data:
            category_id = self.request.data['category_id']
        category_instance = get_object_or_404(Category, id=category_id)

        hanzi = self.request.data['hanzi']
        hanzi_instance, _ = Hanzi.objects.get_or_create(content=hanzi)

        serializer.save(user=self.request.user, hanzi=hanzi_instance, category=category_instance)

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
        required query parameter:
            Category
        optional query parameter:
            num_retired
        '''
        all_records = self.get_queryset()

        category_id = request.query_params.get('category_id', None)
        category_instance = get_object_or_404(Category, id=category_id)

        NUM_RETIRED = 15
        num_retired = request.query_params.get('num_retired', NUM_RETIRED)
        num_retired = int(num_retired)
        study_count, _ = HanziStudyCount.objects.get_or_create(user=request.user, category=category_instance)
        deck_ids = leitner.decks_to_review(study_count.count)

        current_deck_contents = [h for h in all_records.filter(leitner_deck='C')]  # current deck
        progress_deck_contents = []
        for i in deck_ids:
            progress_deck_contents = progress_deck_contents + [h for h in all_records.filter(leitner_deck=i)]  # progres deck

        retired_deck = all_records.filter(leitner_deck='R')
        index = range(0, len(retired_deck))
        random.shuffle(index)
        picked_retired = [retired_deck[i] for i in index[:num_retired]]
        retired_deck_contents = [h for h in picked_retired]

        ret = current_deck_contents + progress_deck_contents + retired_deck_contents

        serializer = HanziStudyRecordSerializer(ret, many=True, context={'request': request})
        # log.debug(study_count)
        # log.debug(serializer.data)
        StudySessionContentLog.objects.create(
            session_count=study_count.count,
            category=category_instance.user.username + category_instance.display,
            current_deck_contents=' '.join([h.hanzi.content for h in current_deck_contents]),
            progress_deck_contents=' '.join([h.hanzi.content for h in progress_deck_contents]),
            retired_deck_contents=' '.join([h.hanzi.content for h in picked_retired]))
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

        category_id = None
        if 'category_id' in self.request.data:
            category_id = self.request.data['category_id']
        category_instance = get_object_or_404(Category, id=category_id)
        all_records = all_records.filter(category=category_instance)

        grasped_hanzi_key = 'grasped_hanzi'
        new_hanzi_key = 'new_hanzi'
        grasped_hanzi = request.data[grasped_hanzi_key] if grasped_hanzi_key in request.data else []
        new_hanzi = request.data[new_hanzi_key] if new_hanzi_key in request.data else []
        study_count = get_object_or_404(HanziStudyCount, user=request.user, category=category_instance)
        # log.debug(study_count)
        # log.debug(request.data)

        grasped_hanzi = jsonpickle.decode(grasped_hanzi)
        new_hanzi = jsonpickle.decode(new_hanzi)

        for hanzi in grasped_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi:
                study_record = all_records.get(hanzi=hanzi_instance, category=category_instance)
                study_record.repeat_count += 1
                # move from Deck Current to Session Deck
                if study_record.leitner_deck == 'C':
                    study_record.leitner_deck = str(study_count.count % 10)
                # move from Session Deck to Deck Retired
                elif study_record.leitner_deck != 'R' and leitner.is_last_number_on_deck(study_record.leitner_deck, study_count.count):
                    study_record.leitner_deck = 'R'
                study_record.save()

        for hanzi in new_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi and all_records.filter(hanzi=hanzi_instance).count() > 0:
                study_record = all_records.get(hanzi=hanzi_instance)
                # move to Deck Current
                study_record.leitner_deck = 'C'
                study_record.forget_count += 1
                study_record.repeat_count += 1
                study_record.save()
            else:
                HanziStudyRecord.objects.create(user=request.user, category=category_instance, hanzi=hanzi_instance)

        if len(grasped_hanzi) > 0:
            # update session count
            study_count.count += 1
            study_count.save()
        # log.debug(study_count)
        StudySessionResultLog.objects.create(
            session_count=study_count.count,
            category=category_instance.user.username + category_instance.display,
            grasped_contents=' '.join(grasped_hanzi),
            new_contents=' '.join(new_hanzi))
        return Response(request.data)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    '''
    login required, so by default, filtering against the current user
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
