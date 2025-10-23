# File Processor

A Python-based CSV file processing system that validates, transforms, and converts data files with comprehensive logging and error handling.

## Overview

This file processor is designed to handle CSV files with specific validation requirements, data transformations, and output formatting. It processes files through a pipeline of validation, transformation, and conversion steps, with detailed logging throughout the process.

## Features

- **File Validation**: Validates required columns, data types, and data completeness
- **Data Transformation**: Converts dates to specified formats and applies currency conversion
- **Multiple Output Formats**: Supports JSON and CSV output formats
- **Comprehensive Logging**: Detailed logging with separate info and error logs
- **Error Handling**: Robust error handling with file categorization (success/error)
- **Configuration Management**: YAML-based configuration system

## Project Structure

```
file_processor/
├── config/
│   ├── __init__.py
│   └── config.py          # Configuration management
├── project/
│   ├── __init__.py
│   ├── main.py            # Main entry point
│   ├── processor.py       # Core file processing logic
│   ├── transformer.py     # Data transformation utilities
│   ├── validator.py       # Data validation utilities
│   ├── logging.py         # Logging configuration
│   └── test.py            # Test file
├── input/                 # Input CSV files
├── output/
│   ├── logs/              # Log files
│   ├── processed/         # Processed files (success/error)
│   └── *.json            # Output JSON files
├── config.yml            # Configuration file
├── requirements.txt      # Python dependencies
└── README.md
```

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The system uses a `config.yml` file for configuration. Default configuration includes:

- **Required Columns**: `name`, `date`, `amount`
- **Column Types**: String, date, and float types
- **Date Format**: `%Y-%d-%m`
- **Currency Conversion**: EUR to USD with rate 1.6
- **Output Format**: JSON

### Configuration Options

- `required_column`: List of required column names
- `column_type`: Expected data types for each column
- `date_format`: Date parsing format
- `currency_conversion`: Source and target currencies
- `currency_rate`: Conversion rate
- `required_output_format`: Output format (json/csv)

## Usage

### Basic Usage

```bash
python -m project.main <filename>
```

### Examples

```bash
# Process a CSV file
python -m project.main sales_data.csv

# Process with date parsing
python -m project.main sales_data.csv --date
```

### Input File Requirements

Your CSV files should contain the required columns as specified in the configuration:

- `name` (string)
- `date` (date in specified format)
- `amount` (float)

## Processing Pipeline

1. **File Reading**: Reads CSV file with optional date parsing
2. **Column Validation**: Checks for required columns
3. **Type Validation**: Validates data types match expectations
4. **Completeness Check**: Ensures no missing values
5. **Data Transformation**:
   - Date format conversion
   - Currency conversion (if applicable)
6. **Output Generation**: Converts to specified output format
7. **File Management**: Moves processed files to success/error directories

## Output

- **Success**: Files are moved to `output/processed/success/` and JSON output is created
- **Error**: Files are moved to `output/processed/error/` with error details logged
- **Logs**: Detailed processing logs in `output/logs/`

## Dependencies

- `pandas`: Data manipulation and analysis
- `loguru`: Advanced logging
- `pyyaml`: YAML configuration parsing
- `numpy`: Numerical operations
- `python-dateutil`: Date parsing utilities

## Error Handling

The system provides comprehensive error handling:

- **File Reading Errors**: Logged and file moved to error directory
- **Validation Errors**: Column, type, and completeness validation with detailed error messages
- **Transformation Errors**: Date and currency conversion errors
- **Output Errors**: JSON/CSV conversion failures

## Logging

The system uses structured logging with:

- **Info Logs**: Processing steps and successful operations
- **Error Logs**: Detailed error information
- **Log Rotation**: Automatic log rotation at 10MB

## Example Data

### Input CSV Format

```csv
name,date,amount
Alice,2024-01-01,120.50
Bob,2024-01-02,250.75
```

### Output JSON Format

```json
[
  {
    "name": "Alice",
    "date": 1735689600000,
    "amount": 192.8
  },
  {
    "name": "Bob",
    "date": 1739577600000,
    "amount": 401.2
  }
]
```

## Development

The project follows a modular architecture:

- `main.py`: Entry point and argument parsing
- `processor.py`: Core processing logic
- `validator.py`: Data validation utilities
- `transformer.py`: Data transformation utilities
- `logging.py`: Logging configuration
- `config.py`: Configuration management

## License

This project is available for use and modification.
