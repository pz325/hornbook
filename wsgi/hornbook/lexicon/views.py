from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import generics

from lexicon.models import Hanzi
from lexicon.serializers import HanziSerializer


class HanziViewSet(viewsets.ModelViewSet):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer


class HanziList(generics.ListAPIView):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer


class HanziCreate(generics.CreateAPIView):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer


class HanziDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer
    lookup_field = 'content'
