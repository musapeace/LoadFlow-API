from rest_framework.generics import ListCreateAPIView
from .models import Bus, Line, Load
from .serializers import BusSerializer, LineSerializer, LoadSerializer
from .utils import calculate_power_flow
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np


class BusListView(ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class LineListView(ListCreateAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class LoadListView(ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer


class BusListView(ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class LineListView(ListCreateAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class LoadListView(ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

# Load flow calculation API
class LoadlowAnalysisView(APIView):
    def get(self, request):
        loads = np.array([10, 5])  # Replace with actual DB values
        lines = []  # Replace with line impedance data

        voltages = calculate_power_flow(loads, lines)

        return Response({"bus_voltages": voltages.tolist()})