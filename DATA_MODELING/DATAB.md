erDiagram
    CUSTOMER_CHURN {
        VARCHAR(50) customerID PK
        VARCHAR(10) gender
        INT SeniorCitizen
        VARCHAR(10) Partner
        VARCHAR(10) Dependents
        INT tenure
        VARCHAR(10) PhoneService
        VARCHAR(10) MultipleLines
        VARCHAR(20) InternetService
        VARCHAR(10) OnlineSecurity
        VARCHAR(10) OnlineBackup
        VARCHAR(10) DeviceProtection
        VARCHAR(10) TechSupport
        VARCHAR(10) StreamingTV
        VARCHAR(10) StreamingMovies
        VARCHAR(20) Contract
        VARCHAR(10) PaperlessBilling
        VARCHAR(50) PaymentMethod
        FLOAT MonthlyCharges
        FLOAT TotalCharges
        VARCHAR(10) Churn
    }

    API_RESPONSE_STAGING {
        SERIAL id PK
        VARCHAR(100) source
        JSONB response_json
        INT status_code
        TIMESTAMP fetched_at
        BOOLEAN processed
    }

    AUDIT_LOG {
        SERIAL id PK
        VARCHAR(100) table_name
        INT row_count
        VARCHAR(20) status
        TIMESTAMP logged_at
    }

    CUSTOMER_CHURN ||--o{ AUDIT_LOG : "operations logged"
    API_RESPONSE_STAGING ||--o{ AUDIT_LOG : "responses logged"
