"""
Configuration for extracting budget data from CBO Excel worksheets.
Defines the sheet names, columns, and rename mappings for each section.
"""
from typing import TypedDict, List

XLS_FILENAME = "51134-2025-01-Historical-Budget-Data.xlsx"

class SheetConfig(TypedDict):
    nominal_sheet: str
    gdp_sheet: str
    columns: List[str]
    rename_map: dict[str, str] | None
    skip_rows: int

# Configure columns to extract from each Excel sheet
SHEET_CONFIGS: dict[str, SheetConfig] = {
    "deficit": {
        "nominal_sheet": "1. Rev, Outlays, Surplus, Debt",
        "gdp_sheet": "1a. Rev, Outlays, Surplus (GDP)",
        "columns": ["Total"],
        "rename_map": {"Total": "Surplus"},
        "skip_rows": 8
    },
    "revenue": {
        "nominal_sheet": "2. Revenues",
        "gdp_sheet": "2a. Revenues as Share of GDP",
        "columns": ["Total"],
        "rename_map": {"Total": "Total Revenue"},
        "skip_rows": 7
    },
    "spending": {
        "nominal_sheet": "3. Outlays",
        "gdp_sheet": "3a. Outlays as Share of GDP",
        "columns": ["Net interest", "Total"],
        "rename_map": {"Total": "Total Spending"},
        "skip_rows": 8
    },
    "defense": {
        "nominal_sheet": "4. Discretionary Outlays",
        "gdp_sheet": "4a. Discretionary Outlays (GDP)", 
        "columns": ["Defense", "Nondefense"],
        "rename_map": {"Nondefense": "Non-defense discretionary"},
        "skip_rows": 7
    },
    "mandatory": {
        "nominal_sheet": "5. Mandatory Outlays",
        "gdp_sheet": "5a. Mandatory Outlays (GDP)",
        "columns": [
            'Social Security',
            'Medicareᵃ',
            'Medicaid',
            'Income securityᵇ',
            'Federal civilian and military retirement',
            "Veterans’ programs",
            "Other programs",
            "Offsetting receipts"
        ],
        "rename_map": {
            'Medicareᵃ': 'Medicare',
            'Income securityᵇ': 'Income security',
            'Veterans’ programs': 'Veterans programs'
        },
        "skip_rows": 7
    }
}