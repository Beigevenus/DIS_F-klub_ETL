from tqdm import tqdm
from dw_setup import member_dim


def transform_member(member_data):
    member_dict: dict = {}

    for row in tqdm(member_data, desc="Constructing Member rows"):
        member_dict["is_active"] = row["active"]
        member_dim.ensure(member_dict)
