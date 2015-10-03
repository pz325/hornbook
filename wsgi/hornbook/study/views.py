from django.shortcuts import render
from django.http import Http404


from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.contrib.auth.models import User
from study.models import HanziStudyCount
from study.models import HanziStudyRecord

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
    studyCount = HanziStudyCount.objects
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly)
