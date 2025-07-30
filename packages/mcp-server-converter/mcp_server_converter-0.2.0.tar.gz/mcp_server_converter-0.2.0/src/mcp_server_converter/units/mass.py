"""
Weight/Mass unit conversions.
"""

MASS_CONVERSIONS = {
    # Base unit: kilogram (kg)
    "kg_to_g": 1000,              # kilograms to grams
    "g_to_kg": 0.001,             # grams to kilograms
    "kg_to_mg": 1000000,          # kilograms to milligrams
    "mg_to_kg": 0.000001,         # milligrams to kilograms
    "g_to_mg": 1000,              # grams to milligrams
    "mg_to_g": 0.001,             # milligrams to grams
    "kg_to_lb": 2.20462,          # kilograms to pounds
    "lb_to_kg": 0.453592,         # pounds to kilograms
    "kg_to_oz": 35.274,           # kilograms to ounces
    "oz_to_kg": 0.0283495,        # ounces to kilograms
    "lb_to_oz": 16,               # pounds to ounces
    "oz_to_lb": 0.0625,           # ounces to pounds
    "kg_to_t": 0.001,             # kilograms to metric tons
    "t_to_kg": 1000,              # metric tons to kilograms
    "kg_to_st": 0.157473,         # kilograms to stone
    "st_to_kg": 6.35029,          # stone to kilograms
    "lb_to_st": 0.0714286,        # pounds to stone
    "st_to_lb": 14,               # stone to pounds
}

# Mapping of unit names to standardized format
MASS_UNIT_MAP = {
    "kg": "kg", "kilogram": "kg", "kilograms": "kg",
    "g": "g", "gram": "g", "grams": "g",
    "mg": "mg", "milligram": "mg", "milligrams": "mg",
    "lb": "lb", "pound": "lb", "pounds": "lb", "lbs": "lb",
    "oz": "oz", "ounce": "oz", "ounces": "oz",
    "t": "t", "tonne": "t", "tonnes": "t", "metric ton": "t", "metric tons": "t",
    "st": "st", "stone": "st", "stones": "st"
}

def convert_mass(value, from_unit, to_unit):
    """Convert a value from one mass/weight unit to another."""
    # Normalize units
    from_unit = MASS_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = MASS_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in MASS_CONVERSIONS:
        return value * MASS_CONVERSIONS[conversion_key]
    
    # Two-step conversion through kilograms as base unit
    mass_units = ["kg", "g", "mg", "lb", "oz", "t", "st"]
    if from_unit in mass_units and to_unit in mass_units:
        # Convert to kilograms first if not already in kilograms
        if from_unit != "kg":
            value = value * MASS_CONVERSIONS.get(f"{from_unit}_to_kg", 
                      1 / MASS_CONVERSIONS[f"kg_to_{from_unit}"] if f"kg_to_{from_unit}" in MASS_CONVERSIONS else None)
        
        # Then convert from kilograms to target unit
        if to_unit != "kg":
            value = value * MASS_CONVERSIONS.get(f"kg_to_{to_unit}", 
                      1 / MASS_CONVERSIONS[f"{to_unit}_to_kg"] if f"{to_unit}_to_kg" in MASS_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
