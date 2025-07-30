"""
Pressure unit conversions.
"""

PRESSURE_CONVERSIONS = {
    # Base unit: pascal (Pa)
    "pa_to_kpa": 0.001,          # pascals to kilopascals
    "kpa_to_pa": 1000,           # kilopascals to pascals
    "pa_to_mpa": 0.000001,       # pascals to megapascals
    "mpa_to_pa": 1000000,        # megapascals to pascals
    "pa_to_bar": 0.00001,        # pascals to bars
    "bar_to_pa": 100000,         # bars to pascals
    "pa_to_atm": 9.86923e-6,     # pascals to atmospheres
    "atm_to_pa": 101325,         # atmospheres to pascals
    "pa_to_psi": 0.000145038,    # pascals to pounds per square inch
    "psi_to_pa": 6894.76,        # pounds per square inch to pascals
    "pa_to_mmhg": 0.00750062,    # pascals to millimeters of mercury (torr)
    "mmhg_to_pa": 133.322,       # millimeters of mercury (torr) to pascals
    "pa_to_inhg": 0.0002953,     # pascals to inches of mercury
    "inhg_to_pa": 3386.39,       # inches of mercury to pascals
    "bar_to_psi": 14.5038,       # bars to pounds per square inch
    "psi_to_bar": 0.0689476,     # pounds per square inch to bars
    "atm_to_bar": 1.01325,       # atmospheres to bars
    "bar_to_atm": 0.986923,      # bars to atmospheres
    "mmhg_to_inhg": 0.0393701,   # millimeters of mercury to inches of mercury
    "inhg_to_mmhg": 25.4,        # inches of mercury to millimeters of mercury
}

# Mapping of unit names to standardized format
PRESSURE_UNIT_MAP = {
    "pa": "pa", "pascal": "pa", "pascals": "pa",
    "kpa": "kpa", "kilopascal": "kpa", "kilopascals": "kpa",
    "mpa": "mpa", "megapascal": "mpa", "megapascals": "mpa",
    "bar": "bar", "bars": "bar",
    "atm": "atm", "atmosphere": "atm", "atmospheres": "atm",
    "psi": "psi", "pound per square inch": "psi", "pounds per square inch": "psi",
    "mmhg": "mmhg", "torr": "mmhg", "mm hg": "mmhg", "millimeters of mercury": "mmhg",
    "inhg": "inhg", "in hg": "inhg", "inches of mercury": "inhg"
}

def convert_pressure(value, from_unit, to_unit):
    """Convert a value from one pressure unit to another."""
    # Normalize units
    from_unit = PRESSURE_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = PRESSURE_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in PRESSURE_CONVERSIONS:
        return value * PRESSURE_CONVERSIONS[conversion_key]
    
    # Two-step conversion through pascals as base unit
    pressure_units = ["pa", "kpa", "mpa", "bar", "atm", "psi", "mmhg", "inhg"]
    if from_unit in pressure_units and to_unit in pressure_units:
        # Convert to pascals first if not already in pascals
        if from_unit != "pa":
            value = value * PRESSURE_CONVERSIONS.get(f"{from_unit}_to_pa", 
                      1 / PRESSURE_CONVERSIONS[f"pa_to_{from_unit}"] if f"pa_to_{from_unit}" in PRESSURE_CONVERSIONS else None)
        
        # Then convert from pascals to target unit
        if to_unit != "pa":
            value = value * PRESSURE_CONVERSIONS.get(f"pa_to_{to_unit}", 
                      1 / PRESSURE_CONVERSIONS[f"{to_unit}_to_pa"] if f"{to_unit}_to_pa" in PRESSURE_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
