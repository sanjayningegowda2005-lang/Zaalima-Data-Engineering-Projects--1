from sqlalchemy import create_engine
def get_sqlite_engine(db_path="DATAB"):
    engine = create_engine("sqlite:///%s" % db_path)
    return engine
def get_postgre_engine(user="postgres",password="Harsha@1131",host="localhost",port=5432,db_name="mybd"):
    con_str="postgresql://%s:%s@%s/%s" % (user,password,host,port,db_name)
    engine = create_engine(con_str)
    return engine
def test_connection(engine):
    try:
        with engine.connect() as conn:
            print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)
if __name__ == "__main__":
    sql_engine=get_sqlite_engine("mydb.sqlite")
    print("sql engine created:", sql_engine)
    test_connection(sql_engine)
    postgre_engine=get_postgre_engine()
    print("postgreSQL engine created:",postgre_engine)
    test_connection(postgre_engine)




