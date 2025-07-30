"""
Energy unit conversions.
"""

ENERGY_CONVERSIONS = {
    # Base unit: joule (J)
    "j_to_kj": 0.001,            # joules to kilojoules
    "kj_to_j": 1000,             # kilojoules to joules
    "j_to_cal": 0.239006,        # joules to calories
    "cal_to_j": 4.184,           # calories to joules
    "j_to_kcal": 0.000239006,    # joules to kilocalories
    "kcal_to_j": 4184,           # kilocalories to joules
    "j_to_wh": 0.000277778,      # joules to watt-hours
    "wh_to_j": 3600,             # watt-hours to joules
    "j_to_kwh": 2.77778e-7,      # joules to kilowatt-hours
    "kwh_to_j": 3600000,         # kilowatt-hours to joules
    "j_to_ev": 6.242e+18,        # joules to electron volts
    "ev_to_j": 1.602e-19,        # electron volts to joules
    "j_to_btu": 0.000947817,     # joules to British Thermal Units
    "btu_to_j": 1055.06,         # British Thermal Units to joules
    "wh_to_kwh": 0.001,          # watt-hours to kilowatt-hours
    "kwh_to_wh": 1000,           # kilowatt-hours to watt-hours
    "cal_to_kcal": 0.001,        # calories to kilocalories
    "kcal_to_cal": 1000,         # kilocalories to calories
}

# Mapping of unit names to standardized format
ENERGY_UNIT_MAP = {
    "j": "j", "joule": "j", "joules": "j",
    "kj": "kj", "kilojoule": "kj", "kilojoules": "kj",
    "cal": "cal", "calorie": "cal", "calories": "cal",
    "kcal": "kcal", "kilocalorie": "kcal", "kilocalories": "kcal",
    "wh": "wh", "watt hour": "wh", "watt hours": "wh", "watt-hour": "wh", "watt-hours": "wh",
    "kwh": "kwh", "kilowatt hour": "kwh", "kilowatt hours": "kwh", "kilowatt-hour": "kwh", "kilowatt-hours": "kwh",
    "ev": "ev", "electron volt": "ev", "electron volts": "ev",
    "btu": "btu", "british thermal unit": "btu", "british thermal units": "btu"
}

def convert_energy(value, from_unit, to_unit):
    """Convert a value from one energy unit to another."""
    # Normalize units
    from_unit = ENERGY_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = ENERGY_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in ENERGY_CONVERSIONS:
        return value * ENERGY_CONVERSIONS[conversion_key]
    
    # Two-step conversion through joules as base unit
    energy_units = ["j", "kj", "cal", "kcal", "wh", "kwh", "ev", "btu"]
    if from_unit in energy_units and to_unit in energy_units:
        # Convert to joules first if not already in joules
        if from_unit != "j":
            value = value * ENERGY_CONVERSIONS.get(f"{from_unit}_to_j", 
                      1 / ENERGY_CONVERSIONS[f"j_to_{from_unit}"] if f"j_to_{from_unit}" in ENERGY_CONVERSIONS else None)
        
        # Then convert from joules to target unit
        if to_unit != "j":
            value = value * ENERGY_CONVERSIONS.get(f"j_to_{to_unit}", 
                      1 / ENERGY_CONVERSIONS[f"{to_unit}_to_j"] if f"{to_unit}_to_j" in ENERGY_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
