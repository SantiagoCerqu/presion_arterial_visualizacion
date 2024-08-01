import os
from dotenv import load_dotenv 
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Load environment variables from .env
load_dotenv()
db_info = os.getenv("DATABASE_INFO_2") 

# Conection string for sqlalchemy, and declare the engine with the string
con_string = f"postgresql://{db_info}"
engine = create_engine(con_string)

# SQL queries para el usuario 1
user = 1

# Get all the medical records for especific user
query_1 = f"""
    SELECT * FROM medical_records
    WHERE user_id =
"""
# Get all the personal information from especific user
query_2 = f"""
    SELECT * FROM users
    WHERE id =
"""

# Get medical record for especific user and create a DataFrame with the data
def get_user_medical_records(user_id):
    query = query_1 + f"{user_id};"
    return pd.read_sql_query(query, engine)

def get_user_information(user_id):
    query = query_2 + f"{user_id};"
    return pd.read_sql_query(query, engine)


# Set birthdate and actual date to calculate the user age
def calc_age(user_df) -> int:
    # Change the birthdate from object to date data type and 
    user_df["birthdate"] = pd.to_datetime(user_df["birthdate"])
    birthdate = user_df["birthdate"][0].date()
    today_date = datetime.now().date()
    return relativedelta(today_date, birthdate).years


