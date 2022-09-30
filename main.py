import psycopg2 as psycopg2
import pygrametl
from pygrametl.datasources import CSVSource
from pygrametl.tables import Dimension, FactTable

# Connection to target DW:
pgconn = psycopg2.connect(user='postgres', password='PASSWORD', host='127.0.0.1', database='f_klub')
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


def main():
    global connection

    product_data = CSVSource(open('data/product.csv', 'r', 16384, encoding='utf-8'),
                             delimiter=';')
    category_data = CSVSource(open('data/category.csv', 'r', 16384, encoding='utf-8'),
                              delimiter=';')
    member_data = CSVSource(open('data/member.csv', 'r', 16384, encoding='utf-8'),
                            delimiter=';')
    product_categories_data = CSVSource(open('data/product_categories.csv', 'r', 16384, encoding='utf-8'),
                                        delimiter=';')
    location_data = CSVSource(open('data/room.csv', 'r', 16384, encoding='utf-8'),
                              delimiter=';')
    sale_data = CSVSource(open('data/sale.csv', 'r', 16384, encoding='utf-8'),
                          delimiter=';')

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
