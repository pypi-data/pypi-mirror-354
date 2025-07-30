# csv-stringify

A Python package for converting data to CSV text format.

## Installation

```bash
pip install csv-stringify
```

## Usage

### Basic Usage

```python
from csv_stringify import stringify

output = stringify([
  ["1", "2", "3", "4"],
  ["a", "b", "c", "d"],
], header=False)

print(output)  # "1,2,3,4\na,b,c,d\n"
```

### More Examples

```python
from csv_stringify import stringify

# Basic usage
data = [["1", "2", "3"], ["a", "b", "c"]]
csv_string = stringify(data, header=False)
print(csv_string)  # "1,2,3\na,b,c\n"

# With headers
csv_string = stringify(data, columns=["A", "B", "C"])
print(csv_string)  # "A,B,C\n1,2,3\na,b,c\n"

# From dictionaries
data = [{"name": "John", "age": 25}]
csv_string = stringify(data)
print(csv_string)  # "name,age\nJohn,25\n"
```

## API

### `stringify(data, **options)`

Convert data to CSV string.

**Parameters:**
- `data`: List of lists or list of dictionaries
- `columns`: List of column names (optional)
- `header`: Include header row (default: True)
- `delimiter`: Field delimiter (default: ',')
- `quote_char`: Quote character (default: '"')
- `quote_mode`: Quoting mode (default: 'minimal')

**Returns:** CSV string

## Requirements

- Python 3.7+
- No external dependencies

## License

MIT