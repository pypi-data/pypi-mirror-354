from ..utils import (  # la función que hicimos con geopy
    calculate_distance_between_points,
)
from .airport import Airport


class Flight:
    """
    Representa un vuelo entre dos aeropuertos.
    """

    def __init__(self, origin: Airport, destination: Airport):
        """
        Args:
            origin (Airport): Aeropuerto de origen.
            destination (Airport): Aeropuerto de destino.
        """
        self.origin = origin
        self.destination = destination
        self.distance_km = calculate_distance_between_points(
            (origin.latitude, origin.longitude),
            (destination.latitude, destination.longitude),
        )

    def __repr__(self):
        return f"<Flight {self.origin.iata_code} -> {self.destination.iata_code} ({self.distance_km:.1f} km)>"
