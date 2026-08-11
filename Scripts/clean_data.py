import pandas as pd


def clean_data(df):
    """
    Clean the raw Telco Customer Churn data.

    Steps:
    1. Clean column names
    2. Remove extra whitespace from string values
    3. Handle missing values
    4. Remove duplicate rows
    """

    # 1. Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2. Remove extra whitespace from string columns
    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].str.strip()

    # 3. Convert blank strings to missing values
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # 4. Remove duplicate rows
    df = df.drop_duplicates()

    # 5. Handle missing values
    # Numeric columns -> median
    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    # Text/categorical columns -> "Unknown"
    string_columns = df.select_dtypes(include="object").columns

    for column in string_columns:
        df[column] = df[column].fillna("Unknown")

    return df


if __name__ == "__main__":
    # Path to raw dataset
    file_path = "../Data/WA_Fn-UseC_-Telco-Customer-Churn.csv"

    # Read raw data
    data = pd.read_csv(file_path)

    # Clean data
    cleaned_data = clean_data(data)

    # Display result
    print("Raw data shape:", data.shape)
    print("Cleaned data shape:", cleaned_data.shape)
    print("\nMissing values after cleaning:")
    print(cleaned_data.isnull().sum())
