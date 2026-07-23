"""
Centralized Faker utility for generating test data across all pages.
Single source of truth for all mock data generation.
"""

import random
import string

from faker import Faker


class FakerDataGenerator:
    """
    Reusable fake data generator for test automation.
    Provides methods for generating consistent test data across multiple pages.
    """

    def __init__(self, locale="en_US"):
        """
        Initialize Faker with specified locale.

        Args:
            locale (str): Locale for faker (default: en_US for US English)
        """
        self.fake = Faker(locale)

    def generate_first_name(self):
        """Generate random first name."""
        return self.fake.first_name()

    def generate_last_name(self):
        """Generate random last name."""
        return self.fake.last_name()

    def generate_email(self):
        """Generate random email address."""
        return self.fake.email()

    def generate_phone(self):
        """
        Generate random 10-digit phone number.
        Format: 1239876178 (numeric only)
        """
        return self.fake.numerify(text="##########")

    def generate_password(self, length=12):
        """
        Generate a secure password with uppercase, lowercase, numbers, and special chars.

        Args:
            length (int): Password length (default: 12)

        Returns:
            str: Secure password (e.g., 'Ks7@mP9xRt2Q')
        """
        characters = (
            string.ascii_uppercase
            + string.ascii_lowercase
            + string.digits
            + string.punctuation
        )
        password = "".join(random.choice(characters) for _ in range(length))
        return password

    def generate_user_registration_data(self):
        """
        Generate complete user registration data (all fields together).
        Useful for data-driven tests and fixtures.

        Returns:
            dict: Dictionary with all user registration fields
        """
        password = self.generate_password()

        return {
            "first_name": self.generate_first_name(),
            "last_name": self.generate_last_name(),
            "email": self.generate_email(),
            "phone": self.generate_phone(),
            "password": password,
            "confirm_password": password,
        }

    def generate_go_rest_post_body(self):
        return {
            "name": self.fake.name(),
            "email": self.fake.email(),
            "gender": "male",
            "status": "active",
        }


# Singleton instance for simple usage
_faker_instance = None


def get_faker_generator(locale="en_US"):
    """
    Get or create a singleton Faker generator instance.

    Args:
        locale (str): Locale for faker (default: en_US)

    Returns:
        FakerDataGenerator: Faker generator instance
    """
    global _faker_instance
    if _faker_instance is None:
        _faker_instance = FakerDataGenerator(locale)
    return _faker_instance
