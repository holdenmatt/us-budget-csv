# scripts/extract_budget_data.py
import os
import numpy as np
import pandas as pd
from typing import Tuple
from config import SHEET_CONFIGS, XLS_FILENAME, COLUMN_ORDER

script_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.abspath(os.path.join(script_dir, "..", "input"))
output_dir = os.path.abspath(os.path.join(script_dir, "..", "output"))

xls_path = os.path.join(input_dir, XLS_FILENAME)

gdp_path = os.path.join(output_dir, "budget_gdp.csv")
nominal_path = os.path.join(output_dir, "budget_nominal.csv")

def read_sheet_pair(
    nominal_sheet: str,
    gdp_sheet: str,
    columns: list[str],  # List of columns to keep
    rename_map: dict[str, str] | None = None,  # Optional mapping of original -> new names
    skip_rows: int = 7,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read a pair of nominal and GDP percentage sheets.
    Returns a tuple of (nominal_df, gdp_df) with year and specified columns.
    """
    if not os.path.exists(xls_path):
        raise FileNotFoundError(f"Excel file not found: {xls_path}")

    # Read nominal values
    df_nominal = pd.read_excel(xls_path, sheet_name=nominal_sheet, skiprows=skip_rows)
    
    # Always include year column
    cols_to_keep = ['Unnamed: 0'] + columns
    df_nominal = df_nominal[cols_to_keep]
    
    # Handle renaming
    rename_dict = {'Unnamed: 0': 'Year'}
    if rename_map:
        rename_dict.update(rename_map)
    df_nominal = df_nominal.rename(columns=rename_dict)

    # Read GDP percentages 
    df_gdp = pd.read_excel(xls_path, sheet_name=gdp_sheet, skiprows=skip_rows)
    df_gdp = df_gdp[cols_to_keep]
    
    # For GDP sheet, rename columns
    gdp_rename_dict = {'Unnamed: 0': 'Year'}
    for col in columns:
        new_name = rename_dict.get(col, col)  # Use renamed column if available
        gdp_rename_dict[col] = new_name
        
    df_gdp = df_gdp.rename(columns=gdp_rename_dict)
    
    return df_nominal, df_gdp

def extract_budget_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Read and combine all budget data based on config.
    Returns tuple of (nominal_df, gdp_df).
    """
    nominal_dfs = []
    gdp_dfs = []
    
    for config in SHEET_CONFIGS.values():
        nominal_df, gdp_df = read_sheet_pair(**config)
        nominal_dfs.append(nominal_df)
        gdp_dfs.append(gdp_df)
    
    # Combine all nominal dataframes
    combined_nominal = nominal_dfs[0]
    combined_nominal = combined_nominal[pd.to_numeric(combined_nominal['Year'], errors='coerce').notna()].copy()
    combined_nominal['Year'] = pd.to_numeric(combined_nominal['Year'])

    # Combine all GDP dataframes
    combined_gdp = gdp_dfs[0]
    combined_gdp = combined_gdp[pd.to_numeric(combined_gdp['Year'], errors='coerce').notna()].copy()
    combined_gdp['Year'] = pd.to_numeric(combined_gdp['Year'])
    
    # Merge in the rest
    for nominal_df, gdp_df in zip(nominal_dfs[1:], gdp_dfs[1:]):
        combined_nominal = pd.merge(combined_nominal, nominal_df, on='Year', how='inner')
        combined_gdp = pd.merge(combined_gdp, gdp_df, on='Year', how='inner')

    # Convert surplus to deficit (more intuitive)
    combined_nominal['Deficit'] = -combined_nominal['Surplus']
    combined_gdp['Deficit'] = -combined_gdp['Surplus']

    # Reorder columns
    combined_nominal = combined_nominal[COLUMN_ORDER]
    combined_gdp = combined_gdp[COLUMN_ORDER]

    return combined_nominal, combined_gdp

def validate_data(nominal_df: pd.DataFrame, gdp_df: pd.DataFrame) -> None:
    """Validate extracted budget data for consistency."""
    assert np.allclose(
        nominal_df['Total Spending'] - nominal_df['Total Revenue'],
        nominal_df['Deficit'],
        rtol=1e-8 # Allow floating point rounding errors
    ), "Nominal deficit calculation mismatch"
    
    assert np.allclose(
        gdp_df['Total Spending'] - gdp_df['Total Revenue'],
        gdp_df['Deficit'],
        atol=0.001 # Allow rounding errors up to 0.001 percentage points
    ), "GDP deficit calculation mismatch"

def main():
    budget_nominal, budget_gdp = extract_budget_data()
    validate_data(budget_nominal, budget_gdp)

    budget_nominal.to_csv(nominal_path, index=False)
    print(f"\nWrote nominal data to {nominal_path}:\n{budget_nominal.head()}")

    budget_gdp.to_csv(gdp_path, index=False)
    print(f"\nWrote GDP data to {gdp_path}:\n{budget_gdp.head()}")

if __name__ == "__main__":
    main()