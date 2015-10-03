from rest_framework import viewsets

from lexicon.models import Hanzi
from lexicon.serializers import HanziSerializer


class HanziViewSet(viewsets.ModelViewSet):
    queryset = Hanzi.objects.all()
    serializer_class = HanziSerializer
    lookup_field = 'content'
