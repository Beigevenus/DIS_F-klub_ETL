from tqdm import tqdm
from dw_setup import (
    product_dim,
    time_dim,
    location_dim,
    member_dim,
    sales_fact,
    connection
)
from time_construction import extract_attribute_values_from_timestamp
from decimal import Decimal


def construct_sales_dict(row):
    sales_dict = {
        'member_id': member_dim.lookup({"lookup_id": int(row['member_id'])}),  # There's a problem here.
        'location_id': location_dim.lookup({"lookup_id": row['room_id']}),
        'product_id': product_dim.lookup({"lookup_id": row['product_id']}),
        'total_sale': float(int(row['price']) / 100),
    }

    existing_time_stamp = time_dim.lookup({"time_stamp": row['timestamp']})
    if existing_time_stamp:
        sales_dict['time_id'] = existing_time_stamp
    else:
        time_dict = extract_attribute_values_from_timestamp(row['timestamp'])
        sales_dict['time_id'] = time_dim.ensure(time_dict)

    return sales_dict


def transform_sales(sales_data):
    errors = 0
    duplicated_entries = 0
    for row in tqdm(sales_data, desc="Constructing Sales rows"):
        try:
            sales_dict = construct_sales_dict(row)

            fact_with_identical_entries_exists = sales_fact.lookup(sales_dict)
            if fact_with_identical_entries_exists:
                # Sales entries are assumed to have different timestamps.
                print("Should not happen.")
                duplicated_entries += 1

                new_accumulated_measure_row = fact_with_identical_entries_exists
                new_accumulated_measure_row['total_sale'] += Decimal(sales_dict['total_sale'])
                sales_fact.update(new_accumulated_measure_row)
            else:
                sales_fact.insert(sales_dict)

            connection.commit()
        except Exception as e:
            # If a transaction fails, consequtive use of the connection will be invalid.
            # A rollback can resolve this.
            connection.rollback()
            errors += 1
            # print(f"Sales fact error: {str(e)}.")

    print(f"Total errors: {errors}")
    print(f"Total diplicated entries: {duplicated_entries}")
