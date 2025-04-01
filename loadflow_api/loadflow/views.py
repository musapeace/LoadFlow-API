from rest_framework.generics import ListCreateAPIView
from .models import Bus, Line, Load
from .serializers import BusSerializer, LineSerializer, LoadSerializer

class BusListView(ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class LineListView(ListCreateAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class LoadListView(ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer