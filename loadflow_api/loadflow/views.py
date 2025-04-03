from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .models import Bus, Line, Load
from .serializers import BusSerializer, LineSerializer, LoadSerializer
from .utils import calculate_power_flow


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
class LoadFlowAnalysisView(APIView):
    def get(self, request):
        # Fetch all buses, lines, and loads
        buses = Bus.objects.all()
        lines = Line.objects.exclude(impedance=0)  # Ignore zero-impedance lines
        loads = Load.objects.all()

        # Return error if required data is missing
        if not buses.exists():
            return Response({"error": "No buses available"}, status=400)

        if not lines.exists():
            return Response({"error": "No valid transmission lines available"}, status=400)

        if not loads.exists():
            return Response({"error": "No loads available"}, status=400)

        # Map bus IDs to their load power
        load_values = {load.bus.id: load.power for load in loads}

        # Assign loads to buses (defaulting to 0 if no load is attached)
        bus_loads = np.array([load_values.get(bus.id, 0) for bus in buses])

        # Extract line impedances (excluding zero-impedance lines)
        line_impedances = [(line.from_bus.id, line.to_bus.id, line.impedance) for line in lines]

        # Run power flow analysis
        try:
            voltages = calculate_power_flow(bus_loads, line_impedances)
        except Exception as e:
            return Response({"error": f"Load flow calculation failed: {str(e)}"}, status=500)

        return Response({"bus_voltages": voltages.tolist()})
