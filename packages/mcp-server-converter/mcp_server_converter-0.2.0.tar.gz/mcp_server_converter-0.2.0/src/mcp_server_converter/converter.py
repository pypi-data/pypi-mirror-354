import re
from mcp.server.fastmcp import FastMCP

# Import all unit conversion modules and unified unit map
from mcp_server_converter.units import (
    CONVERSION_FUNCTIONS,
    ALL_UNIT_MAP
)

def evaluate(expression: str) -> str:
    """
    Convert units based on the given expression.
    Expected formats: 
    - "value from_unit to_unit" (e.g., "5.2 m km")
    - "value from_unit to to_unit" (e.g., "5.2 m to km")
    """
    # Clean up the expression
    expression = expression.strip().lower()
    
    # Remove the word "to" if present in the format "unit to unit"
    expression = re.sub(r'\s+to\s+', ' ', expression)
    
    # Try to match the pattern: number unit1 unit2
    # Updated pattern to match units with possible slash (like km/h) or other special characters
    pattern = r"^([-+]?\d*\.?\d+)\s+([a-zA-Z0-9/°]+)\s+([a-zA-Z0-9/°]+)$"
    match = re.match(pattern, expression)
    
    if not match:
        return "Error: Invalid format. Please use 'value from_unit to_unit' (e.g., '5 m km' or '5 m to km')"
    
    value_str, from_unit, to_unit = match.groups()
    try:
        value = float(value_str)
    except ValueError:
        return f"Error: Invalid number format '{value_str}'"
    
    # Normalize units using the combined unit map
    from_unit = ALL_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = ALL_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # Try all conversion functions
    for category, convert_func in CONVERSION_FUNCTIONS.items():
        result = convert_func(value, from_unit, to_unit)
        if result is not None:
            return f"{result:.6g}"
    
    return f"Error: Cannot convert from '{from_unit}' to '{to_unit}'."

mcp = FastMCP("converter")

@mcp.tool()
async def convert(expression: str) -> str:
    """Converts between different units (length, area, volume, mass, temperature, etc.)."""
    return evaluate(expression)

def main():
    mcp.run()
