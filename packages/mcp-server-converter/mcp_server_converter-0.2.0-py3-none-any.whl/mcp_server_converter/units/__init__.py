"""
Unit conversion modules for the MCP server converter.
"""

from .length import convert_length, LENGTH_UNIT_MAP
from .frequency import convert_frequency, FREQUENCY_UNIT_MAP
from .area import convert_area, AREA_UNIT_MAP
from .volume import convert_volume, VOLUME_UNIT_MAP
from .mass import convert_mass, MASS_UNIT_MAP
from .temperature import convert_temperature, TEMPERATURE_UNIT_MAP
from .energy import convert_energy, ENERGY_UNIT_MAP
from .power import convert_power, POWER_UNIT_MAP
from .pressure import convert_pressure, PRESSURE_UNIT_MAP
from .speed import convert_speed, SPEED_UNIT_MAP
from .time import convert_time, TIME_UNIT_MAP
from .digital_storage import convert_digital_storage, DIGITAL_STORAGE_UNIT_MAP
from .fuel_economy import convert_fuel_economy, FUEL_ECONOMY_UNIT_MAP
from .data_transfer import convert_data_transfer, DATA_TRANSFER_UNIT_MAP

# Combine all unit maps for quick lookup
ALL_UNIT_MAP = {}
ALL_UNIT_MAP.update(LENGTH_UNIT_MAP)
ALL_UNIT_MAP.update(FREQUENCY_UNIT_MAP)
ALL_UNIT_MAP.update(AREA_UNIT_MAP)
ALL_UNIT_MAP.update(VOLUME_UNIT_MAP)
ALL_UNIT_MAP.update(MASS_UNIT_MAP)
ALL_UNIT_MAP.update(TEMPERATURE_UNIT_MAP)
ALL_UNIT_MAP.update(ENERGY_UNIT_MAP)
ALL_UNIT_MAP.update(POWER_UNIT_MAP)
ALL_UNIT_MAP.update(PRESSURE_UNIT_MAP)
ALL_UNIT_MAP.update(SPEED_UNIT_MAP)
ALL_UNIT_MAP.update(TIME_UNIT_MAP)
ALL_UNIT_MAP.update(DIGITAL_STORAGE_UNIT_MAP)
ALL_UNIT_MAP.update(FUEL_ECONOMY_UNIT_MAP)
ALL_UNIT_MAP.update(DATA_TRANSFER_UNIT_MAP)

# Dictionary mapping conversion functions to their categories
CONVERSION_FUNCTIONS = {
    "length": convert_length,
    "frequency": convert_frequency,
    "area": convert_area,
    "volume": convert_volume,
    "mass": convert_mass,
    "temperature": convert_temperature,
    "energy": convert_energy,
    "power": convert_power,
    "pressure": convert_pressure,
    "speed": convert_speed,
    "time": convert_time,
    "digital_storage": convert_digital_storage,
    "fuel_economy": convert_fuel_economy,
    "data_transfer": convert_data_transfer
}
