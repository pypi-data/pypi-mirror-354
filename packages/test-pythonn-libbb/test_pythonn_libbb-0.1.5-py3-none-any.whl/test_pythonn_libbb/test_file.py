import numpy as np

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def matrix_add(x, y, z):
    x, y, z = np.array(x), np.array(y), np.array(z)

    return x + y + z

def matrix_subtract(x, y, z):
    x, y, z = np.array(x), np.array(y), np.array(z)

    return x - y - z