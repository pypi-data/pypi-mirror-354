"""
Digital storage unit conversions.
"""

# Using binary prefixes (powers of 2) for storage units
DIGITAL_STORAGE_CONVERSIONS = {
    # Base unit: byte (B)
    "B_to_KB": 0.000976563,       # bytes to kilobytes (2^10)
    "KB_to_B": 1024,              # kilobytes to bytes
    "B_to_MB": 9.53674e-7,        # bytes to megabytes (2^20)
    "MB_to_B": 1048576,           # megabytes to bytes
    "B_to_GB": 9.31323e-10,       # bytes to gigabytes (2^30)
    "GB_to_B": 1073741824,        # gigabytes to bytes
    "B_to_TB": 9.09495e-13,       # bytes to terabytes (2^40)
    "TB_to_B": 1099511627776,     # terabytes to bytes
    "B_to_PB": 8.88178e-16,       # bytes to petabytes (2^50)
    "PB_to_B": 1125899906842624,  # petabytes to bytes
    "KB_to_MB": 0.000976563,      # kilobytes to megabytes
    "MB_to_KB": 1024,             # megabytes to kilobytes
    "MB_to_GB": 0.000976563,      # megabytes to gigabytes
    "GB_to_MB": 1024,             # gigabytes to megabytes
    "GB_to_TB": 0.000976563,      # gigabytes to terabytes
    "TB_to_GB": 1024,             # terabytes to gigabytes
    "TB_to_PB": 0.000976563,      # terabytes to petabytes
    "PB_to_TB": 1024,             # petabytes to terabytes
    # Bit conversions
    "bit_to_B": 0.125,            # bits to bytes
    "B_to_bit": 8,                # bytes to bits
    "bit_to_Kb": 0.000976563,     # bits to kilobits
    "Kb_to_bit": 1024,            # kilobits to bits
    "bit_to_Mb": 9.53674e-7,      # bits to megabits
    "Mb_to_bit": 1048576,         # megabits to bits
    "bit_to_Gb": 9.31323e-10,     # bits to gigabits
    "Gb_to_bit": 1073741824,      # gigabits to bits
    "Kb_to_KB": 0.125,            # kilobits to kilobytes
    "KB_to_Kb": 8,                # kilobytes to kilobits
    "Mb_to_MB": 0.125,            # megabits to megabytes
    "MB_to_Mb": 8,                # megabytes to megabits
    "Gb_to_GB": 0.125,            # gigabits to gigabytes
    "GB_to_Gb": 8,                # gigabytes to gigabits
}

# Mapping of unit names to standardized format
DIGITAL_STORAGE_UNIT_MAP = {
    # Byte units
    "b": "B", "byte": "B", "bytes": "B",
    "kb": "KB", "kilobyte": "KB", "kilobytes": "KB", "kbyte": "KB", "kbytes": "KB",
    "mb": "MB", "megabyte": "MB", "megabytes": "MB", "mbyte": "MB", "mbytes": "MB",
    "gb": "GB", "gigabyte": "GB", "gigabytes": "GB", "gbyte": "GB", "gbytes": "GB",
    "tb": "TB", "terabyte": "TB", "terabytes": "TB", "tbyte": "TB", "tbytes": "TB",
    "pb": "PB", "petabyte": "PB", "petabytes": "PB", "pbyte": "PB", "pbytes": "PB",
    # Bit units
    "bit": "bit", "bits": "bit",
    "kbit": "Kb", "kilobit": "Kb", "kilobits": "Kb",
    "mbit": "Mb", "megabit": "Mb", "megabits": "Mb",
    "gbit": "Gb", "gigabit": "Gb", "gigabits": "Gb",
    "tbit": "Tb", "terabit": "Tb", "terabits": "Tb",
}

def convert_digital_storage(value, from_unit, to_unit):
    """Convert a value from one digital storage unit to another."""
    # Normalize units
    from_unit = DIGITAL_STORAGE_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = DIGITAL_STORAGE_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in DIGITAL_STORAGE_CONVERSIONS:
        return value * DIGITAL_STORAGE_CONVERSIONS[conversion_key]
    
    # Two-step conversion through bytes as base unit
    storage_units = ["B", "KB", "MB", "GB", "TB", "PB", "bit", "Kb", "Mb", "Gb", "Tb"]
    if from_unit in storage_units and to_unit in storage_units:
        # Convert to bytes first if not already in bytes
        if from_unit != "B":
            if from_unit == "bit":
                value = value * DIGITAL_STORAGE_CONVERSIONS["bit_to_B"]
            else:
                value = value * DIGITAL_STORAGE_CONVERSIONS.get(f"{from_unit}_to_B", 
                          1 / DIGITAL_STORAGE_CONVERSIONS[f"B_to_{from_unit}"] if f"B_to_{from_unit}" in DIGITAL_STORAGE_CONVERSIONS else None)
        
        # Then convert from bytes to target unit
        if to_unit != "B":
            if to_unit == "bit":
                value = value * DIGITAL_STORAGE_CONVERSIONS["B_to_bit"]
            else:
                value = value * DIGITAL_STORAGE_CONVERSIONS.get(f"B_to_{to_unit}", 
                          1 / DIGITAL_STORAGE_CONVERSIONS[f"{to_unit}_to_B"] if f"{to_unit}_to_B" in DIGITAL_STORAGE_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
