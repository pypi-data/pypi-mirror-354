


![ISEL logo](https://raw.githubusercontent.com/crpereir/jsonify/main/img/logo-isel.png)


# JSONIFYER

[![PyPI version](https://badge.fury.io/py/jsonify.svg)](https://badge.fury.io/py/jsonify)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com/carol/jsonify)

A Python package to easily convert different types of files into JSON format. JSONIFYER provides a simple and efficient way to transform various file formats (XML, CSV, TXT) into JSON, making it easier to work with structured data in your Python applications.

## Features

- Convert XML files to JSON using either Python-based or XSLT methods
- Convert CSV files to JSON with customizable options
- Convert TXT files to JSON with customizable options
- Detailed error handling and validation

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
4. [Project Structure](#project-structure)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)

## Installation

Install via PyPI:

```bash
pip install jsonifyer
```

Or install locally for development:

```bash
git clone https://github.com/crpereir/jsonify.git
cd jsonifyer
pip install -e .
```

## Quick Start

```python
from jsonify import convert_file, convert_csv, convert_xml

# Convert any supported file type
result = convert_file(
    file_path="data/input/example.xml",
    fields=["name", "description", "price"],
    file_type="xml"
)

# Convert CSV specifically
result = convert_csv(
    file_path="data/input/example.csv",
    fields=["id", "name", "value"],
    delimiter=",",
    skiprows=1
)

# Convert XML with specific options
result = convert_xml(
    file_path="data/input/example.xml",
    fields=["name", "description"],
    converter="python",  # or "xslt"
    namespaces={"ns": "http://example.com/ns"},
    root_tag="items"
)
```

### Directory Structure

The package automatically manages input and output directories based on file types:

- CSV files: `csv_files/`
- XML files: `xml_files/`
- TXT files: `text_files/`

## Project Structure

```
jsonify/
├── README.md                  # Project documentation
├── setup.py                   # Setup script for installation
└── src/
    └── jsonifyer/
        ├── __init__.py        # Package initialization
        ├── api.py             # Main API functions
        ├── config.py          # Directory management
        ├── config_loader.py   # Configuration handling
        ├── main.py            # Core conversion logic
        └── converter/         # Conversion implementations
            ├── __init__.py
            ├── csv_converter.py
            ├── python_converter.py
            └── xslt_converter.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- GitHub: [https://github.com/crpereir/jsonifyer](https://github.com/crpereir/jsonifyer)
- Email: carolinadpereira18[@]gmail.com & matilde.pato[@]isel.pt
