from time import time, sleep

from pages.base_page import BasePage
from utilities.logger import get_logger


"""
Each Page class inherits Base Page classto inherit the basic actions 

"""
class RegisterPage(BasePage):


   log = get_logger(__name__)

   def __init__(self, page):
      super().__init__(page)

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
      self.enter_text(self.first_name,'august')
      self.enter_text(self.last_name,'hasting')
      self.enter_text(self.email,'august.hasting@ecart.com')
      self.enter_text(self.phone,'1239876178')
      self.enter_text(self.password,'August@12345')
      self.enter_text(self.confirm_password,'August@12345')
      self.agree_checkbox.click()
      self.continue_button.click()
