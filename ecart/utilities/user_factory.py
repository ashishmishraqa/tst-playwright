from dataclasses import dataclass
from ecart.utilities.faker_helper import get_faker_generator


@dataclass
class RegistrationUser:
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    confirm_password: str


class UserFactory:
    def __init__(self):
        self.fake = get_faker_generator()

    def valid_registration_user(self):
        password = self.fake.generate_password()

        return RegistrationUser(
            first_name=self.fake.generate_first_name(),
            last_name=self.fake.generate_last_name(),
            email=self.fake.generate_email(),
            phone=self.fake.generate_phone(),
            password=password,
            confirm_password=password,
        )

    def user_with_mismatched_password(self):
        user = self.valid_registration_user()
        user.confirm_password = self.fake.generate_password()
        return user