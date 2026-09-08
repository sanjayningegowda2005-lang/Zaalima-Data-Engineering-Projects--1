# generate_sample_data.py
import pandas as pd
import random

def generate_sample_data(rows=100):
    data = {
        "customerID": [f"CUST{i}" for i in range(1, rows+1)],
        "gender": [random.choice(["Male", "Female"]) for _ in range(rows)],
        "SeniorCitizen": [random.choice([0,1]) for _ in range(rows)],
        "Partner": [random.choice(["Yes","No"]) for _ in range(rows)],
        "Dependents": [random.choice(["Yes","No"]) for _ in range(rows)],
        "tenure": [random.randint(1,72) for _ in range(rows)],
        "PhoneService": [random.choice(["Yes","No"]) for _ in range(rows)],
        "MultipleLines": [random.choice(["Yes","No","No phone service"]) for _ in range(rows)],
        "InternetService": [random.choice(["DSL","Fiber optic","No"]) for _ in range(rows)],
        "OnlineSecurity": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "OnlineBackup": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "DeviceProtection": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "TechSupport": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "StreamingTV": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "StreamingMovies": [random.choice(["Yes","No","No internet service"]) for _ in range(rows)],
        "Contract": [random.choice(["Month-to-month","One year","Two year"]) for _ in range(rows)],
        "PaperlessBilling": [random.choice(["Yes","No"]) for _ in range(rows)],
        "PaymentMethod": [random.choice(["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]) for _ in range(rows)],
        "MonthlyCharges": [round(random.uniform(20,120),2) for _ in range(rows)],
        "TotalCharges": [round(random.uniform(100,8000),2) for _ in range(rows)],
        "Churn": [random.choice(["Yes","No"]) for _ in range(rows)]
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_sample_data(200)
    df.to_csv("mock_data.csv", index=False)
    print("mock_data.csv created successfully!")
