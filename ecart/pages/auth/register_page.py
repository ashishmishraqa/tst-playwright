from pages.base_page import BasePage
from utilities.logger import get_logger

"""
Each Page class inherits Base Page classto inherit the basic actions like click, enter text, get text, etc.
"""
class RegisterPage(BasePage):

   log = get_logger(__name__)

   def __init__(self, page):
      super().__init__(page)

   @property
   def first_name(self):
       return self.page.get_by_role('textbox', name='First Name')

   @property
   def last_name(self):
       return self.page.get_by_role('textbox', name='Last Name')

   @property
   def email(self):
       return self.page.get_by_role('textbox', name='E-Mail')

   @property
   def phone(self):
       return self.page.get_by_role('textbox', name='Telephone')

   @property
   def password(self):
       return self.page.locator('#input-password')

   @property
   def confirm_password(self):
       return self.page.get_by_role('textbox', name='Password Confirm')

   @property
   def agree_checkbox(self):
       return self.page.locator('[name="agree"]')

   @property
   def continue_button(self):
       return self.page.get_by_role('button', name='Continue')

    #---------------------
    #  Actions
    #---------------------


   def register_user(self, user):
      """
      Register a new user with randomly generated faker data.
      Each registration will have unique user data.
      """
      self.enter_text(self.first_name, user.first_name)
      self.enter_text(self.last_name, user.last_name)
      self.enter_text(self.email, user.email)
      self.enter_text(self.phone, user.phone)
      self.enter_text(self.password, user.password)
      self.enter_text(self.confirm_password, user.confirm_password)
      self.click_on(self.agree_checkbox)
      self.click_on(self.continue_button)

      self.log.info(f"User registered successfully with email: {user.email} ")
