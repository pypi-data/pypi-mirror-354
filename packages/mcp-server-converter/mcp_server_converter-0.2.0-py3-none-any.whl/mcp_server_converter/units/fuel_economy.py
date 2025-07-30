"""
Fuel economy unit conversions.
"""

FUEL_ECONOMY_CONVERSIONS = {
    # Base unit: kilometers per liter (km/l)
    "km/l_to_mpg": 2.35215,        # kilometers per liter to miles per gallon (US)
    "mpg_to_km/l": 0.425144,       # miles per gallon (US) to kilometers per liter
    "km/l_to_l/100km": 100,        # kilometers per liter to liters per 100 kilometers (inverse relationship)
    "l/100km_to_km/l": 100,        # liters per 100 kilometers to kilometers per liter (inverse relationship)
    "mpg_to_l/100km": 235.215,     # miles per gallon (US) to liters per 100 kilometers (inverse relationship)
    "l/100km_to_mpg": 235.215,     # liters per 100 kilometers to miles per gallon (US) (inverse relationship)
    "mpg_to_mpgimp": 0.832674,     # miles per gallon (US) to miles per gallon (Imperial)
    "mpgimp_to_mpg": 1.20095,      # miles per gallon (Imperial) to miles per gallon (US)
}

# Special handling for fuel economy since some conversions are inverses
def inverse_conversion(value, factor):
    if value == 0:
        return float('inf')  # Avoid division by zero
    return factor / value

# Mapping of unit names to standardized format
FUEL_ECONOMY_UNIT_MAP = {
    "km/l": "km/l", "kilometer per liter": "km/l", "kilometers per liter": "km/l",
    "mpg": "mpg", "mile per gallon": "mpg", "miles per gallon": "mpg", "mpgus": "mpg",
    "l/100km": "l/100km", "liter per 100 kilometers": "l/100km", "liters per 100 kilometers": "l/100km",
    "mpgimp": "mpgimp", "mile per imperial gallon": "mpgimp", "miles per imperial gallon": "mpgimp"
}

def convert_fuel_economy(value, from_unit, to_unit):
    """Convert a value from one fuel economy unit to another."""
    # Normalize units
    from_unit = FUEL_ECONOMY_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = FUEL_ECONOMY_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Special handling for inverse relationships (l/100km)
    if from_unit == "l/100km" and to_unit == "km/l":
        return inverse_conversion(value, FUEL_ECONOMY_CONVERSIONS["l/100km_to_km/l"])
    
    if from_unit == "km/l" and to_unit == "l/100km":
        return inverse_conversion(value, FUEL_ECONOMY_CONVERSIONS["km/l_to_l/100km"])
    
    if from_unit == "l/100km" and to_unit == "mpg":
        return inverse_conversion(value, FUEL_ECONOMY_CONVERSIONS["l/100km_to_mpg"])
    
    if from_unit == "mpg" and to_unit == "l/100km":
        return inverse_conversion(value, FUEL_ECONOMY_CONVERSIONS["mpg_to_l/100km"])
    
    # Direct conversion for other cases
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in FUEL_ECONOMY_CONVERSIONS:
        return value * FUEL_ECONOMY_CONVERSIONS[conversion_key]
    
    # Two-step conversion through kilometers per liter as base unit
    fuel_economy_units = ["km/l", "mpg", "mpgimp"]
    if from_unit in fuel_economy_units and to_unit in fuel_economy_units:
        # Convert to kilometers per liter first if not already in kilometers per liter
        if from_unit != "km/l":
            value = value * FUEL_ECONOMY_CONVERSIONS.get(f"{from_unit}_to_km/l", 
                      1 / FUEL_ECONOMY_CONVERSIONS[f"km/l_to_{from_unit}"] if f"km/l_to_{from_unit}" in FUEL_ECONOMY_CONVERSIONS else None)
        
        # Then convert from kilometers per liter to target unit
        if to_unit != "km/l":
            value = value * FUEL_ECONOMY_CONVERSIONS.get(f"km/l_to_{to_unit}", 
                      1 / FUEL_ECONOMY_CONVERSIONS[f"{to_unit}_to_km/l"] if f"{to_unit}_to_km/l" in FUEL_ECONOMY_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
