from config import Config
from pathlib import Path
import pytest


class TestConfig:
    """ Tests that the Config class can read config files having the expected structure. """

    def setup_method(self):
        print('setting up')

        # 'test_config.ini' exhibits the structure which Config should be able to read.
        self.config = Config(
            file_name="test_config.ini",
            config_file_dir=str(Path(__file__).parent)
        )

    @pytest.mark.parametrize(
        "conf_obj_attr, expected_value",
        [
            ("data_folder_name", "data"),
            ("file_name_category", "category.csv"),
            ("file_name_members", "members.csv"),
            ("file_name_product_categories", "product_categories.csv"),
            ("file_name_product", "product.csv"),
            ("file_name_room", "room.csv"),
            ("file_name_sale", "sale.csv")
        ],
    )
    def test__When_test_config_read__Then_correct_value_exposed(self, conf_obj_attr, expected_value):
        """ Checks that all the public properties of the config object have the expected values. """

        actual_value = getattr(self.config, conf_obj_attr)

        assert actual_value == expected_value
