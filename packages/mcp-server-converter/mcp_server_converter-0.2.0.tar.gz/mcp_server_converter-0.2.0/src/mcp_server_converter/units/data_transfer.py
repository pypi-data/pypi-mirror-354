"""
Data transfer rate unit conversions.
"""

DATA_TRANSFER_CONVERSIONS = {
    # Base unit: bits per second (bit/s)
    "bit/s_to_kbit/s": 0.001,            # bits per second to kilobits per second
    "kbit/s_to_bit/s": 1000,             # kilobits per second to bits per second
    "bit/s_to_mbit/s": 0.000001,         # bits per second to megabits per second
    "mbit/s_to_bit/s": 1000000,          # megabits per second to bits per second
    "bit/s_to_gbit/s": 1e-9,             # bits per second to gigabits per second
    "gbit/s_to_bit/s": 1000000000,       # gigabits per second to bits per second
    "bit/s_to_B/s": 0.125,               # bits per second to bytes per second
    "B/s_to_bit/s": 8,                   # bytes per second to bits per second
    "B/s_to_kB/s": 0.001,                # bytes per second to kilobytes per second
    "kB/s_to_B/s": 1000,                 # kilobytes per second to bytes per second
    "B/s_to_MB/s": 0.000001,             # bytes per second to megabytes per second
    "MB/s_to_B/s": 1000000,              # megabytes per second to bytes per second
    "B/s_to_GB/s": 1e-9,                 # bytes per second to gigabytes per second
    "GB/s_to_B/s": 1000000000,           # gigabytes per second to bytes per second
    "kbit/s_to_kB/s": 0.125,             # kilobits per second to kilobytes per second
    "kB/s_to_kbit/s": 8,                 # kilobytes per second to kilobits per second
    "mbit/s_to_MB/s": 0.125,             # megabits per second to megabytes per second
    "MB/s_to_mbit/s": 8,                 # megabytes per second to megabits per second
    "gbit/s_to_GB/s": 0.125,             # gigabits per second to gigabytes per second
    "GB/s_to_gbit/s": 8,                 # gigabytes per second to gigabits per second
}

# Mapping of unit names to standardized format
DATA_TRANSFER_UNIT_MAP = {
    # Bit-based units
    "bps": "bit/s", 
    "bit/s": "bit/s", 
    "bit/sec": "bit/s", 
    "bits/s": "bit/s", 
    "bits/sec": "bit/s", 
    "bits per second": "bit/s",
    
    "kbps": "kbit/s", 
    "kbit/s": "kbit/s", 
    "kbit/sec": "kbit/s", 
    "kilobit/s": "kbit/s", 
    "kilobit/sec": "kbit/s", 
    "kilobits/s": "kbit/s", 
    "kilobits per second": "kbit/s",
    
    "mbps": "mbit/s", 
    "mbit/s": "mbit/s", 
    "mbits/s": "mbit/s", 
    "mbit/sec": "mbit/s", 
    "megabit/s": "mbit/s", 
    "megabit/sec": "mbit/s", 
    "megabits/s": "mbit/s", 
    "megabits per second": "mbit/s",
    
    "gbps": "gbit/s", 
    "gbit/s": "gbit/s", 
    "gbit/sec": "gbit/s", 
    "gigabit/s": "gbit/s", 
    "gigabit/sec": "gbit/s", 
    "gigabits/s": "gbit/s", 
    "gigabits per second": "gbit/s",
    
    # Byte-based units
    "b/s": "B/s", 
    "B/s": "B/s", 
    "B/sec": "B/s", 
    "bytes/s": "B/s", 
    "bytes/sec": "B/s", 
    "bytes per second": "B/s",
    
    "kb/s": "kB/s", 
    "kB/s": "kB/s", 
    "kB/sec": "kB/s", 
    "kilobytes/s": "kB/s", 
    "kilobytes/sec": "kB/s", 
    "kilobytes per second": "kB/s",
    
    "mb/s": "MB/s", 
    "MB/s": "MB/s", 
    "MB/sec": "MB/s", 
    "megabytes/s": "MB/s", 
    "megabytes/sec": "MB/s", 
    "megabytes per second": "MB/s",
    
    "gb/s": "GB/s", 
    "GB/s": "GB/s", 
    "GB/sec": "GB/s", 
    "gigabytes/s": "GB/s", 
    "gigabytes/sec": "GB/s", 
    "gigabytes per second": "GB/s"
}

def convert_data_transfer(value, from_unit, to_unit):
    """Convert a value from one data transfer rate unit to another."""
    # Normalize units
    from_unit = DATA_TRANSFER_UNIT_MAP.get(from_unit.lower(), from_unit.lower())
    to_unit = DATA_TRANSFER_UNIT_MAP.get(to_unit.lower(), to_unit.lower())
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in DATA_TRANSFER_CONVERSIONS:
        return value * DATA_TRANSFER_CONVERSIONS[conversion_key]
    
    # Two-step conversion through bits per second as base unit
    data_transfer_units = ["bit/s", "kbit/s", "mbit/s", "gbit/s", "B/s", "kB/s", "MB/s", "GB/s"]
    if from_unit in data_transfer_units and to_unit in data_transfer_units:
        # Convert to bits per second first if not already in bits per second
        if from_unit != "bit/s":
            value = value * DATA_TRANSFER_CONVERSIONS.get(f"{from_unit}_to_bit/s", 
                      1 / DATA_TRANSFER_CONVERSIONS[f"bit/s_to_{from_unit}"] if f"bit/s_to_{from_unit}" in DATA_TRANSFER_CONVERSIONS else None)
        
        # Then convert from bits per second to target unit
        if to_unit != "bit/s":
            value = value * DATA_TRANSFER_CONVERSIONS.get(f"bit/s_to_{to_unit}", 
                      1 / DATA_TRANSFER_CONVERSIONS[f"{to_unit}_to_bit/s"] if f"{to_unit}_to_bit/s" in DATA_TRANSFER_CONVERSIONS else None)
            
        return value
    
    return None  # Conversion not supported
