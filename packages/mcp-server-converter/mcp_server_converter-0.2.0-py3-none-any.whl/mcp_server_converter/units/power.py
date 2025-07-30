"""
Power unit conversions.
"""

POWER_CONVERSIONS = {
    # Base unit: watt (W)
    "w_to_kw": 0.001,            # watts to kilowatts
    "kw_to_w": 1000,             # kilowatts to watts
    "w_to_mw": 0.000001,         # watts to megawatts
    "mw_to_w": 1000000,          # megawatts to watts
    "w_to_hp": 0.00134102,       # watts to horsepower (mechanical)
    "hp_to_w": 745.7,            # horsepower (mechanical) to watts
    "kw_to_mw": 0.001,           # kilowatts to megawatts
    "mw_to_kw": 1000,            # megawatts to kilowatts
    "w_to_btu_h": 3.41214,       # watts to BTU per hour
    "btu_h_to_w": 0.293071,      # BTU per hour to watts
    "hp_to_btu_h": 2544.43,      # horsepower to BTU per hour
    "btu_h_to_hp": 0.000393,     # BTU per hour to horsepower
}

# Mapping of unit names to standardized format
POWER_UNIT_MAP = {
    "w": "w", "watt": "w", "watts": "w",
    "kw": "kw", "kilowatt": "kw", "kilowatts": "kw",
    "mw": "mw", "megawatt": "mw", "megawatts": "mw",
    "hp": "hp", "horsepower": "hp",
    "btu/h": "btu_h", "btu/hr": "btu_h", "btu per hour": "btu_h", "btu per hr": "btu_h"
}

def convert_power(value, from_unit, to_unit):
    """Convert a value from one power unit to another."""
    # Normalize units
    from_unit = POWER_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = POWER_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in POWER_CONVERSIONS:
        return value * POWER_CONVERSIONS[conversion_key]
    
    # Two-step conversion through watts as base unit
    power_units = ["w", "kw", "mw", "hp", "btu_h"]
    if from_unit in power_units and to_unit in power_units:
        # Convert to watts first if not already in watts
        if from_unit != "w":
            value = value * POWER_CONVERSIONS.get(f"{from_unit}_to_w", 
                      1 / POWER_CONVERSIONS[f"w_to_{from_unit}"] if f"w_to_{from_unit}" in POWER_CONVERSIONS else None)
        
        # Then convert from watts to target unit
        if to_unit != "w":
            value = value * POWER_CONVERSIONS.get(f"w_to_{to_unit}", 
                      1 / POWER_CONVERSIONS[f"{to_unit}_to_w"] if f"{to_unit}_to_w" in POWER_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
    # Normalize units
    from_unit = POWER_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = POWER_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in POWER_CONVERSIONS:
        return value * POWER_CONVERSIONS[conversion_key]
    
    # Two-step conversion through watts as base unit
    power_units = ["w", "kw", "mw", "hp", "btu_h"]
    if from_unit in power_units and to_unit in power_units:
        # Convert to watts first if not already in watts
        if from_unit != "w":
            value = value * POWER_CONVERSIONS.get(f"{from_unit}_to_w", 
                      1 / POWER_CONVERSIONS[f"w_to_{from_unit}"] if f"w_to_{from_unit}" in POWER_CONVERSIONS else None)
        
        # Then convert from watts to target unit
        if to_unit != "w":
            value = value * POWER_CONVERSIONS.get(f"w_to_{to_unit}", 
                      1 / POWER_CONVERSIONS[f"{to_unit}_to_w"] if f"{to_unit}_to_w" in POWER_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
