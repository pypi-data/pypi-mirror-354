"""
Temperature unit conversions.
"""

# Mapping of unit names to standardized format
TEMPERATURE_UNIT_MAP = {
    "c": "celsius", "celsius": "celsius", "°c": "celsius", "centigrade": "celsius",
    "f": "fahrenheit", "fahrenheit": "fahrenheit", "°f": "fahrenheit",
    "k": "kelvin", "kelvin": "kelvin"
}

# Temperature conversions are special because they don't use simple multiplication factors
# We need to use specific formulas for each conversion

def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def fahrenheit_to_kelvin(fahrenheit):
    """Convert Fahrenheit to Kelvin."""
    return (fahrenheit - 32) * 5/9 + 273.15

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit."""
    return (kelvin - 273.15) * 9/5 + 32

def convert_temperature(value, from_unit, to_unit):
    """Convert a value from one temperature unit to another."""
    # Normalize units
    from_unit = TEMPERATURE_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = TEMPERATURE_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Perform the appropriate conversion
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return celsius_to_fahrenheit(value)
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return fahrenheit_to_celsius(value)
    elif from_unit == "celsius" and to_unit == "kelvin":
        return celsius_to_kelvin(value)
    elif from_unit == "kelvin" and to_unit == "celsius":
        return kelvin_to_celsius(value)
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return fahrenheit_to_kelvin(value)
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        return kelvin_to_fahrenheit(value)
    
    return None  # Conversion not supported
TEMPERATURE_UNIT_MAP = {
    "c": "celsius", "celsius": "celsius", "°c": "celsius", "centigrade": "celsius",
    "f": "fahrenheit", "fahrenheit": "fahrenheit", "°f": "fahrenheit",
    "k": "kelvin", "kelvin": "kelvin"
}

def convert_temperature(value, from_unit, to_unit):
    """Convert a value from one temperature unit to another."""
    # Normalize units
    from_unit = TEMPERATURE_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = TEMPERATURE_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Perform the appropriate conversion
    if from_unit == "celsius" and to_unit == "fahrenheit":
        return celsius_to_fahrenheit(value)
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        return fahrenheit_to_celsius(value)
    elif from_unit == "celsius" and to_unit == "kelvin":
        return celsius_to_kelvin(value)
    elif from_unit == "kelvin" and to_unit == "celsius":
        return kelvin_to_celsius(value)
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        return fahrenheit_to_kelvin(value)
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        return kelvin_to_fahrenheit(value)
    
    return None  # Conversion not supported
