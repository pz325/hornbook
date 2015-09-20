from django.shortcuts import render
from rest_framework import viewsets
from study.serializers import HanziStudyCountSerializer
from study.models import HanziStudyCount


class HanziStudyCountViewSet(viewsets.ModelViewSet):
    queryset = HanziStudyCount.objects.all()
    serializer_class = HanziStudyCountSerializer
