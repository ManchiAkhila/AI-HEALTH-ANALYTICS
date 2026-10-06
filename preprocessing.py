
import pandas as pd
from pathlib import Path


def load_health_data():
    # Find the project folder
    project_root = Path(__file__).resolve().parent.parent

    # Location of our dataset
    data_path = project_root / "data" / "health_data.csv"

    # Load CSV
    df = pd.read_csv(data_path)

    # Convert date column
    df["date"] = pd.to_datetime(df["date"]) 

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing numerical values with median
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    return df


if __name__ == "__main__":
    data = load_health_data()

    print("Health data loaded successfully!")
    print("\nDataset shape:", data.shape)
    print("\nColumns:")
    print(data.columns.tolist())
    print("\nFirst 5 rows:")
    print(data.head())