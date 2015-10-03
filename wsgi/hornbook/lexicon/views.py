from django.shortcuts import render
from django.http import Http404

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lexicon.models import Hanzi
from lexicon.serializers import HanziSerializer


class HanziViewSet(viewsets.ModelViewSet):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer


class HanziList(APIView):
    def get(self, request, format=None):
        hanzis = Hanzi.objects.all()
        serializer = HanziSerializer(hanzis, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HanziSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class HanziDetail(APIView):
    def get_object(self, content):
        try:
            # TODO: could return multiple hanzis (e.g. heteronym (polyphone) )
            return Hanzi.objects.get(content=content)
        except Hanzi.DoesNotExist:
            raise Http404

    def get(self, request, content, format=None):
        hanzi = self.get_object(content)
        serializer = HanziSerializer(hanzi)
        return Response(serializer.data)

    def put(self, request, content, format=None):
        hanzi = self.get_object(content)
        serializer = HanziSerializer(hanzi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, content, format=None):
        hanzi = self.get_object(content)
        hanzi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
