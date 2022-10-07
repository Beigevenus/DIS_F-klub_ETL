import psycopg2 as psycopg2
import pygrametl
from pygrametl.datasources import CSVSource
from pygrametl.tables import Dimension, FactTable
import os
import constants
from config import Config
from dotenv import load_dotenv
import re
from typing import Dict
from datetime import datetime
from tqdm import tqdm
from copy import deepcopy

load_dotenv()  # take environment variables from .env.

DB_NAME = os.environ[constants.DB_NAME]
DB_USER_NAME = os.environ[constants.DB_USER_NAME]
DB_HOST = os.environ[constants.DB_HOST]
DB_PASSWORD = os.environ[constants.DB_PASSWORD]

TIMESTAMP_REGEX = "^([-]?[0-9]+)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) ([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(\+|-)(0[0-9]|1[0-2])$"

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


def clean_product_name(name: str):
    """ 
    Removes HTML tags.
    Removes trailing whitespace characters.
    """

    name = re.sub("<.*?>", "", name)

    if ("\"" in name):
        name = name.replace("\"", "")

    if (name.startswith(" ") or name.endswith(" ")):
        name = name.strip()

    return name


def clean_product_data(product_data):
    clean_product_data: list[dict[str, any]] = []

    # TODO: Figure out why product_data is destroyed.
    for row in product_data:
        # extractdomaininfo(row)
        # extractserverinfo(row)
        row_copy = deepcopy(row)
        row_copy['name'] = clean_product_name(row_copy['name'])

        clean_product_data.append(row_copy)

    return clean_product_data


def verify_timestamp(time: str) -> bool:
    if re.search(TIMESTAMP_REGEX, time):
        return True
    else:
        return False


def extract_attribute_values_from_timestamp(timestamp: str) -> Dict[str, any]:

    match_obj = re.search(TIMESTAMP_REGEX, timestamp)

    time_dim_row = {}
    if match_obj:
        time_dim_row["year"] = int(match_obj.group(1))
        time_dim_row['month'] = int(match_obj.group(2))
        time_dim_row['day'] = int(match_obj.group(3))
        time_dim_row['hour'] = int(match_obj.group(4))
        time_dim_row['minute'] = int(match_obj.group(5))

        time_dim_row['quarter'] = int(time_dim_row['month']) // 3 + 1
        time_dim_row['weekday'] = datetime(
            year=time_dim_row['year'],
            month=time_dim_row['month'],
            day=time_dim_row['day']
        ).strftime('%A')
        time_dim_row['is_holiday'] = False  # `is_holiday` not supported in this version.
    else:
        # Default to end of time
        time_dim_row.update({
            "year": 9999,
            "month": 12,
            "day": 31,
            "hour": 23,
            "minute": 59,
            "quarter": 4,
            "weekday": "Friday",
            "is_holiday": False
        })

    return time_dim_row


def insert_time_row(timestamp: str):

    row = extract_attribute_values_from_timestamp(timestamp)
    # print(row)
    time_dim.ensure(row)


def transform_timestamp(data, time_key: str):
    for row in tqdm(data):
        # print(row)
        if verify_timestamp(row[time_key]):
            insert_time_row(row[time_key])

    # [ insert_time_row(row[time_key]) if verify_timestamp(row[time_key]) else  for row in tqdm(data) ]


def find_category_id(product_id, product_category_data):
    for row in product_category_data:
        if row['product_id'] == product_id:
            return row['category_id']

    raise Exception(f"No category_id related to {product_id}")


def find_category_name(category_id, category_data):
    for row in category_data:
        if row['id'] == category_id:
            return row['name']

    raise Exception(f"Could not find category name from {category_id}")


def extract_product_dict(row, category_data, product_category_data):
    # 'category', 'is_active'
    product_dict = {}
    product_dict['name'] = row['name']
    product_dict['price'] = float(int(row['price']) / 100)  # price is measured in "øre".
    product_dict['is_active'] = bool(row['active'])

    product_id = row['id']

    try:
        category_id = find_category_id(product_id, product_category_data)
        product_dict['category'] = find_category_name(category_id, category_data)
    except Exception as e:
        print(f"Got exception {str(e)}")
        product_dict['category'] = "Uncategorized"

    time_dict = extract_attribute_values_from_timestamp(row['deactivate_date'])
    product_dict['deactivation_date'] = time_dim.ensure(time_dict)

    return product_dict


def construct_product_dim(product_data, category_data, product_category_data):

    for row in product_data:
        product_dict = extract_product_dict(row, category_data, product_category_data)
        print(product_dict)
        product_dim.ensure(product_dict)


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

    product_data = clean_product_data(product_data)

    # Verify that all timestamps are correct.
    # Transform all timestamps to Time representation.
    transform_timestamp(product_data, "deactivate_date")
    transform_timestamp(sale_data, "timestamp")

    transform()

    construct_product_dim(product_data, category_data, product_categories_data)

    for row in product_data:
        # print(row)
        # extractdomaininfo(row)
        # extractserverinfo(row)
        row['name']
        # row['size'] = pygrametl.getint(row['size']) # Convert to an int
        # # Add the data to the dimension tables and the fact table
        # row['pageid'] = pagesf.scdensure(row)
        # row['dateid'] = datedim.ensure(row, {'date':'downloaddate'})
        # row['testid'] = testdim.lookup(row, {'testname':'test'})
        # facttbl.insert(row)
    connection.commit()


if __name__ == '__main__':
    main()
