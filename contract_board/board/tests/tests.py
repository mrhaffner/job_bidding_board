import platform
import random
import string

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType


class FunctionalTest(StaticLiveServerTestCase):
    """Tests the basic functionality of the bidding board."""

    def setUp(self):
        current_os = platform.platform()
        if 'linux' in current_os.lower():
            driver = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            service = ChromiumService(driver)
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            self.browser = webdriver.Chrome(service=service, options=options)
        else:
            self.browser = webdriver.Chrome()
        self.base_url = 'http://127.0.0.1:8000'

    def tearDown(self):
        self.browser.quit()

    def random_string(self, length):
        """Generates a random string of specified length/"""
        return ''.join(random.choices(string.ascii_letters, k=length))

    def random_date_string(self):
        """Generate a random date string in m/d/y format."""
        month = str(random.randint(1, 12))
        if len(month) == 1:
            month = '0' + month
        day = str(random.randint(1, 28))
        if len(day) == 1:
            day = '0' + day
        year = 23
        return f'{month}/{day}/{year}'

    def random_contract_dict(self, **kwargs):
        """
        Creates a contract dict with random values.
        You may use kwargs to overwrite individual keys.
        """
        contract = {
            'agency_name': self.random_string(10),
            'contact_information': self.random_string(10),
            'contract_title': self.random_string(10),
            'bidding_end_date': self.random_date_string(),
            'job_description': self.random_string(10),
        }
        for key, value in kwargs.items():
            contract[key] = value
        return contract

    def random_bid_dict(self, **kwargs):
        """
        Creates a bid with random values.
        You may use kwargs to overwrite individual keys.
        """
        bid = {
            'contractor_name': self.random_string(10),
            'contact_information': self.random_string(10),
            'amount': str(random.randint(1, 1000000))
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