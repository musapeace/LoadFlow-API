from django.shortcuts import render

from rest_framework import generics
from .models import Bus, Generator, Load
from .serializers import BusSerializer, GeneratorSerializer, LoadSerializer

class BusListCreate(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class GeneratorListCreate(generics.ListCreateAPIView):
    queryset = Generator.objects.all()
    serializer_class = GeneratorSerializer

class LoadListCreate(generics.ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

