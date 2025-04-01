import numpy as np

def calculate_power_flow(loads, lines):
    Ybus = np.array([[complex(0, -10), complex(0, 10)], 
                     [complex(0, 10), complex(0, -10)]])
    V = np.linalg.solve(Ybus, loads)
    return V
