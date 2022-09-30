import pygrametl
from pygrametl.tables import Dimension, FactTable

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


def main():
    pass
    # for row in inputdata:
    #     extractdomaininfo(row)
    #     extractserverinfo(row)
    #     row['size'] = pygrametl.getint(row['size']) # Convert to an int
    #     # Add the data to the dimension tables and the fact table
    #     row['pageid'] = pagesf.scdensure(row)
    #     row['dateid'] = datedim.ensure(row, {'date':'downloaddate'})
    #     row['testid'] = testdim.lookup(row, {'testname':'test'})
    #     facttbl.insert(row)
    # connection.commit()


if __name__ == '__main__':
    main()
