import numpy as np

def calculate_power_flow(bus_loads, line_impedances, slack_bus=0, tolerance=1e-6):
    num_buses = len(bus_loads)
    Y = np.zeros((num_buses, num_buses), dtype=complex)

    # Create Y-Bus matrix
    for i, j, z in line_impedances:
        y = 1 / z
        Y[i, i] += y
        Y[j, j] += y
        Y[i, j] -= y
        Y[j, i] -= y


    # Initialize voltage vector
    V = np.ones(num_buses, dtype=complex) 
    V[slack_bus] = 1.0  # Slack bus voltage


    for _ in range(10):  # Few iterations for simplicity
        for i in range(num_buses):
            if i == slack_bus:
                continue
            sum_yv = sum(Y[i][j] * V[j] for j in range(num_buses) if j != i)
            V[i] = (1 / Y[i][i]) * ((bus_loads[i] / np.conj(V[i])) - sum_yv)

    return {i: round(abs(V[i]), 4) for i in range(num_buses)}

