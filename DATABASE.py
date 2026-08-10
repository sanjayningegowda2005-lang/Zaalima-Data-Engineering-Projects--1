import pandas as pd
from sqlalchemy import create_engine
engine=create_engine('postgresql://postgres:c##cse@localhost:5432/project')
df=pd.read_sql("SELECT * FROM customers",engine)
 
 #for testing
print(df.info())
