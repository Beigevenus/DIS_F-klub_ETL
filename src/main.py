import psycopg2 as psycopg2
import pygrametl
from pygrametl.datasources import CSVSource
from pygrametl.tables import Dimension, FactTable
import os
import constants
from config import Config
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

DB_NAME = os.environ[constants.DB_NAME]
DB_USER_NAME = os.environ[constants.DB_USER_NAME]
DB_HOST = os.environ[constants.DB_HOST]
DB_PASSWORD = os.environ[constants.DB_PASSWORD]

config = Config()


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
    attributes=['year', 'quarter', 'month', 'day', 'weekday', 'is_holiday', 'time_of_day'],
    lookupatts=['year', 'month', 'day', 'time_of_day']
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


def clean():
    pass


def transform():
    pass


def read_from_csv_file(relative_path_to_file, mode="r", buffering=16384, encoding="utf-8", delimiter=";"):
    """ Utility function for reading data from a CSV file. """

    from pathlib import Path
    project_dir_path = Path(__file__).parent.parent.resolve()
    abs_path_to_file = str(Path.joinpath(project_dir_path, relative_path_to_file))
    return CSVSource(open(abs_path_to_file, mode, buffering, encoding=encoding), delimiter=delimiter)


def get_csv_file_path(file_name, data_folder_name=config.data_folder_name):
    """ Utility function for constructing relative CSV file path based on convention 
        that CSV files exist in `<project_root>/data_folder_name`. """

    return f"{data_folder_name}/{file_name}"


def main():
    global connection

    product_data = read_from_csv_file(
        get_csv_file_path(config.file_name_product)
    )
    category_data = read_from_csv_file(
        get_csv_file_path(config.file_name_category)
    )
    member_data = read_from_csv_file(
        get_csv_file_path(config.file_name_members)
    )
    product_categories_data = read_from_csv_file(
        get_csv_file_path(config.file_name_product_categories)
    )
    location_data = read_from_csv_file(
        get_csv_file_path(config.file_name_room)
    )
    sale_data = read_from_csv_file(
        get_csv_file_path(config.file_name_sale)
    )

    clean()
    transform()

    for row in product_data:
        print(row)
        # extractdomaininfo(row)
        # extractserverinfo(row)
        # row['size'] = pygrametl.getint(row['size']) # Convert to an int
        # # Add the data to the dimension tables and the fact table
        # row['pageid'] = pagesf.scdensure(row)
        # row['dateid'] = datedim.ensure(row, {'date':'downloaddate'})
        # row['testid'] = testdim.lookup(row, {'testname':'test'})
        # facttbl.insert(row)
    connection.commit()


if __name__ == '__main__':
    main()
