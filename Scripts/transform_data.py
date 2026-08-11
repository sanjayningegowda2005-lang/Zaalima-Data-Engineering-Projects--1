import pandas as pd


def transform_data(df):
    """
    Transform cleaned Telco Customer Churn data.

    Steps:
    1. Convert numeric columns to numeric data types
    2. Create useful features
    3. Return a ready-to-load DataFrame
    """

    # 1. Convert numeric columns
    numeric_columns = [
        "seniorcitizen",
        "tenure",
        "monthlycharges",
        "totalcharges"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    # 2. Feature engineering

    # Total expected revenue based on monthly charges and tenure
    if "monthlycharges" in df.columns and "tenure" in df.columns:
        df["estimated_lifetime_value"] = (
            df["monthlycharges"] * df["tenure"]
        )

    # Average monthly charge per year of tenure
    if "tenure" in df.columns and "monthlycharges" in df.columns:
        df["tenure_years"] = df["tenure"] / 12

    return df


if __name__ == "__main__":
    # Read cleaned data
    file_path = "Data/WA_Fn-UseC_-Telco-Customer-Churn.csv"

    data = pd.read_csv(file_path)

    # Transform data
    transformed_data = transform_data(data)

    # Display data types
    print("Data types after transformation:")
    print(transformed_data.dtypes)

    print("\nTransformed data preview:")
    print(transformed_data.head())

    print("\nFinal shape:", transformed_data.shape)
