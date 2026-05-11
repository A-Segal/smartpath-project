

from datetime import datetime
from sqlalchemy import create_engine, text

# הגדרות החיבור
SERVER = 'localhost'
DATABASE = 'deliveryDB'
DRIVER = 'ODBC Driver 17 for SQL Server'

connection_string = f"mssql+pyodbc://@{SERVER}/{DATABASE}?driver={DRIVER.replace(' ', '+')}&trusted_connection=yes"
engine = create_engine(connection_string)

def create_recipient(fname, lname, username, password, mail, phone,
                     location_lat, location_lng, amount_of_meals, delivery_date):
    with engine.connect() as conn:
        conn.execute(
            text(
                "INSERT INTO recipient "
                "(fname, lname, username, password, mail, phone, "
                "location_lat, location_lng, amount_of_meals, delivery_date) "
                "VALUES (:fname, :lname, :username, :password, :mail, :phone, "
                ":location_lat, :location_lng, :amount_of_meals, :delivery_date)"
            ),
            {
                "fname": fname,
                "lname": lname,
                "username": username,
                "password": password,
                "mail": mail,
                "phone": phone,
                "location_lat": location_lat,
                "location_lng": location_lng,
                "amount_of_meals": amount_of_meals,
                "delivery_date": delivery_date
            }
        )
        conn.commit()
        print(f"Recipient {fname} added!")





def update_amount_of_meals(username, new_amount):
    with engine.connect() as conn:
        conn.execute(
            text("""
                UPDATE recipient
                SET amount_of_meals = :new_amount
                WHERE username = :username
            """),
            {"new_amount": new_amount, "username": username}
        )
        conn.commit()
        print(f"Updated amount_of_meals for {username} to {new_amount}!")


# דוגמאות לשימוש
create_recipient(
    "shani", "dan", "sd", "1133sd", "sd@gmail.com", "0546789876",
    32.0853, 34.7818, 5, datetime(2026, 5, 11, 14, 30)
)
update_amount_of_meals("shani", 20)
