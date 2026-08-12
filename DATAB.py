from sqlalchemy import create_engine
def get_sqlite_engine(db_path="DATAB"):
    engine = create_engine("sqlite:///%s" % db_path)
    return engine
def get_postgre_engine(user="postgres",password="Harsha@1131",host="localhost",port=5432,db_name="mybd"):
    con_str="postgresql://%s:%s@%s/%s" % (user,password,host,port,db_name)
    engine = create_engine(con_str)
    return engine
if __name__=="main":
    sql_engine=get_sqlite_engine("mydb.sqlite")
    print("sql engine created:", sql_engine)
    postgre_engine=get_postgre_engine()
    print("postgreSQL engine created:",postgre_engine)



