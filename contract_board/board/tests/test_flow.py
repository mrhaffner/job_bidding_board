import platform
import random
import string
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


class FlowTest(StaticLiveServerTestCase):
    """Tests the basic functionality of the bidding board."""

    def setUp(self):
        current_os = platform.platform()
        if "linux" in current_os.lower():
            driver = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            service = ChromiumService(driver)
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            self.browser = webdriver.Chrome(service=service, options=options)
        else:
            self.browser = webdriver.Chrome()
        self.base_url = "http://127.0.0.1:8000/"

    def tearDown(self):
        self.browser.quit()

    def random_string(self, length):
        """Generates a random string of specified length"""
        return "".join(random.choices(string.ascii_letters, k=length))

    def random_bid_dict(self, **kwargs):
        """
        Creates a bid with random values.
        You may use kwargs to overwrite individual keys.
        """
        bid = {
            "contractor_name": self.random_string(10),
            "contact_information": self.random_string(10),
            "amount": str(random.randint(1, 1000000))
        }
        for key, value in kwargs.items():
            bid[key] = value
        return bid

    def fill_form_from_dictionary(self, form_data):
        """
        Fills in a form from a dictionary and submits that form.
        The keys of the dictionary correspond to the "name" of the form elements.
        """
        for name, value in form_data.items():
            element = self.browser.find_element(By.NAME, name)
            element.send_keys(value)

    def random_user_dict(self):
        """Creates a user with random values."""
        return {
            "username": self.random_string(5),
            "email": self.random_string(3) + "@" + self.random_string(3) + ".com",
            "agency_name": self.random_string(5),
            "password1": self.random_string(8)
        }

    def fill_user_form_from_dicitonary(self, user_dict, user_type):
        """Fills the user registration form from a dictionary."""
        self.fill_form_from_dictionary(user_dict)
        password2 = self.browser.find_element(By.NAME, "password2")
        password2.send_keys(user_dict["password1"])
        dropdown = self.browser.find_element(By.NAME, "type")
        select = Select(dropdown)
        select.select_by_value(user_type)

    def test_basic_flow(self):
        # go to registration page
        self.browser.get(self.base_url + "register")
        self.browser.set_window_size(1024, 768)

        # create contractee account
        time.sleep(2)
        user_dict = self.random_user_dict()
        self.fill_user_form_from_dicitonary(user_dict, "CONTRACTEE")
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # check you are redirected to login page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "accounts/login/")

        # login
        login_dict = {"username": user_dict["username"], "password": user_dict["password1"]}
        self.fill_form_from_dictionary(login_dict)
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # check you are redirected to contract list page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url)

        # keep track of number of contracts for later
        number_contracts1 = len(self.browser.find_elements(By.CLASS_NAME, "contract"))

        # click button to navigate to create contract page
        create_button = self.browser.find_element(By.ID, "create-contract")
        create_button.click()

        # check that you are on create contract page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "contract/new")

        # create a contract
        contract_dict = {
            "contract_title": self.random_string(10),
            "bidding_end_date": "11/11/50",
            "job_description": self.random_string(20),
        }
        self.fill_form_from_dictionary(contract_dict)
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # check that redirected to contract list page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url)

        # check that there is one more contract
        number_contracts2 = len(self.browser.find_elements(By.CLASS_NAME, "contract"))
        self.assertEqual(number_contracts1, number_contracts2 - 1)

        # logout
        logout_button = self.browser.find_element(By.ID, "logout")
        logout_button.click()

        # check redirected to login page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "accounts/login/")

        # navigate to register page
        self.browser.get(self.base_url + "register")

        # create contractor account
        time.sleep(2)
        user_dict = self.random_user_dict()
        self.fill_user_form_from_dicitonary(user_dict, "CONTRACTOR")
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # login
        time.sleep(2)
        login_dict = {"username": user_dict["username"], "password": user_dict["password1"]}
        self.fill_form_from_dictionary(login_dict)
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # navigate to contract
        time.sleep(2)
        contract = self.browser.find_element(By.CLASS_NAME, "contract")
        contract.click()

        # check directed to contract page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "contract/1")

        # keep track of number of bids for later
        number_bids1 = len(self.browser.find_elements(By.CLASS_NAME, "bid"))

        # navigate to create bid page
        create_button = self.browser.find_element(By.ID, "create-bid")
        create_button.click()

        # check directed to create bid page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "contract/1/bid")

        # place a bid
        self.fill_form_from_dictionary({"amount": "100"})
        submit_button = self.browser.find_element(By.ID, "submit")
        submit_button.send_keys(Keys.RETURN)

        # check redirected to contract page
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.base_url + "contract/1")

        # check that there is one more bid
        number_bids2 = len(self.browser.find_elements(By.CLASS_NAME, "bid"))
        self.assertEqual(number_bids1, number_bids2 - 1)