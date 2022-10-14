import re
from datetime import datetime
from tqdm import tqdm
from dw_setup import time_dim

TIMESTAMP_REGEX = "^([-]?[0-9]+)-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) " \
                  "([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(\+|-)(0[0-9]|1[0-2])$"


def extract_attribute_values_from_timestamp(timestamp: str) -> dict[str, any]:
    match_obj = re.search(TIMESTAMP_REGEX, timestamp)

    time_dim_row = {}
    if match_obj:
        time_dim_row['time_stamp'] = timestamp
        time_dim_row["year"] = int(match_obj.group(1))
        time_dim_row['month'] = int(match_obj.group(2))
        time_dim_row['day'] = int(match_obj.group(3))
        time_dim_row['hour'] = int(match_obj.group(4))
        time_dim_row['minute'] = int(match_obj.group(5))
        time_dim_row['seconds'] = int(match_obj.group(6))

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
            'time_stamp': timestamp,
            "year": 9999,
            "month": 12,
            "day": 31,
            "hour": 23,
            "minute": 59,
            "seconds": 59,
            "quarter": 4,
            "weekday": "Friday",
            "is_holiday": False
        })

    return time_dim_row


def load_time(row):
    time_dim.ensure(row)


def transform_time(data, time_key: str):
    for row in tqdm(data, desc=f"Constructing Time rows for key '{time_key}'"):
        if verify_timestamp(row[time_key]):
            load_time(extract_attribute_values_from_timestamp(row[time_key]))


def verify_timestamp(time: str) -> bool:
    if re.search(TIMESTAMP_REGEX, time):
        return True
    else:
        return False
