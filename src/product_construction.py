import re
from copy import deepcopy
from tqdm import tqdm
from dw_setup import product_dim, time_dim
from time_construction import extract_attribute_values_from_timestamp


def clean_product_name(name: str):
    """
    Removes HTML tags.
    Removes trailing whitespace characters.
    """

    name = re.sub("<.*?>", "", name)

    if "\"" in name:
        name = name.replace("\"", "")

    if name.startswith(" ") or name.endswith(" "):
        name = name.strip()

    return name


def clean_product_data(product_data) -> list[dict[str, any]]:
    cleaned_product_data: list[dict[str, any]] = []

    # TODO: Figure out why product_data is destroyed.
    for row in product_data:
        row_copy = deepcopy(row)
        row_copy['name'] = clean_product_name(row_copy['name'])

        cleaned_product_data.append(row_copy)

    return cleaned_product_data


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


def construct_product_dict(row, category_data, product_category_data):
    product_dict = {
        'name': row['name'],
        'price': float(int(row['price']) / 100),
        'is_active': bool(row['active'])
    }

    product_id = row['id']

    try:
        category_id = find_category_id(product_id, product_category_data)
        product_dict['category'] = find_category_name(category_id, category_data)
    except Exception as e:
        # print(f"Got exception {str(e)}")
        product_dict['category'] = "Uncategorized"

    time_dict = extract_attribute_values_from_timestamp(row['deactivate_date'])
    product_dict['deactivation_date'] = time_dim.ensure(time_dict)

    return product_dict


def transform_product(product_data, category_data, product_category_data):
    for row in tqdm(product_data, desc="Constructing Product rows"):
        product_dict = construct_product_dict(row, category_data, product_category_data)
        product_dim.ensure(product_dict)
