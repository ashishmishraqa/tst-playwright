import json
import pathlib

"""A helper function which returns the list of test_data"""


def fetch_products():
    """load products data from the local JSON file."""
    data_path = pathlib.Path(__file__).parent.parent / "test_data" / "products.json"
    with open(data_path) as f:
        product_data = json.load(f)
        return product_data["products"]
