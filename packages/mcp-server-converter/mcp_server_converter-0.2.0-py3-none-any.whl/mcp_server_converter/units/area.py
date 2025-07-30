"""
Area unit conversions.
"""

AREA_CONVERSIONS = {
    # Base unit: square meter (m²)
    "sqm_to_sqkm": 0.000001,      # square meters to square kilometers
    "sqkm_to_sqm": 1000000,       # square kilometers to square meters
    "sqm_to_sqcm": 10000,         # square meters to square centimeters  
    "sqcm_to_sqm": 0.0001,        # square centimeters to square meters
    "sqm_to_sqft": 10.7639,       # square meters to square feet
    "sqft_to_sqm": 0.092903,      # square feet to square meters
    "sqm_to_sqyd": 1.19599,       # square meters to square yards
    "sqyd_to_sqm": 0.836127,      # square yards to square meters
    "sqm_to_acre": 0.000247105,   # square meters to acres
    "acre_to_sqm": 4046.86,       # acres to square meters
    "sqm_to_ha": 0.0001,          # square meters to hectares
    "ha_to_sqm": 10000,           # hectares to square meters
    "sqm_to_sqmi": 3.861e-7,      # square meters to square miles
    "sqmi_to_sqm": 2589988.11,    # square miles to square meters
    "sqft_to_sqin": 144,          # square feet to square inches
    "sqin_to_sqft": 0.00694444,   # square inches to square feet
    "sqyd_to_sqft": 9,            # square yards to square feet
    "sqft_to_sqyd": 0.111111,     # square feet to square yards
    "acre_to_sqft": 43560,        # acres to square feet
    "sqft_to_acre": 2.29568e-5,   # square feet to acres
    "sqmi_to_acre": 640,          # square miles to acres
    "acre_to_sqmi": 0.0015625,    # acres to square miles
}

# Mapping of unit names to standardized format
AREA_UNIT_MAP = {
    "m2": "sqm", "sqm": "sqm", "square meter": "sqm", "square meters": "sqm", "sq m": "sqm",
    "km2": "sqkm", "sqkm": "sqkm", "square kilometer": "sqkm", "square kilometers": "sqkm", "sq km": "sqkm",
    "cm2": "sqcm", "sqcm": "sqcm", "square centimeter": "sqcm", "square centimeters": "sqcm", "sq cm": "sqcm",
    "ft2": "sqft", "sqft": "sqft", "square foot": "sqft", "square feet": "sqft", "sq ft": "sqft",
    "yd2": "sqyd", "sqyd": "sqyd", "square yard": "sqyd", "square yards": "sqyd", "sq yd": "sqyd",
    "in2": "sqin", "sqin": "sqin", "square inch": "sqin", "square inches": "sqin", "sq in": "sqin",
    "mi2": "sqmi", "sqmi": "sqmi", "square mile": "sqmi", "square miles": "sqmi", "sq mi": "sqmi",
    "acre": "acre", "acres": "acre",
    "ha": "ha", "hectare": "ha", "hectares": "ha"
}

def convert_area(value, from_unit, to_unit):
    """Convert a value from one area unit to another."""
    # Normalize units
    from_unit = AREA_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = AREA_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in AREA_CONVERSIONS:
        return value * AREA_CONVERSIONS[conversion_key]
    
    # Two-step conversion through square meters as base unit
    area_units = ["sqm", "sqkm", "sqcm", "sqft", "sqyd", "sqin", "sqmi", "acre", "ha"]
    if from_unit in area_units and to_unit in area_units:
        # Convert to square meters first if not already in square meters
        if from_unit != "sqm":
            value = value * AREA_CONVERSIONS.get(f"{from_unit}_to_sqm", 
                      1 / AREA_CONVERSIONS[f"sqm_to_{from_unit}"] if f"sqm_to_{from_unit}" in AREA_CONVERSIONS else None)
        
        # Then convert from square meters to target unit
        if to_unit != "sqm":
            value = value * AREA_CONVERSIONS.get(f"sqm_to_{to_unit}", 
                      1 / AREA_CONVERSIONS[f"{to_unit}_to_sqm"] if f"{to_unit}_to_sqm" in AREA_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
