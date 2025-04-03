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
        buses = Bus.objects.all()
        lines = Line.objects.all()

        if not buses.exists():
            return Response({"error": "No buses available"}, status=400)

        if not lines.exists():
            return Response({"error": "No transmission lines available"}, status=400)

        # Extract bus loads
        loads = np.array([bus.load for bus in buses])  # Replace with actual DB values

        # Extract line impedances and check for zero impedance
        line_impedances = [line.impedance for line in lines]

        if any(z == 0 for z in line_impedances):
            return Response({"error": "Transmission line impedance cannot be zero"}, status=400)

        # Call power flow calculation
        voltages = calculate_power_flow(loads, line_impedances)

        return Response({"bus_voltages": voltages.tolist()})
