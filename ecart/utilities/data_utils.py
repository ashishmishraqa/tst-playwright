import json
import os
import pathlib

"""A helper function which returns the list of test_data"""


def fetch_products():
    """load products data from the local JSON file."""
    data_path = pathlib.Path(__file__).parent.parent / "test_data" / "products.json"
    with open(data_path) as f:
        product_data = json.load(f)
        return product_data["products"]


def get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set.")
    return value
