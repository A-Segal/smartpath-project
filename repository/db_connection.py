import pyodbc
SERVER = 'localhost'
DATABASE = 'deliveryDB'
DRIVER='ODBC Driver 17 for SQL Server'
def get_connection():
 conn_str = (
 f'DRIVER={{{DRIVER}}};'
 f'SERVER={SERVER};'
 f'DATABASE={DATABASE};'
 f'Trusted_Connection=yes;'
 )


 return pyodbc.connect(conn_str)
conn = get_connection()
cursor = conn.cursor()

