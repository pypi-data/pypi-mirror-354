class Airport:
    """
    Representa un aeropuerto con código IATA y coordenadas.
    """

    def __init__(self, iata_code: str, latitude: float, longitude: float):
        self.iata_code = iata_code
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"<Airport {self.iata_code} ({self.latitude}, {self.longitude})>"
