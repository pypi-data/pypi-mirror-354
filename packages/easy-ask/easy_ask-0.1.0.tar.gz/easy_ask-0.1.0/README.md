# easy-ask

easy-ask is a minimal demonstration package intended to show how chart options can be generated programmatically. The library exposes a function called `generate_option` which accepts a chart type and data description and returns a configuration dictionary.

## Quick start

```python
from easy_ask import generate_option

# Build an option for a bar chart
option = generate_option(
    chart_type="bar",
    data=[{"value": 10}, {"value": 20}, {"value": 30}],
    title="Demo Bar Chart",
)
print(option)
```

## Python version

This project requires **Python 3.12** or newer, as specified in `pyproject.toml`.

## Running the demo

To see the package in action, run the demonstration module:

```bash
python -m easy_ask
```

Example scripts are also available in the `examples/` directory.
