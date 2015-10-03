from django.shortcuts import render

from rest_framework import viewsets

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lexicon.models import Hanzi
from lexicon.serializers import HanziSerializer


class HanziViewSet(viewsets.ModelViewSet):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer


@api_view(['GET', 'POST'])
def hanzi_list(request):
    if request.method == 'GET':
        hanzis = Hanzi.objects.all()
        serializer = HanziSerializer(hanzis, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HanziSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def hanzi_detail(request, content):
    try:
        print(content)
        hanzi = Hanzi.objects.get(content=content)
    except Hanzi.DoesNotExist:
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HanziSerializer(hanzi)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = HanziSerializer(hanzi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        hanzi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
