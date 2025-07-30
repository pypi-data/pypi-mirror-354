"""
Frequency unit conversions.
"""

FREQUENCY_CONVERSIONS = {
    # Base unit: hertz
    "hz_to_khz": 0.001,       # hertz to kilohertz
    "khz_to_hz": 1000,        # kilohertz to hertz
    "hz_to_mhz": 0.000001,    # hertz to megahertz
    "mhz_to_hz": 1000000,     # megahertz to hertz
    "hz_to_ghz": 0.000000001, # hertz to gigahertz
    "ghz_to_hz": 1000000000,  # gigahertz to hertz
    "khz_to_mhz": 0.001,      # kilohertz to megahertz
    "mhz_to_khz": 1000,       # megahertz to kilohertz
    "khz_to_ghz": 0.000001,   # kilohertz to gigahertz
    "ghz_to_khz": 1000000,    # gigahertz to kilohertz
    "mhz_to_ghz": 0.001,      # megahertz to gigahertz
    "ghz_to_mhz": 1000,       # gigahertz to megahertz
}

# Mapping of unit names to standardized format
FREQUENCY_UNIT_MAP = {
    "hz": "hz", "hertz": "hz",
    "khz": "khz", "kilohertz": "khz",
    "mhz": "mhz", "megahertz": "mhz",
    "ghz": "ghz", "gigahertz": "ghz"
}

def convert_frequency(value, from_unit, to_unit):
    """Convert a value from one frequency unit to another."""
    # Normalize units
    from_unit = FREQUENCY_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = FREQUENCY_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in FREQUENCY_CONVERSIONS:
        return value * FREQUENCY_CONVERSIONS[conversion_key]
    
    # Two-step conversion through hertz as base unit
    frequency_units = ["hz", "khz", "mhz", "ghz"]
    if from_unit in frequency_units and to_unit in frequency_units:
        # Convert to hertz first if not already in hertz
        if from_unit != "hz":
            value = value * FREQUENCY_CONVERSIONS[f"{from_unit}_to_hz"]
        
        # Then convert from hertz to target unit
        if to_unit != "hz":
            value = value * FREQUENCY_CONVERSIONS[f"hz_to_{to_unit}"]
            
        return value
    
    return None  # Conversion not supported
