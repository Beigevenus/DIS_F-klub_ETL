import pytest
from main import (
    clean_product_name,
    extract_attribute_values_from_timestamp,
    extract_product_dict
)


@pytest.mark.parametrize(
    "input_str, expected_str",
    [
        ("<h2> Fyttetur </h2>", "Fyttetur"),
    ],
)
def test__clean_product_name(input_str, expected_str):

    actual_str = clean_product_name(input_str)

    assert actual_str == expected_str


@pytest.mark.parametrize(
    "input_str, expected_dict",
    [
        (
            "2017-04-28 01:59:00+02",
            {
                "year": 2017,
                "month": 4,
                "day": 28,
                "hour": 1,
                "minute": 59,
                "quarter": 2,
                "weekday": "Friday",
                "is_holiday": False
            }
        ),
    ],
)
def test__extract_attribute_values_from_timestamp(input_str, expected_dict):

    actual_dict = extract_attribute_values_from_timestamp(input_str)

    assert actual_dict == expected_dict


# @pytest.mark.parametrize(
#     "input_dict, expected_dict",
#     [
#         (
#             {
#                 'id': ,
#                 'name': ,
#                 'price': ,
#                 'active': ,
#                 'deactivate_date': ,
#                 'quantity': ,
#                 'alcohol_content_ml': ,
#                 'start_date':
#             },
#             {
#                 'category': ,
#                 'name': ,
#                 'price': ,
#                 'is_active': ,
#                 'deactivation_date':
#             }
#         ),
#     ],
# )
# def test__extract_product_dict(input_dict, expected_dict):

#     actual_dict = extract_product_dict(input_dict)

#     assert actual_dict == expected_dict
