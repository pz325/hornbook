from django.shortcuts import render
from rest_framework import viewsets
from study.serializers import HanziStudyCountSerializer, HanziStudyRecordSerializer
from study.models import HanziStudyCount, HanziStudyRecord


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer


class HanziStudyRecordViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyRecord.objects.all()
    serializer_class = HanziStudyRecordSerializer
