# Aerotransport

![PyPI](https://img.shields.io/pypi/v/aerotransport?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dm/aerotransport?style=flat-square)
![License](https://img.shields.io/pypi/l/aerotransport?style=flat-square)
![Python Version](https://img.shields.io/pypi/pyversions/aerotransport?style=flat-square)

Aerotransport es una librería Python para estimar tiempos de vuelo, consumos de combustible, costes y emisiones de CO₂ entre aeropuertos. Incluye utilidades para cálculos geográficos y conversión de unidades, ideal para proyectos de aviación, logística y simulación.

---

## Características

- **Estimación de tiempos de vuelo** entre aeropuertos.
- **Cálculo de consumo de combustible** según el avión y la ruta.
- **Estimación de costes de vuelo** en función del precio del combustible.
- **Cálculo de emisiones de CO₂**.
- **Conversión entre millas náuticas y kilómetros**.
- **Cálculo de distancias geográficas** usando Geopy o Haversine.
- **Fácil de extender y personalizar**.

---

## Instalación

Desde PyPI (cuando esté publicado):

```bash
pip install aerotransport
```

O desde el repositorio:

```bash
git clone https://github.com/tuusuario/aerotransport.git
cd aerotransport
pip install .
```

---

## Ejemplo de uso

```python
from aerotransport import (
    Airplane,
    Airport,
    Flight,
    estimate_flight_time,
    estimate_fuel_consumption,
    estimate_flight_cost,
    estimate_co2_emissions,
)

# Definir aeropuertos
jfk = Airport("JFK", latitude=40.6413, longitude=-73.7781)
lax = Airport("LAX", latitude=33.9416, longitude=-118.4085)

# Definir avión
airplane = Airplane("Boeing 737", cruise_speed=850, fuel_burn_rate=2500)

# Crear vuelo
flight = Flight(jfk, lax)

# Cálculos
tiempo = estimate_flight_time(flight, airplane)
consumo = estimate_fuel_consumption(flight, airplane)
coste = estimate_flight_cost(flight, airplane, fuel_cost_per_liter=0.85)
emisiones = estimate_co2_emissions(flight, airplane)

print(f"Tiempo estimado: {tiempo:.2f} horas")
print(f"Consumo estimado: {consumo:.2f} litros")
print(f"Coste estimado: €{coste:.2f}")
print(f"Emisiones CO2 estimadas: {emisiones:.2f} kg")
```

---

## Documentación

- [Guía de instalación](docs/index.md)
- [Clases principales](docs/classes.md)
- [Funciones principales](docs/functions.md)
- [Ejemplos avanzados](docs/advanced.md)
- [Cómo contribuir](docs/contributing.md)

---

## Requisitos

- Python 3.7 o superior
- [geopy](https://pypi.org/project/geopy/)

Las dependencias se instalan automáticamente con `pip install .` o desde PyPI.

---

## Tests

Para ejecutar los tests:

```bash
pytest
```

---

## Contribuir

¡Las contribuciones son bienvenidas! Por favor, revisa [CONTRIBUTING.md](docs/contributing.md) para más detalles.

1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad.
3. Haz tus cambios y añade tests.
4. Haz un pull request.

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## Autor

Álvaro Fernández Villar
[alvarofv.ing.aeronautico@gmail.com](mailto:alvarofv.ing.aeronautico@gmail.com)

---

## Agradecimientos

- [geopy](https://github.com/geopy/geopy) por las utilidades geográficas.
- La comunidad Python por su apoyo y recursos.
