import numpy as np

def calculate_power_flow(bus_loads, line_impedances):
    print("Bus Loads:", bus_loads)
    print("Line Impedances:", line_impedances)

    # Ensure correct dimensions
    if len(bus_loads) != len(set([i[0] for i in line_impedances] + [i[1] for i in line_impedances])):
        return {"error": "Mismatch between bus loads and impedance data"}

