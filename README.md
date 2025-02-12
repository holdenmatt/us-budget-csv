# US Federal Budget Deficit CSV extractor

A simple Python script to extract historical US federal budget data from
Congressional Budget Office (CBO) Excel files into CSV format.

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone this repository:
```bash
git clone https://github.com/holdenmatt/us-deficit-csv.git
cd us-deficit-csv
```

2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install:
```bash
pip install -r requirements.txt
```

## Usage

1. Download the latest "Historical Budget Data" Excel file from the
[CBO website](https://www.cbo.gov/data/budget-economic-data)

2. Move the Excel file to the `input/` directory

3. Run the script:
```bash
python scripts/extract_budget_data.py
```

The script will generate two CSV files in the `output/` directory:
- `budget_gdp.csv`: Budget values as a percentage of gross domestic product (GDP)
- `budget_nominal.csv`: Raw budget values in billions of dollars