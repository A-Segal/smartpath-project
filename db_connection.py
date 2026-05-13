# import pyodbc
# SERVER = 'localhost'
# DATABASE = 'deliveryDB'
# DRIVER='ODBC Driver 17 for SQL Server'
# def get_connection():
#  conn_str = (
#  f'DRIVER={{{DRIVER}}};'
#  f'SERVER={SERVER};'
#  f'DATABASE={DATABASE};'
#  f'Trusted_Connection=yes;'
#  )
#
#
#  return pyodbc.connect(conn_str)
# conn = get_connection()
# cursor = conn.cursor()





from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SERVER = 'localhost'
DATABASE = 'deliveryDB'
DRIVER = 'ODBC Driver 17 for SQL Server'

# חיבור ל-SQL Server דרך SQLAlchemy
connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"
engine = create_engine(connection_string, echo=True)

# יצירת סשן
SessionLocal = sessionmaker(bind=engine)