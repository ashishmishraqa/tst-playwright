from time import time, sleep

from pages.base_page import BasePage
from utilities.logger import get_logger
from utilities.faker_helper import get_faker_generator


"""
Each Page class inherits Base Page classto inherit the basic actions 

"""
class RegisterPage(BasePage):


   log = get_logger(__name__)

   def __init__(self, page):
      super().__init__(page)
      
      # Initialize faker for test data generation
      self.fake = get_faker_generator()

      # locators
      self.first_name = page.get_by_role('textbox', name='First Name')
      self.last_name = page.get_by_role('textbox', name='Last Name')
      self.email = page.get_by_role('textbox', name='E-Mail')
      self.phone = page.get_by_role('textbox', name='Telephone')
      self.password = page.locator('#input-password')
      self.confirm_password = page.get_by_role('textbox', name='Password Confirm')
      self.agree_checkbox = page.locator('[name="agree"]')
      self.continue_button = page.get_by_role('button', name='Continue')



    #---------------------
    #  Actions
    #---------------------

   def user_registration(self):
      """
      Register a new user with randomly generated faker data.
      Each registration will have unique user data.
      """
      first_name = self.fake.generate_first_name()
      last_name = self.fake.generate_last_name()
      email = self.fake.generate_email()
      phone = self.fake.generate_phone()
      password = self.fake.generate_password()
      
      self.enter_text(self.first_name, first_name)
      self.enter_text(self.last_name, last_name)
      self.enter_text(self.email, email)
      self.enter_text(self.phone, phone)
      self.enter_text(self.password, password)
      self.enter_text(self.confirm_password, password)
      self.agree_checkbox.click()
      self.continue_button.click()
      
      self.log.info(f"User registered successfully with email: {email}")
