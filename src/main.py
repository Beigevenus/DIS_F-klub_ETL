from pygrametl.datasources import CSVSource
from config import Config
from src.product_construction import clean_product_data, transform_product
from src.time_construction import transform_time
import dw_setup

config = Config()


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

    # Create lists from DictReaders and populate them cause we don't know how to work with readers
    product_categories_data_list: list = []
    category_data_list: list = []

    for entry in product_categories_data:
        product_categories_data_list.append(entry)

    for entry in category_data:
        category_data_list.append(entry)

    # Clean product data
    product_data = clean_product_data(product_data)

    # Verify that timestamps are valid and populate time table
    transform_time(product_data, "deactivate_date")
    transform_time(sale_data, "timestamp")

    # Populate product table
    transform_product(product_data, category_data, product_categories_data_list)

    dw_setup.connection.commit()


if __name__ == '__main__':
    main()
