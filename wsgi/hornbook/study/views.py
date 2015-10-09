from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from django.contrib.auth.models import User
from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from lexicon.models import Hanzi

from study.serializers import HanziStudyCountSerializer
from study.serializers import HanziStudyRecordSerializer
from study.serializers import UserSerializer

import leitner
import random
import jsonpickle


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    '''
    detail: pk -- user's id
    '''
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return HanziStudyCount.objects.filter(user=self.request.user)


class HanziStudyRecordViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return HanziStudyRecord.objects.filter(user=self.request.user)

    @list_route(methods=['GET', 'POST'])
    def leitner_record(self, request):
        if request.method == 'GET':
            return self._get_leitner_record(request)
        if request.method == 'POST':
            return self._set_leitner_record(request)

    def perform_create(self, serializer):
        hanzi_data = self.request.data['hanzi']
        hanzi, _ = Hanzi.objects.get_or_create(content=hanzi_data)
        serializer.save(user=self.request.user, hanzi=hanzi)

    def _get_leitner_record(self, request):
        NUM_RETIRED = 5
        NUM_PERMANENT = 10
        study_count, _ = HanziStudyCount.objects.get_or_create(user=request.user)

        current_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck='C')]
        level2_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck=str(leitner.get_deck_id(study_count.count, 2)), leitner_level=2)]
        level3_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck=str(leitner.get_deck_id(study_count.count, 3)), leitner_level=3)]
        level4_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck=str(leitner.get_deck_id(study_count.count, 4)), leitner_level=4)]
        retired_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck='R')]
        permanent_deck = [h for h in HanziStudyRecord.objects.filter(user=request.user, leitner_deck='P')]

        random.shuffle(retired_deck)
        random.shuffle(permanent_deck)
        ret = current_deck + level2_deck + level3_deck + level4_deck + retired_deck[:NUM_RETIRED] + permanent_deck[:NUM_PERMANENT]
        serializer = HanziStudyRecordSerializer(ret, many=True, context={'request': request})
        return Response(serializer.data)

    def _set_leitner_record(self, request):
        '''
        {
            "grasped_hanzi": ["u0x2345", "u0x2345"],
            "new_hanzi": ["u0x2345", "u0x2345"]
        }
        '''
        grasped_hanzi = jsonpickle.decode(request.POST['grasped_hanzi'])
        new_hanzi = jsonpickle.decode(request.POST['new_hanzi'])

        study_count = HanziStudyCount.objects.get(user=request.user)

        current_deck_id = leitner.get_deck_id(study_count.count, 1)

        for hanzi in grasped_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi:
                study_record = HanziStudyRecord.objects.get(user=request.user, hanzi=hanzi_instance)
                # update level
                study_record.leitner_level += 1
                # move from Deck Current to Session Deck
                if study_record.leitner_deck == 'C':
                    study_record.leitner_deck = current_deck_id
                # move from Session Deck to Deck Retired
                if study_record.leitner_level == 4:
                    study_record.leitner_deck = 'R'
                # move from Deck Retired to Deck Permanent
                if study_record.leitner_level >= 5:
                    study_record.leitner_level = 5
                    study_record.leitner_deck = 'P'
                study_record.save()

        for hanzi in new_hanzi:
            hanzi_instance, is_new_hanzi = Hanzi.objects.get_or_create(content=hanzi)
            if not is_new_hanzi:
                study_record = HanziStudyRecord.objects.get(user=request.user, hanzi=hanzi_instance)
                # move to Deck Current, set level to 0
                study_record.leitner_deck = 'C'
                study_record.leitner_level = 0
                study_record.forget_count += 1
                study_record.save()

        # update session count
        study_count.count += 1
        study_count.save()
        return Response('POST leitner')


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
