# US Historical Federal Budget Data CSV extractor

A Python script that extracts historical US federal budget data from Congressional Budget Office (CBO) Excel workbooks into CSV format.

**Important**: We deliberately avoid any calculations or transformations here.
All values are extracted directly from CBO's published data.

You can audit the extraction script [here](https://github.com/holdenmatt/us-budget-csv/blob/main/scripts/extract_budget_data.py). The only changes made during extraction are:
- Converting surplus values to deficit (multiplying by -1) for more intuitive interpretation
- Very minor column renames and reordering for readability

## Output

The script extracts CBO data into two CSV files:
- `budget_gdp.csv`: Budget values as a percentage of gross domestic product (GDP)
- `budget_nominal.csv`: Raw nominal budget values in billions of dollars (not adjusted for inflation)

GDP percentages are generally more meaningful for analysis since they show spending, revenue,
and deficits relative to the size of the economy (which is what matters).

## Requirements

- Python 3.8+
- pip

## Installation

1. Clone this repository:
```bash
git clone https://github.com/holdenmatt/us-budget-csv.git
cd us-budget-csv
```

2. Create a Python virtual environment:
```bash
python -m venv venv
```

3. Activate it:
```bash
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

4. Install dependencies:
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