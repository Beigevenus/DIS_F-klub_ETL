import os
import psycopg2
import pygrametl
from dotenv import load_dotenv
from pygrametl.tables import Dimension, FactTable
from src import constants
from src.config import Config

load_dotenv()  # take environment variables from .env.

DB_NAME = os.environ[constants.DB_NAME]
DB_USER_NAME = os.environ[constants.DB_USER_NAME]
DB_HOST = os.environ[constants.DB_HOST]
DB_PASSWORD = os.environ[constants.DB_PASSWORD]

# Connection to target DW:
pgconn = psycopg2.connect(user=DB_USER_NAME, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)
connection = pygrametl.ConnectionWrapper(pgconn)
connection.setasdefault()
connection.execute('set search_path to f_klub')

# Dimensions
product_dim = Dimension(
    name='product',
    key='product_id',
    attributes=['category', 'name', 'price', 'is_active', 'deactivation_date'],
    lookupatts=['name']
)

member_dim = Dimension(
    name='member',
    key='member_id',
    attributes=['is_active']
)

location_dim = Dimension(
    name='location',
    key='location_id',
    attributes=["name"],
    lookupatts=['name']
)

time_dim = Dimension(
    name='time',
    key='time_id',
    attributes=['year', 'quarter', 'month', 'day', 'weekday', 'is_holiday', 'hour', 'minute'],
    lookupatts=['year', 'month', 'day', 'hour', 'minute']
)

# Fact Tables
sales_fact = FactTable(
    name='sales',
    keyrefs=['product_id', 'location_id', 'member_id', 'time_id'],
    measures=['total_sale']
)

inventory_fact = FactTable(
    name='inventory',
    keyrefs=['product_id', 'location_id', 'time_id'],
    measures=['number_of_units']
)