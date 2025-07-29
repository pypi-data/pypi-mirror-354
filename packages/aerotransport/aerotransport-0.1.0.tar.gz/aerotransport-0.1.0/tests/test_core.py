import pytest

from aerotransport import (
    AerotransportError,
    Airplane,
    Airport,
    Flight,
    estimate_co2_emissions,
    estimate_flight_cost,
    estimate_flight_time,
    estimate_fuel_consumption,
)


def test_estimate_flight_time():
    airplane = Airplane("A320", cruise_speed=800, fuel_burn_rate=2200)
    origin = Airport("MAD", latitude=40.472, longitude=-3.561)
    dest = Airport("BCN", latitude=41.297, longitude=2.083)
    flight = Flight(origin, dest)
    tiempo = estimate_flight_time(flight, airplane)
    assert abs(tiempo - (flight.distance_km / 800)) < 0.01


def test_estimate_fuel_consumption():
    airplane = Airplane("A320", cruise_speed=800, fuel_burn_rate=2200)
    origin = Airport("MAD", latitude=40.472, longitude=-3.561)
    dest = Airport("BCN", latitude=41.297, longitude=2.083)
    flight = Flight(origin, dest)
    consumo = estimate_fuel_consumption(flight, airplane)
    tiempo = estimate_flight_time(flight, airplane)
    assert abs(consumo - (tiempo * 2200)) < 0.01


def test_estimate_flight_cost():
    airplane = Airplane("A320", cruise_speed=800, fuel_burn_rate=2200)
    origin = Airport("MAD", latitude=40.472, longitude=-3.561)
    dest = Airport("BCN", latitude=41.297, longitude=2.083)
    flight = Flight(origin, dest)
    consumo = estimate_fuel_consumption(flight, airplane)
    coste = estimate_flight_cost(flight, airplane, fuel_cost_per_liter=1.5)
    assert abs(coste - (consumo * 1.5)) < 0.01


def test_estimate_co2_emissions():
    airplane = Airplane("A320", cruise_speed=800, fuel_burn_rate=2200)
    origin = Airport("MAD", latitude=40.472, longitude=-3.561)
    dest = Airport("BCN", latitude=41.297, longitude=2.083)
    flight = Flight(origin, dest)
    consumo = estimate_fuel_consumption(flight, airplane)
    emisiones = estimate_co2_emissions(flight, airplane)
    assert abs(emisiones - (consumo * 3.16)) < 0.1  # 3.16 es el factor por defecto


def test_invalid_speed():
    airplane = Airplane("A320", cruise_speed=0, fuel_burn_rate=2200)
    origin = Airport("MAD", latitude=40.472, longitude=-3.561)
    dest = Airport("BCN", latitude=41.297, longitude=2.083)
    flight = Flight(origin, dest)
    with pytest.raises(AerotransportError):
        estimate_flight_time(flight, airplane)
