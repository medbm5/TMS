import pandas as pd
import math

import numpy as np
from math import sin, cos, sqrt, atan2, radians

from scipy.spatial.distance import pdist, squareform



def dist(x, y):
    """Function to compute the distance between two points x, y"""

    lat1 = radians(float(x[0]))
    lon1 = radians(float(x[1]))
    lat2 = radians(float(y[0]))
    lon2 = radians(float(y[1]))

    R = 6373.0

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return round(distance, 4)

def get_matrix_distances(df):
    distances = pdist(df.values, metric=dist)

    points = [f'point_{i}' for i in range(1, len(df) + 1)]

    result = pd.DataFrame(squareform(distances), columns=points, index=points)
    result=result.to_numpy()
    result[np.diag_indices_from(result)] = math.inf
    return(result)
