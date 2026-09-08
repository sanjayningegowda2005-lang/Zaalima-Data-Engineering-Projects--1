import pytest
import pandas as pd
from ingest_data import validate_file_extension, validate_schema, clean_dataframe

def test_validate_file_extension_valid():
    assert validate_file_extension("data.csv") is True
    assert validate_file_extension("data.xlsx") is True

def test_validate_file_extension_invalid():
    assert validate_file_extension("data.txt") is False
    assert validate_file_extension("data.json") is False

def test_validate_schema(tmp_path):
    schema = {"customer_churn": {"columns": ["customerID", "gender"]}}
    file = tmp_path / "test.csv"
    pd.DataFrame({"customerID": ["C1"], "gender": ["Male"]}).to_csv(file, index=False)
    assert validate_schema(file, schema) is True

def test_validate_schema_mismatch(tmp_path):
    schema = {"customer_churn": {"columns": ["customerID", "gender"]}}
    file = tmp_path / "bad.csv"
    pd.DataFrame({"id": [1], "name": ["Abhi"]}).to_csv(file, index=False)
    assert validate_schema(file, schema) is False

def test_clean_dataframe():
    df = pd.DataFrame({"col": ["  hello ", "world"]})
    cleaned = clean_dataframe(df)
    assert cleaned.iloc[0, 0] == "hello"
    # Access dtype by column name
    assert str(cleaned.dtypes["col"]).startswith("string")

