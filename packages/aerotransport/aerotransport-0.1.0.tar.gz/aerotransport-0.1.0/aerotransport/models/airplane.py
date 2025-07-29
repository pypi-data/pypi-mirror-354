class Airplane:
    """
    Representa un avión con características básicas.
    """

    def __init__(
        self,
        model: str,
        cruise_speed: float,
        fuel_burn_rate: float,
        max_range_km: float = None,
        fuel_burn_climb: float = None,
        fuel_burn_cruise: float = None,
        fuel_burn_descent: float = None,
        cruise_altitude_ft: int = None,
    ):
        """
        Args:
            model (str): Modelo del avión.
            cruise_speed (float): Velocidad de crucero en km/h.
            fuel_burn_rate (float): Consumo en litros/hora.
            max_range_km (float, opcional): Rango máximo de vuelo en kilómetros.
            fuel_burn_climb (float, opcional): Consumo en litros/h durante el ascenso.
            fuel_burn_cruise (float, opcional): Consumo en litros/h durante el crucero.
            fuel_burn_descent (float, opcional): Consumo en litros/h durante el descenso.
            cruise_altitude_ft (int, opcional): Altitud de crucero estándar en pies.
        """
        self.model = model
        self.cruise_speed = cruise_speed
        self.fuel_burn_rate = fuel_burn_rate
        self.max_range_km = max_range_km
        self.fuel_burn_climb = fuel_burn_climb
        self.fuel_burn_cruise = fuel_burn_cruise
        self.fuel_burn_descent = fuel_burn_descent
        self.cruise_altitude_ft = cruise_altitude_ft

    def __repr__(self):
        return (
            f"<Airplane model={self.model} cruise_speed={self.cruise_speed} km/h "
            f"fuel_burn_rate={self.fuel_burn_rate} L/h max_range={self.max_range_km} km "
            f"cruise_altitude={self.cruise_altitude_ft} ft>"
        )
