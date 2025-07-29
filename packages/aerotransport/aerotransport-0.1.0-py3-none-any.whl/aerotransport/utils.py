import math
from typing import Tuple

from geopy.distance import geodesic


def nm_to_km(nm: float) -> float:
    """Convierte millas náuticas a kilómetros."""
    return nm * 1.852


def km_to_nm(km: float) -> float:
    """Convierte kilómetros a millas náuticas."""
    return km / 1.852


def calculate_distance_between_points(
    point1: Tuple[float, float], point2: Tuple[float, float], method: str = "geopy"
) -> float:
    """
    Calcula la distancia ortodrómica (gran círculo) entre dos puntos geográficos.

    Args:
        point1: Tuple (latitud, longitud) en grados decimales.
        point2: Tuple (latitud, longitud) en grados decimales.
        method: 'geopy' para usar geodesic (Vincenty/Geodesic),
                'haversine' para usar la fórmula haversine.

    Returns:
        Distancia en kilómetros (float).
    """
    if method == "geopy":
        return geodesic(point1, point2).kilometers
    elif method == "haversine":
        R = 6371.0  # Radio medio de la Tierra en km
        lat1, lon1 = point1
        lat2, lon2 = point2
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    else:
        raise ValueError(f"Método de cálculo no soportado: {method}")
