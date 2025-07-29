# STanalysis

<p align="center">
  <img src="DSS_Logo.png" alt="DSS Logo" width="200"/>
</p>

A Python package for extracting, analyzing, and comparing environmental data from multiple sources.

> Developed by the Data Science Support group (DSS) at AWI  
> For the HealthyPlanet Project – BIPS, under the DataNord initiative

---

## Features

- Extract point values from NetCDF datasets with spatial and temporal dimensions
- Support for multiple input formats (CSV, Shapefile, GeoJSON)
- Temporal aggregation with configurable window sizes
- Efficient nearest-neighbor interpolation
- Comprehensive error handling and input validation

## Installation

You can install STanalysis directly from PyPI:

```bash
pip install STanalysis
```

Or install from source for development:

```bash
git clone https://github.com/MuhammadShafeeque/dss-environment-analysis.git
cd dss-environment-analysis
uv pip install -e .[dev]
```

## Quick Start

Here's a simple example of extracting temperature values at specific points:

```python
from STanalysis import extract_point_values

# Extract values from a NetCDF file at specified points
result_df = extract_point_values(
    netcdf_path="temperature.nc",
    points_path="measurement_points.csv",
    variable="temperature",
    days_back=2,  # Average over the last 2 days
    date_col="date"
)

print(result_df[["name", "lat", "lon", "value"]])
```

Input CSV format example:
```csv
name,lat,lon,date
"Bremen City",53.0793,8.8017,2024-06-08
"Bremen North",53.1680,8.6317,2024-06-15
```

## Documentation

### Main Functions

#### `extract_point_values`

```python
def extract_point_values(
    netcdf_path: str | Path,
    points_path: str | Path,
    variable: str,
    *,
    days_back: int = 7,
    date_col: Optional[str] = None,
    output_path: Optional[str | Path] = None,
) -> pd.DataFrame
```

Parameters:
- `netcdf_path`: Path to the input NetCDF file
- `points_path`: Path to point data (CSV, shapefile or GeoJSON)
- `variable`: Name of the variable to extract from the NetCDF dataset
- `days_back`: Number of days to average backwards from the provided date
- `date_col`: Optional column in the point file containing the date
- `output_path`: Optional path to write results (CSV or JSON)

Returns:
- DataFrame containing the extracted values and point metadata

### Development Setup

#### Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

#### Using Dev Container

1. **Clone the Repository:**
```bash
git clone https://github.com/MuhammadShafeeque/dss-environment-analysis.git
cd dss-environment-analysis
```

2. **Open in Dev Container:**
   - Open VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Dev Containers: Open Folder in Container"
   - Select the cloned repository folder

The dev container provides:
- Python 3.13+ with `uv` package manager
- Pre-configured VS Code extensions
- All development dependencies

#### Development Tools

The development environment includes:
- **pytest** for testing
- **mypy** for type checking
- **ruff** for code formatting and linting

Run tests:
```bash
pytest
```

Run type checking:
```bash
mypy STanalysis
```

Format code:
```bash
ruff format .
```

### Project Structure

```
dss-environment-analysis/          # Repository root
├── STanalysis/                   # Main package source
│   ├── __init__.py              # Package initialization
│   └── point_extraction.py       # Core functionality
├── examples/                     # Example scripts
│   └── point_extraction_example.py
├── tests/                        # Test files
├── docs/                         # Documentation
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Note:** This repository is under active development. Features and APIs may change.
