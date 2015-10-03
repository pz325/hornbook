from django.shortcuts import render


from rest_framework import viewsets
from rest_framework import permissions

from django.contrib.auth.models import User
from study.models import HanziStudyCount
from study.models import HanziStudyRecord
from lexicon.models import Hanzi

from study.serializers import HanziStudyCountSerializer
from study.serializers import HanziStudyRecordSerializer
from study.serializers import UserSerializer
from study.permissions import IsOwnerOrReadOnly


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    '''
    detail: pk -- user's id
    '''
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HanziStudyRecordViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        hanzi_data = self.request.data['hanzi']
        hanzi, _ = Hanzi.objects.get_or_create(content=hanzi_data)
        serializer.save(user=self.request.user, hanzi=hanzi)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly)
