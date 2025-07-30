from mcp_server_converter.converter import evaluate

def test_conversion(expression, expected=None):
    """Test a conversion and print the result"""
    result = evaluate(expression)
    if expected is not None:
        passed = False
        try:
            result_float = float(result)
            passed = abs(result_float - expected) < 0.001
        except ValueError:
            # Result might be an error message
            pass
        status = "PASSED" if passed else "FAILED"
        print(f"{status}: '{expression}' => {result} (expected {expected})")
    else:
        print(f"Result of '{expression}': {result}")

def run_tests():
    print("Testing Length conversions:")
    test_conversion("5 km to miles", 3.10686)
    test_conversion("10 feet to meters", 3.048)
    test_conversion("100 cm to inches", 39.37)
    test_conversion("42 inches to cm", 106.68)
    test_conversion("5280 feet to mile", 1)
    
    print("\nTesting Area conversions:")
    test_conversion("1 sqm to sqft", 10.7639)
    test_conversion("2 acre to sqm", 8093.72)
    test_conversion("3 ha to acre", 7.41316)
    test_conversion("1000 sqft to acre", 0.023)
    test_conversion("10000 sqm to ha", 1)
    
    print("\nTesting Volume conversions:")
    test_conversion("1 l to ml", 1000)
    test_conversion("1 gal to l", 3.78541)
    test_conversion("1 ft3 to m3", 0.0283168)
    test_conversion("3 cup to floz", 24)
    test_conversion("2 qt to pt", 4)
    
    print("\nTesting Mass/Weight conversions:")
    test_conversion("70 kg to lb", 154.323)
    test_conversion("160 lb to kg", 72.5748)
    test_conversion("1000 g to kg", 1)
    test_conversion("16 oz to lb", 1)
    test_conversion("14 st to lb", 196)
    
    print("\nTesting Temperature conversions:")
    test_conversion("32 f to c", 0)
    test_conversion("100 c to f", 212)
    test_conversion("0 c to k", 273.15)
    test_conversion("373.15 k to c", 100)
    test_conversion("77 f to k", 298.15)
    
    print("\nTesting Energy conversions:")
    test_conversion("1 kwh to j", 3600000)
    test_conversion("1000 j to cal", 239.006)
    test_conversion("1 kcal to j", 4184)
    test_conversion("1 btu to j", 1055.06)
    test_conversion("3.6 mj to kwh", 1)
    
    print("\nTesting Power conversions:")
    test_conversion("1 hp to w", 745.7)
    test_conversion("1000 w to kw", 1)
    test_conversion("2 kw to hp", 2.682)
    test_conversion("1 kw to btu_h", 3412.14)
    test_conversion("1000 w to btu_h", 3412.14)
    
    print("\nTesting Pressure conversions:")
    test_conversion("1 atm to psi", 14.6959)
    test_conversion("1 bar to kpa", 100)
    test_conversion("760 mmhg to atm", 1)
    test_conversion("101325 pa to atm", 1)
    test_conversion("14.7 psi to bar", 1.01355)
    
    print("\nTesting Speed conversions:")
    test_conversion("100 km/h to mph", 62.1371)
    test_conversion("60 mph to km/h", 96.5604)
    test_conversion("1 m/s to km/h", 3.6)
    test_conversion("88 ft/s to mph", 60)
    test_conversion("30 knot to mph", 34.5233)
    
    print("\nTesting Time conversions:")
    test_conversion("1 h to min", 60)
    test_conversion("1 day to h", 24)
    test_conversion("1 week to day", 7)
    test_conversion("365 day to year", 0.999315)
    test_conversion("60000 ms to min", 1)
    
    print("\nTesting Digital Storage conversions:")
    test_conversion("1 GB to MB", 1024)
    test_conversion("1024 KB to MB", 1)
    test_conversion("8 bit to B", 1)
    test_conversion("1 TB to GB", 1024)
    test_conversion("1024 MB to GB", 1)
    
    print("\nTesting Fuel Economy conversions:")
    test_conversion("10 km/l to mpg", 23.5215)
    test_conversion("25 mpg to l/100km", 9.40858)
    test_conversion("5 l/100km to km/l", 20)
    test_conversion("25 mpg to mpgimp", 20.8168)
    test_conversion("30 mpgimp to mpg", 36.0286)
    
    print("\nTesting Data Transfer Rate conversions:")
    test_conversion("1 MB/s to mbit/s", 8)
    test_conversion("100 mbit/s to MB/s", 12.5)
    test_conversion("1 gbit/s to mbit/s", 1000)
    test_conversion("8 bit/s to B/s", 1)
    test_conversion("1 GB/s to gbit/s", 8)

if __name__ == "__main__":
    run_tests()

