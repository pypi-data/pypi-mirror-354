from .exceptions import AerotransportError
from .models.airplane import Airplane
from .models.flight import Flight
from .utils import calculate_distance_between_points

CO2_EMISSION_FACTOR = 3.16  # kg CO2 por litro de combustible de aviación


def estimate_flight_time(flight: Flight, airplane: Airplane) -> float:
    """
    Estima el tiempo de vuelo en horas.
    """
    if airplane.cruise_speed <= 0:
        raise AerotransportError("La velocidad de crucero debe ser positiva.")
    return flight.distance_km / airplane.cruise_speed


def estimate_fuel_consumption(flight: Flight, airplane: Airplane) -> float:
    """
    Estima el consumo de combustible en litros.
    """
    flight_time = estimate_flight_time(flight, airplane)
    return flight_time * airplane.fuel_burn_rate


def calculate_flight_distance(flight: Flight, method: str = "geopy") -> float:
    """
    Calcula la distancia entre los aeropuertos de origen y destino de un vuelo.

    Args:
        flight: objeto Flight con atributos origin y destination (cada uno con latitud y longitud).
        method: método de cálculo ('geopy' o 'haversine').

    Returns:
        Distancia en kilómetros.
    """
    origin_coords = (flight.origin.latitude, flight.origin.longitude)
    destination_coords = (flight.destination.latitude, flight.destination.longitude)
    return calculate_distance_between_points(origin_coords, destination_coords, method)


def estimate_flight_cost(
    flight: Flight, airplane: Airplane, fuel_cost_per_liter: float
) -> float:
    """
    Estima el coste del combustible para el vuelo.

    Args:
        flight: objeto Flight.
        airplane: objeto Airplane.
        fuel_cost_per_liter: coste del combustible en moneda/litro.

    Returns:
        Coste total estimado del combustible.
    """
    fuel_consumption = estimate_fuel_consumption(flight, airplane)
    return fuel_consumption * fuel_cost_per_liter


def estimate_co2_emissions(flight: Flight, airplane: Airplane) -> float:
    """
    Estima las emisiones de CO2 en kilogramos para el vuelo.

    Args:
        flight: objeto Flight.
        airplane: objeto Airplane.

    Returns:
        Emisiones de CO2 en kg.
    """
    fuel_consumption = estimate_fuel_consumption(flight, airplane)
    return fuel_consumption * CO2_EMISSION_FACTOR
