"""
Time unit conversions.
"""

TIME_CONVERSIONS = {
    # Base unit: second (s)
    "s_to_ms": 1000,              # seconds to milliseconds
    "ms_to_s": 0.001,             # milliseconds to seconds
    "s_to_us": 1000000,           # seconds to microseconds
    "us_to_s": 0.000001,          # microseconds to seconds
    "s_to_ns": 1000000000,        # seconds to nanoseconds
    "ns_to_s": 1e-9,              # nanoseconds to seconds
    "s_to_min": 0.0166667,        # seconds to minutes
    "min_to_s": 60,               # minutes to seconds
    "min_to_h": 0.0166667,        # minutes to hours
    "h_to_min": 60,               # hours to minutes
    "h_to_s": 3600,               # hours to seconds
    "s_to_h": 0.000277778,        # seconds to hours
    "h_to_d": 0.0416667,          # hours to days
    "d_to_h": 24,                 # days to hours
    "d_to_week": 0.142857,        # days to weeks
    "week_to_d": 7,               # weeks to days
    "d_to_s": 86400,              # days to seconds
    "s_to_d": 1.15741e-5,         # seconds to days
    "d_to_month": 0.0328767,      # days to months (average)
    "month_to_d": 30.4375,        # months to days (average)
    "month_to_year": 0.0833333,   # months to years
    "year_to_month": 12,          # years to months
    "d_to_year": 0.00273973,      # days to years
    "year_to_d": 365.25,          # years to days (accounting for leap years)
}

# Mapping of unit names to standardized format
TIME_UNIT_MAP = {
    "s": "s", "sec": "s", "second": "s", "seconds": "s",
    "ms": "ms", "millisecond": "ms", "milliseconds": "ms",
    "us": "us", "microsecond": "us", "microseconds": "us", "µs": "us",
    "ns": "ns", "nanosecond": "ns", "nanoseconds": "ns",
    "min": "min", "minute": "min", "minutes": "min",
    "h": "h", "hr": "h", "hour": "h", "hours": "h",
    "d": "d", "day": "d", "days": "d",
    "week": "week", "weeks": "week",
    "month": "month", "months": "month",
    "year": "year", "years": "year", "y": "year", "yr": "year"
}

def convert_time(value, from_unit, to_unit):
    """Convert a value from one time unit to another."""
    # Normalize units
    from_unit = TIME_UNIT_MAP.get(from_unit.lower(), from_unit)
    to_unit = TIME_UNIT_MAP.get(to_unit.lower(), to_unit)
    
    # If units are the same, return the value
    if from_unit == to_unit:
        return value
    
    # Direct conversion
    conversion_key = f"{from_unit}_to_{to_unit}"
    if conversion_key in TIME_CONVERSIONS:
        return value * TIME_CONVERSIONS[conversion_key]
    
    # Two-step conversion through seconds as base unit
    time_units = ["s", "ms", "us", "ns", "min", "h", "d", "week", "month", "year"]
    if from_unit in time_units and to_unit in time_units:
        # Convert to seconds first if not already in seconds
        if from_unit != "s":
            if from_unit in ["ms", "us", "ns"]:
                # Direct conversions
                value = value * TIME_CONVERSIONS[f"{from_unit}_to_s"]
            elif from_unit == "min":
                value = value * TIME_CONVERSIONS["min_to_s"]
            elif from_unit == "h":
                value = value * TIME_CONVERSIONS["h_to_s"]
            elif from_unit == "d":
                value = value * TIME_CONVERSIONS["d_to_s"]
            elif from_unit == "week":
                value = value * TIME_CONVERSIONS["week_to_d"] * TIME_CONVERSIONS["d_to_s"]
            elif from_unit == "month":
                value = value * TIME_CONVERSIONS["month_to_d"] * TIME_CONVERSIONS["d_to_s"]
            elif from_unit == "year":
                value = value * TIME_CONVERSIONS["year_to_d"] * TIME_CONVERSIONS["d_to_s"]
        
        # Then convert from seconds to target unit
        if to_unit != "s":
            if to_unit in ["ms", "us", "ns"]:
                # Direct conversions
                value = value * TIME_CONVERSIONS[f"s_to_{to_unit}"]
            elif to_unit == "min":
                value = value * TIME_CONVERSIONS["s_to_min"]
            elif to_unit == "h":
                value = value * TIME_CONVERSIONS["s_to_h"]
            elif to_unit == "d":
                value = value * TIME_CONVERSIONS["s_to_d"]
            elif to_unit == "week":
                value = value * TIME_CONVERSIONS["s_to_d"] * TIME_CONVERSIONS["d_to_week"]
            elif to_unit == "month":
                value = value * TIME_CONVERSIONS["s_to_d"] * TIME_CONVERSIONS["d_to_month"]
            elif to_unit == "year":
                value = value * TIME_CONVERSIONS["s_to_d"] * TIME_CONVERSIONS["d_to_year"]
            
        return value
    
    return None  # Conversion not supported
