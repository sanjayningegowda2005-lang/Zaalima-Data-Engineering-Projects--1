import pandas as pd
from sqlalchemy import create_engine
engine=create_engine('postgresql://postgres:c##cse@localhost:5432/project')
df=pd.read_sql("SELECT * FROM customers",engine)
 
 #for testing
<<<<<<< HEAD
print(df.info())
=======
print(df.head())
>>>>>>> 666a455bfbb73e1b215d14fd7257294973097653
