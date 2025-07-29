import numpy as np

# commonroad
from commonroad_route_planner.utility.route_util import chaikins_corner_cutting as rpccc
from commonroad_velocity_planner.preprocessing.elastic_band_algo import (
    smooth_path_elastic_bands,
)


def chaikins_corner_cutting(
    polyline: np.ndarray, num_refinements: int = 4
) -> np.ndarray:
    """
    Smoothing algorithm Chaikin's corner cutting
    :param polyline: (n,2) np.ndarray
    :param num_refinements: number of algorithm loops
    :return: smoothed polyline as (n,2) np.ndarray
    """
    return rpccc(polyline=polyline, num_refinements=num_refinements)


def elastic_band_smoothing(
    polyline: np.ndarray, max_deviation: float = 0.15
) -> np.ndarray:
    """
    Smoothing algorithm elastic band
    :param polyline: (n,2) np.ndarray
    :param max_deviation: maximum lateral deviation for smoothed path
    :return: smoothed polyline as (n,2) np.ndarray
    """
    x, y = smooth_path_elastic_bands(path=polyline, max_deviation=max_deviation)
    return np.concatenate((x, y), axis=1)
