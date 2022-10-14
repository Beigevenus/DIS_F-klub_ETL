from tqdm import tqdm
from dw_setup import location_dim


def transform_location(location_data):
    location_dict: dict = {}

    for row in tqdm(location_data, desc="Constructing Location rows"):
        location_dict["lookup_id"] = row["id"]
        location_dict["name"] = row["name"]
        location_dim.ensure(location_dict)
