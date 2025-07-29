"""
Aerotransport - Estimación de tiempos de vuelo y consumos de combustible.
"""

from .core import (
    estimate_co2_emissions,
    estimate_flight_cost,
    estimate_flight_time,
    estimate_fuel_consumption,
)
from .exceptions import AerotransportError
from .models.airplane import Airplane
from .models.airport import Airport
from .models.flight import Flight

__all__ = [
    "estimate_flight_time",
    "estimate_fuel_consumption",
    "estimate_flight_cost",
    "estimate_co2_emissions",
    "Airplane",
    "Flight",
    "Airport",
    "AerotransportError",
]
