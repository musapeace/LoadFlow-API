from rest_framework.generics import ListCreateAPIView
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
        lines = Line.objects.exclude(impedance_real=0, impedance_imag=0)
        loads = Load.objects.all()

        # Return error if required data is missing
        if not buses.exists():
            return Response({"error": "No buses available"}, status=400)

        if not lines.exists():
            return Response({"error": "No valid transmission lines available"}, status=400)

        if not loads.exists():
            return Response({"error": "No loads available"}, status=400)
        
        # Map bus IDs to their voltage levels
        bus_id_map = {bus.id: idx for idx, bus in enumerate(buses)}

        # Map bus loads
        load_values = {load.bus.id: load.power for load in loads}
        bus_loads = np.array([load_values.get(bus.id, 0) for bus in buses])

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

        return Response({"bus_voltages": voltages.tolist()})
    
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
        i = bus_id_map[line.from_bus.id]
        j = bus_id_map[line.to_bus.id]
        impedance = complex(line.impedance_real, line.impedance_imag)  
        
        if impedance == 0:
            continue

        admittance = 1 / impedance
        Y_bus[i, i] += admittance
        Y_bus[j, j] += admittance
        Y_bus[i, j] -= admittance
        Y_bus[j, i] -= admittance

    # Check for singular matrix before solving
    if np.linalg.matrix_rank(Y_bus) < num_buses:
        return JsonResponse({"error": "Load flow calculation failed: Matrix is singular, check bus connections."})


    # Solve for voltages (simple test case)
    voltages = np.linalg.solve(Y_bus, np.ones(num_buses))  # Adjust for actual power injections

    return JsonResponse({f"bus_{i+1}_voltage": abs(v) for i, v in enumerate(voltages)})