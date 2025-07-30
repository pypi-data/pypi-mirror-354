"""
Volume unit conversions.
"""

VOLUME_CONVERSIONS = {
    # Base unit: cubic meter (m³)
    "m3_to_cm3": 1000000,         # cubic meters to cubic centimeters
    "cm3_to_m3": 0.000001,        # cubic centimeters to cubic meters
    "m3_to_l": 1000,              # cubic meters to liters
    "l_to_m3": 0.001,             # liters to cubic meters
    "m3_to_ml": 1000000,          # cubic meters to milliliters
    "ml_to_m3": 0.000001,         # milliliters to cubic meters
    "l_to_ml": 1000,              # liters to milliliters
    "ml_to_l": 0.001,             # milliliters to liters
    "m3_to_gal": 264.172,         # cubic meters to gallons (US)
    "gal_to_m3": 0.00378541,      # gallons (US) to cubic meters
    "l_to_gal": 0.264172,         # liters to gallons (US)
    "gal_to_l": 3.78541,          # gallons (US) to liters
    "gal_to_qt": 4,               # gallons to quarts
    "qt_to_gal": 0.25,            # quarts to gallons
    "qt_to_pt": 2,                # quarts to pints
    "pt_to_qt": 0.5,              # pints to quarts
    "pt_to_cup": 2,               # pints to cups
    "cup_to_pt": 0.5,             # cups to pints
    "cup_to_floz": 8,             # cups to fluid ounces
    "floz_to_cup": 0.125,         # fluid ounces to cups
    "m3_to_ft3": 35.3147,         # cubic meters to cubic feet
    "ft3_to_m3": 0.0283168,       # cubic feet to cubic meters
    "cm3_to_ml": 1,               # cubic centimeters to milliliters (they are the same)
    "ml_to_cm3": 1,               # milliliters to cubic centimeters (they are the same)
    "in3_to_cm3": 16.3871,        # cubic inches to cubic centimeters
    "cm3_to_in3": 0.0610237,      # cubic centimeters to cubic inches
    "ft3_to_in3": 1728,           # cubic feet to cubic inches
    "in3_to_ft3": 0.000578704,    # cubic inches to cubic feet
    "gal_to_floz": 128,           # gallons to fluid ounces
    "floz_to_gal": 0.0078125,     # fluid ounces to gallons
}

# Mapping of unit names to standardized format
VOLUME_UNIT_MAP = {
    "m3": "m3", "cubic meter": "m3", "cubic meters": "m3",
    "cm3": "cm3", "cubic centimeter": "cm3", "cubic centimeters": "cm3", "cc": "cm3",
    "l": "l", "liter": "l", "liters": "l",
    "ml": "ml", "milliliter": "ml", "milliliters": "ml",
    "gal": "gal", "gallon": "gal", "gallons": "gal", 
    "qt": "qt", "quart": "qt", "quarts": "qt",
    "pt": "pt", "pint": "pt", "pints": "pt",
    "cup": "cup", "cups": "cup",
    "floz": "floz", "fluid ounce": "floz", "fluid ounces": "floz", "fl oz": "floz",
    "ft3": "ft3", "cubic foot": "ft3", "cubic feet": "ft3",
    "in3": "in3", "cubic inch": "in3", "cubic inches": "in3"
}

def convert_volume(value, from_unit, to_unit):
    """Convert a value from one volume unit to another."""
    # Normalize units
    from_unit = VOLUME_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = VOLUME_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in VOLUME_CONVERSIONS:
        return value * VOLUME_CONVERSIONS[conversion_key]
    
    # Two-step conversion through cubic meters as base unit
    volume_units = ["m3", "cm3", "l", "ml", "gal", "qt", "pt", "cup", "floz", "ft3", "in3"]
    if from_unit in volume_units and to_unit in volume_units:
        # For units like qt, pt, cup, floz, we'll first convert to gallons, then to cubic meters
        intermediary_unit = "m3"
        
        # Handle special cases using gallons as an intermediate step
        if from_unit in ["qt", "pt", "cup", "floz"] and to_unit not in ["qt", "pt", "cup", "floz"]:
            # First convert to gallons
            if from_unit == "qt":
                value = value * VOLUME_CONVERSIONS["qt_to_gal"]
            elif from_unit == "pt":
                value = value * VOLUME_CONVERSIONS["pt_to_qt"] * VOLUME_CONVERSIONS["qt_to_gal"]
            elif from_unit == "cup":
                value = value * VOLUME_CONVERSIONS["cup_to_pt"] * VOLUME_CONVERSIONS["pt_to_qt"] * VOLUME_CONVERSIONS["qt_to_gal"]
            elif from_unit == "floz":
                value = value * VOLUME_CONVERSIONS["floz_to_cup"] * VOLUME_CONVERSIONS["cup_to_pt"] * VOLUME_CONVERSIONS["pt_to_qt"] * VOLUME_CONVERSIONS["qt_to_gal"]
            from_unit = "gal"
        
        # Convert to cubic meters if not already in cubic meters
        if from_unit != "m3":
            value = value * VOLUME_CONVERSIONS.get(f"{from_unit}_to_m3", 
                      1 / VOLUME_CONVERSIONS[f"m3_to_{from_unit}"] if f"m3_to_{from_unit}" in VOLUME_CONVERSIONS else None)
        
        # Handle special cases for units like qt, pt, cup, floz
        if to_unit in ["qt", "pt", "cup", "floz"] and from_unit not in ["qt", "pt", "cup", "floz"]:
            # First convert to gallons
            if from_unit != "gal":
                value = value * VOLUME_CONVERSIONS["m3_to_gal"]
            
            # Then convert from gallons to the target unit
            if to_unit == "qt":
                value = value * VOLUME_CONVERSIONS["gal_to_qt"]
            elif to_unit == "pt":
                value = value * VOLUME_CONVERSIONS["gal_to_qt"] * VOLUME_CONVERSIONS["qt_to_pt"]
            elif to_unit == "cup":
                value = value * VOLUME_CONVERSIONS["gal_to_qt"] * VOLUME_CONVERSIONS["qt_to_pt"] * VOLUME_CONVERSIONS["pt_to_cup"]
            elif to_unit == "floz":
                value = value * VOLUME_CONVERSIONS["gal_to_qt"] * VOLUME_CONVERSIONS["qt_to_pt"] * VOLUME_CONVERSIONS["pt_to_cup"] * VOLUME_CONVERSIONS["cup_to_floz"]
            return value
        
        # Then convert from cubic meters to target unit
        if to_unit != "m3":
            value = value * VOLUME_CONVERSIONS.get(f"m3_to_{to_unit}", 
                      1 / VOLUME_CONVERSIONS[f"{to_unit}_to_m3"] if f"{to_unit}_to_m3" in VOLUME_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
