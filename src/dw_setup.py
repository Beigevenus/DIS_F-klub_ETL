import os
import psycopg2
import pygrametl
from dotenv import load_dotenv
from pygrametl.tables import (
    Dimension,
    FactTable,
    AccumulatingSnapshotFactTable
)
import constants

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
    attributes=['lookup_id', 'category', 'name', 'price', 'is_active', 'deactivation_date'],
    lookupatts=['lookup_id']
)

member_dim = Dimension(
    name='member',
    key='member_id',  # This id is auto generated.
    attributes=['lookup_id', 'is_active'],  # `lookup_id` is from from the data and makes lookup possible.
    lookupatts=['lookup_id']
)

location_dim = Dimension(
    name='location',
    key='location_id',
    attributes=['lookup_id', 'name'],
    lookupatts=['lookup_id']
)

time_dim = Dimension(
    name='time',
    key='time_id',
    attributes=['time_stamp', 'year', 'quarter', 'month', 'day', 'weekday', 'is_holiday', 'hour', 'minute', 'seconds'],
    lookupatts=['time_stamp']
)

# Fact Tables
sales_fact = AccumulatingSnapshotFactTable(
    name='sales',
    otherrefs=[],
    keyrefs=['product_id', 'location_id', 'member_id', 'time_id'],
    measures=['total_sale']
)

inventory_fact = FactTable(
    name='inventory',
    keyrefs=['product_id', 'location_id', 'time_id'],
    measures=['number_of_units']
)
