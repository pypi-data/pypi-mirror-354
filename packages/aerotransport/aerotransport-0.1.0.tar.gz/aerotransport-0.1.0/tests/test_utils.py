import pytest

from aerotransport.utils import calculate_distance_between_points, km_to_nm, nm_to_km


def test_nm_to_km():
    assert nm_to_km(1) == 1.852
    assert nm_to_km(0) == 0


def test_km_to_nm():
    assert km_to_nm(1.852) == 1
    assert km_to_nm(0) == 0


def test_calculate_distance_between_points_geopy():
    # JFK (40.6413, -73.7781) to LAX (33.9416, -118.4085)
    d = calculate_distance_between_points(
        (40.6413, -73.7781), (33.9416, -118.4085), method="geopy"
    )
    assert 3930 < d < 4010  # Aproximadamente 3974 km


def test_calculate_distance_between_points_haversine():
    d = calculate_distance_between_points((0, 0), (0, 1), method="haversine")
    assert 110 < d < 112  # Aproximadamente 111 km


def test_calculate_distance_between_points_invalid_method():
    with pytest.raises(ValueError):
        calculate_distance_between_points((0, 0), (0, 1), method="invalid")
