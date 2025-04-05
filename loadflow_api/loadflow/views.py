from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .models import Bus, Line, Load
from .serializers import BusSerializer, LineSerializer, LoadSerializer
from .utils import calculate_power_flow
from django.http import JsonResponse



class BusListView(ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetailView(RetrieveUpdateDestroyAPIView):  # ✅ Allows GET, PUT, PATCH, DELETE
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    

class LineListView(ListCreateAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class LineDetailView(RetrieveUpdateDestroyAPIView):  # ✅ Allows GET, PUT, PATCH, DELETE
    queryset = Line.objects.all()
    serializer_class = LineSerializer

class LoadListView(ListCreateAPIView):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

class LoadDetailView(RetrieveUpdateDestroyAPIView):  # ✅ Allows GET, PUT, PATCH, DELETE
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

# Load flow calculation API
class LoadFlowAnalysisView(APIView):
    def get(self, request):
        # Fetch all buses, lines, and loads
        buses = list(Bus.objects.all())
        lines = list(Line.objects.exclude(impedance_real=0, impedance_imag=0))
        loads = list(Load.objects.all())

        # Return error if required data is missing
        if not buses:
            return Response({"error": "No buses available"}, status=400)

        if not lines:
            return Response({"error": "No valid transmission lines available"}, status=400)

        if not loads:
            return Response({"error": "No loads available"}, status=400)
        
        num_buses = len(buses)
        bus_id_map = {bus.id: idx for idx, bus in enumerate(buses)}

        # Map bus loads
        bus_loads = np.zeros(num_buses, dtype=complex)
        for load in loads:
            if load.bus.id in bus_id_map:
                idx = bus_id_map[load.bus.id]
                bus_loads[idx] += complex(load.load_real, load.load_imag)
        # Extract line impedances (excluding zero-impedance lines)
        line_impedances = [
            (bus_id_map[line.from_bus.id], bus_id_map[line.to_bus.id], complex(line.impedance_real, line.impedance_imag)) 
            for line in lines
        ]


        
        # Run power flow analysis
        try:
            voltages = calculate_power_flow(bus_loads, line_impedances)
        except Exception as e:
            return Response({"error": f"Load flow calculation failed: {str(e)}"}, status=500)

        return Response({"bus_voltages": list(voltages.values())})
    
# Load flow calculation function
def run_load_flow(request):
    buses = list(Bus.objects.all())
    lines = list(Line.objects.all())

    num_buses = len(buses)
    if num_buses < 2:
        return JsonResponse({"error": "At least two buses are required."})
    
    # Create bus ID mapping
    bus_id_map = {bus.id: idx for idx, bus in enumerate(buses)}    

    # Create Y-Bus Matrix
    Y_bus = np.zeros((num_buses, num_buses), dtype=complex)
    for line in lines:
            if line.from_bus.id in bus_id_map and line.to_bus.id in bus_id_map:
                i, j = bus_id_map[line.from_bus.id], bus_id_map[line.to_bus.id]
                impedance = complex(line.impedance_real, line.impedance_imag)
                admittance = 1 / impedance
                Y_bus[i, i] += admittance
                Y_bus[j, j] += admittance
                Y_bus[i, j] -= admittance
                Y_bus[j, i] -= admittance
    # Check for singular matrix before solving
    if np.linalg.matrix_rank(Y_bus) < num_buses:
        return JsonResponse({"error": "Y-Bus matrix is singular."}, status=400)

    try:
            voltages = np.linalg.solve(Y_bus, num_buses)
    except np.linalg.LinAlgError:
            return JsonResponse({"error": "Numerical issue: Cannot solve system."}, status=500)

    return JsonResponse({f"bus_{buses[idx].id}_voltage": abs(voltages[idx]) for idx in range(num_buses)})

        