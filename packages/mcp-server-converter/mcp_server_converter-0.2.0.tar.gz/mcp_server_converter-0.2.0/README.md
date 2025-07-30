# Unit Converter MCP Server

A Model Context Protocol server for converting between different units. This server enables LLMs to perform accurate unit conversions across multiple measurement categories.

### Available Tools

- `convert` - Converts between different units.
  - `expression` (string, required): Expression to be converted in the format "value from_unit to to_unit" (e.g., "5.2 m to km" or "500 hz to khz")

### Supported Unit Categories

The converter supports the following categories of units:

1. **Length**: m, km, cm, inch, ft, mile, etc.
2. **Area**: sqm, sqkm, sqft, acre, ha, etc.
3. **Volume**: m3, l, ml, gal, qt, pt, cup, floz, etc.
4. **Mass/Weight**: kg, g, mg, lb, oz, t, st, etc.
5. **Temperature**: celsius (c), fahrenheit (f), kelvin (k)
6. **Energy**: j, kj, cal, kcal, wh, kwh, btu, etc.
7. **Power**: w, kw, mw, hp, btu_h, etc.
8. **Pressure**: pa, kpa, bar, atm, psi, mmhg, etc.
9. **Speed**: m/s, km/h, mph, ft/s, knot, etc.
10. **Time**: s, ms, min, h, day, week, month, year, etc.
11. **Digital Storage**: B, KB, MB, GB, bit, Kb, Mb, Gb, etc.
12. **Fuel Economy**: km/l, mpg, l/100km, etc.
13. **Data Transfer Rate**: bit/s, kbit/s, mbit/s, B/s, MB/s, etc.

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-server-converter*.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Using PIP

Alternatively you can install `mcp-server-converter` via pip:

```bash
pip install mcp-server-converter
```

After installation, you can run it as a script using:

```bash
python -m mcp_server_converter
```

## Configuration

### Using uv (recommended)

Add this to your MCP client settings:

```json
"mcpServers": {
  "converter": {
    "command": "uvx",
    "args": ["mcp-server-converter"]
  }
}
```

### Using PIP

Alternatively add this to your MCP client settings:

```json
"mcpServers": {
  "converter": {
    "command": "python3",
    "args": ["-m", "mcp_server_converter"]
  }
}
```

## Supported Unit Conversions

### Length Units
- Meters (m, meter, meters)
- Kilometers (km, kilometer, kilometers)
- Centimeters (cm, centimeter, centimeters)
- Inches (in, inch, inches)
- Feet (ft, foot, feet)
- Miles (mi, mile, miles)

### Frequency Units
- Hertz (hz, hertz)
- Kilohertz (khz, kilohertz)
- Megahertz (mhz, megahertz)
- Gigahertz (ghz, gigahertz)

## Examples

### Length Conversions
- Convert meters to kilometers: `5 m to km` → `0.005`
- Convert miles to kilometers: `1 mile to km` → `1.60934`
- Convert feet to meters: `10 ft to m` → `3.048`
- Convert inches to centimeters: `12 in to cm` → `30.48`

### Frequency Conversions
- Convert hertz to kilohertz: `500 hz to khz` → `0.5`
- Convert kilohertz to megahertz: `1500 khz to mhz` → `1.5`
- Convert hertz to megahertz: `2000000 hz to mhz` → `2`
- Convert gigahertz to megahertz: `2.5 ghz to mhz` → `2500`

## License

mcp-server-converter is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
