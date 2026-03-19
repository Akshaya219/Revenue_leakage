from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
INPUT_FILE = DATA_DIR / "hospital_claims_60k_realistic_v2.csv"
OUTPUT_FILE = DATA_DIR / "feature_store.csv"

CATEGORICAL_COLS = [
    "Department",
    "Procedure_Code",
    "Insurance_Type",
]

NUMERICAL_COLS = [
    "Claim_Amount",
    "Billing_Amount",
    "Approved_Amount",
    "Expected_Revenue",
    "Actual_Revenue",
    "Payment_Received",
    "Documentation_Delay_Days",
    "Length_of_Stay",
    "Previous_Denial_Count",
]

DATE_COLS = ["Claim_Submission_Date", "Settlement_Date"]


def _fill_numeric_with_median(df: pd.DataFrame, columns: list[str]) -> None:
    """Coerce numeric columns and fill missing values with median in one vectorized pass."""
    df[columns] = df[columns].apply(pd.to_numeric, errors="coerce")
    medians = df[columns].median(numeric_only=True)
    df[columns] = df[columns].fillna(medians)


def _prepare_dates(df: pd.DataFrame, columns: list[str]) -> None:
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors="coerce").ffill()


def preprocess() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE).drop_duplicates().reset_index(drop=True)

    for col in CATEGORICAL_COLS:
        df[col] = df[col].fillna("Unknown")

    _fill_numeric_with_median(df, NUMERICAL_COLS)
    _prepare_dates(df, DATE_COLS)

    expected_nonzero = df["Expected_Revenue"].replace(0, np.nan)
    billing_nonzero = df["Billing_Amount"].replace(0, np.nan)

    df["Revenue_Leakage"] = df["Expected_Revenue"] - df["Actual_Revenue"]
    df["Revenue_Leakage_Index"] = (df["Revenue_Leakage"] / expected_nonzero) * 100
    df["Charge_Capture_Efficiency"] = (df["Billing_Amount"] / expected_nonzero) * 100

    df["Accounts_Receivable_Days"] = (
        df["Settlement_Date"] - df["Claim_Submission_Date"]
    ).dt.days.clip(lower=0)

    df["Revenue_at_Risk"] = df["Billing_Amount"] - df["Payment_Received"]
    df["Claim_Approval_Gap"] = df["Billing_Amount"] - df["Approved_Amount"]
    df["Claim_Approval_Rate"] = (df["Approved_Amount"] / billing_nonzero) * 100

    df["Month"] = df["Claim_Submission_Date"].dt.to_period("M").astype(str)
    df["Day_of_Week"] = df["Claim_Submission_Date"].dt.day_name()

    return df


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df = preprocess()
    df.to_csv(OUTPUT_FILE, index=False)
    print("Data preprocessing completed")
    print(df.head())


if __name__ == "__main__":
    main()