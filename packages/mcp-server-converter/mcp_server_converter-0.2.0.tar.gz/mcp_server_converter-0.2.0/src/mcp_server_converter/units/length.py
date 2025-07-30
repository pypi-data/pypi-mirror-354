"""
Length unit conversions.
"""

LENGTH_CONVERSIONS = {
    # Base unit: meter
    "m_to_km": 0.001,    # meters to kilometers
    "km_to_m": 1000,     # kilometers to meters
    "inch_to_cm": 2.54,  # inches to centimeters
    "cm_to_inch": 0.3937,# centimeters to inches
    "ft_to_m": 0.3048,   # feet to meters
    "m_to_ft": 3.28084,  # meters to feet
    "mile_to_km": 1.60934, # miles to kilometers
    "km_to_mile": 0.621371, # kilometers to miles
    "m_to_inch": 39.3701, # meters to inches
    "inch_to_m": 0.0254,  # inches to meters
    "m_to_cm": 100,      # meters to centimeters
    "cm_to_m": 0.01,     # centimeters to meters
    "ft_to_mile": 0.000189394, # feet to miles (1 mile = 5280 feet)
    "mile_to_ft": 5280,   # miles to feet
}

# Mapping of unit names to standardized format
LENGTH_UNIT_MAP = {
    "m": "m", "meter": "m", "meters": "m",
    "km": "km", "kilometer": "km", "kilometers": "km",
    "cm": "cm", "centimeter": "cm", "centimeters": "cm", 
    "in": "inch", "inch": "inch", "inches": "inch",
    "ft": "ft", "foot": "ft", "feet": "ft",
    "mi": "mile", "mile": "mile", "miles": "mile"
}

def convert_length(value, from_unit, to_unit):
    """Convert a value from one length unit to another."""
    # Normalize units
    from_unit = LENGTH_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = LENGTH_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in LENGTH_CONVERSIONS:
        return value * LENGTH_CONVERSIONS[conversion_key]
    
    # Two-step conversion through meters as base unit
    if from_unit in ["m", "km", "ft", "mile", "inch", "cm"] and to_unit in ["m", "km", "ft", "mile", "inch", "cm"]:
        # Convert to meters first if not already in meters
        if from_unit != "m":
            value = value * LENGTH_CONVERSIONS.get(f"{from_unit}_to_m", 
                      1 / LENGTH_CONVERSIONS[f"m_to_{from_unit}"] if f"m_to_{from_unit}" in LENGTH_CONVERSIONS else None)
        
        # Then convert from meters to target unit
        if to_unit != "m":
            value = value * LENGTH_CONVERSIONS.get(f"m_to_{to_unit}", 
                      1 / LENGTH_CONVERSIONS[f"{to_unit}_to_m"] if f"{to_unit}_to_m" in LENGTH_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
