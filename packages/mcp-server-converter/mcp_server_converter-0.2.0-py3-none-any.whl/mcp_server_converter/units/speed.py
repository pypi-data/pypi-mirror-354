"""
Speed unit conversions.
"""

SPEED_CONVERSIONS = {
    # Base unit: meters per second (m/s)
    "m/s_to_km/h": 3.6,            # meters per second to kilometers per hour
    "km/h_to_m/s": 0.277778,       # kilometers per hour to meters per second
    "m/s_to_mph": 2.23694,         # meters per second to miles per hour
    "mph_to_m/s": 0.44704,         # miles per hour to meters per second
    "m/s_to_ft/s": 3.28084,        # meters per second to feet per second
    "ft/s_to_m/s": 0.3048,         # feet per second to meters per second
    "m/s_to_knot": 1.94384,        # meters per second to knots
    "knot_to_m/s": 0.514444,       # knots to meters per second
    "km/h_to_mph": 0.621371,       # kilometers per hour to miles per hour
    "mph_to_km/h": 1.60934,        # miles per hour to kilometers per hour
    "km/h_to_knot": 0.539957,      # kilometers per hour to knots
    "knot_to_km/h": 1.852,         # knots to kilometers per hour
    "mph_to_ft/s": 1.46667,        # miles per hour to feet per second
    "ft/s_to_mph": 0.681818,       # feet per second to miles per hour
    "mph_to_knot": 0.868976,       # miles per hour to knots
    "knot_to_mph": 1.15078,        # knots to miles per hour
}

# Mapping of unit names to standardized format
SPEED_UNIT_MAP = {
    "m/s": "m/s", "meter per second": "m/s", "meters per second": "m/s", "meter/second": "m/s", "meters/second": "m/s",
    "km/h": "km/h", "kilometer per hour": "km/h", "kilometers per hour": "km/h", "kmh": "km/h", "kph": "km/h",
    "mph": "mph", "mile per hour": "mph", "miles per hour": "mph", 
    "ft/s": "ft/s", "foot per second": "ft/s", "feet per second": "ft/s", "fps": "ft/s",
    "knot": "knot", "knots": "knot", "kt": "knot", "kn": "knot"
}

def convert_speed(value, from_unit, to_unit):
    """Convert a value from one speed unit to another."""
    # Normalize units
    from_unit = SPEED_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = SPEED_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in SPEED_CONVERSIONS:
        return value * SPEED_CONVERSIONS[conversion_key]
    
    # Two-step conversion through meters per second as base unit
    speed_units = ["m/s", "km/h", "mph", "ft/s", "knot"]
    if from_unit in speed_units and to_unit in speed_units:
        # Convert to meters per second first if not already in meters per second
        if from_unit != "m/s":
            value = value * SPEED_CONVERSIONS.get(f"{from_unit}_to_m/s", 
                      1 / SPEED_CONVERSIONS[f"m/s_to_{from_unit}"] if f"m/s_to_{from_unit}" in SPEED_CONVERSIONS else None)
        
        # Then convert from meters per second to target unit
        if to_unit != "m/s":
            value = value * SPEED_CONVERSIONS.get(f"m/s_to_{to_unit}", 
                      1 / SPEED_CONVERSIONS[f"{to_unit}_to_m/s"] if f"{to_unit}_to_m/s" in SPEED_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
