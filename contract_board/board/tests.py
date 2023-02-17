from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


CONTRACT_DATA1 = {
    'agency_name': 'Rail Corp',
    'contact_information': '777-555-3333',
    'contract_title': 'Build a train house',
    'bidding_end_date': '3/12/23',
    'job_description': 'Build a home for our new train named Steve'
}

CONTRACT_DATA2 = {
    'agency_name': 'Big Bank',
    'contact_information': '222-777-3333',
    'contract_title': 'Create a parking ramp',
    'bidding_end_date': '3/20/23',
    'job_description': 'More parking = more customers'
}

BID_DATA1 = {
    'contractor_name': 'Don Johnson',
    'contact_information': '111-222-3333',
    'amount': '300.00'
}

BID_DATA2 = {
    'contractor_name': 'Big Mike',
    'contact_information': '222-999-3333',
    'amount': '250.00'
}


class FunctionalTest(StaticLiveServerTestCase):
    """Tests the basic functionality of the bidding board."""

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.base_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.browser.quit()

    def fill_form_from_dictionary(self, form_data):
        """
        Fills in a form from a dictionary and submits that form.
        The keys of the dictionary correspond to the "name" of the form elements.
        """
        for name, value in form_data.items():
            element = self.browser.find_element(By.NAME, name)
            element.send_keys(value)

    def validate_contract_listing(self, contract_listing, contract):
        """
        Asserts that every item in a form listing matches the correct item in a data dictionary.
        The keys of the dictionary correspond to the "name" of the listing elements.
        """
        title = contract_listing.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(title.text, contract['contract_title'])
        name = contract_listing.find_element(By.CLASS_NAME, 'listing-agency-name')
        self.assertEquals(name.text, contract['agency_name'])
        end_date = contract_listing.find_element(By.CLASS_NAME, 'listing-bidding-end-date')
        self.assert_date_equality(end_date.text, contract['bidding_end_date'])
        lowest_bid = contract_listing.find_element(By.CLASS_NAME, 'listing-lowest-bid')
        self.assertEquals(lowest_bid.text, 'None')
        number_bids = contract_listing.find_element(By.CLASS_NAME, 'listing-number-bids')
        self.assertEquals(number_bids.text, '0')

    def assert_date_equality(self, str_date, number_date):
        """Asserts that two date strings of specified format are equal."""
        date_object_1 = datetime.strptime(number_date, '%m/%d/%y')
        date_object_2 = datetime.strptime(str_date, '%B %d, %Y')
        self.assertEqual(date_object_1, date_object_2)

    def test_contract_list_page(self):
        """"Tests the basic functionalities of adding contracts to the contract board."""
        # load the page
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024, 768)
        title = self.browser.find_element(By.CLASS_NAME, 'title')

        # check layout/style - test html/css loads properly - smoke test
        self.assertAlmostEqual(
            title.location['x'] + title.size['width'] / 2,
            1008 / 2,  # screen actual width / 2
            delta=10
        )

        # check contract form submission adds a contract to board
        number_contracts_1 = len(self.browser.find_elements(By.CLASS_NAME, 'contract-listing'))
        contract = CONTRACT_DATA1
        self.fill_form_from_dictionary(contract)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        number_contracts_2 = len(self.browser.find_elements(By.CLASS_NAME, 'contract-listing'))
        self.assertEqual(number_contracts_1, number_contracts_2 - 1)

        # check new contract contains correct information
        first_contract = self.browser.find_element(By.CLASS_NAME, 'contract-listing')
        self.validate_contract_listing(first_contract, contract)

        # check adding second contract keeps contracts in order
        # check clicking contract redirects to correct contract page (use most recent contract)

    def test_contract_page(self):
        """"Tests the basic functionalities of adding bids to a contract."""
        # load a contract page
        self.browser.get(self.base_url + '/contract/2')
        self.browser.set_window_size(1024, 768)

        # check layout/style of contract page
        # check contract contains correct information
        # check bid form submission adds bid to contract
        # check new bid contains correct information
        # check adding second bid keeps bids in order
        # check number of bids updates correctly on contract list page
        # check lowest bid updates correctly on contract list page

    def test_404_page(self):
        # load an invalid page
        self.browser.get(self.base_url + '/sdfsdfgsdfg')
        self.browser.set_window_size(1024, 768)

        # check layout/style of 404 page
        # check that the page link to the home page (not in the header)

    def test_cannot_submit_invalid_contract_form(self):
        # load contract list page
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024, 768)

        # check that a new contract is not added to page

    def test_cannot_submit_invalid_bid_form(self):
        # load contract list page
        self.browser.get(self.base_url + '/contract/1')
        self.browser.set_window_size(1024, 768)

        # check that a new bid is not added to page

        def test_cannot_submit_invalid_contract_form(self):
    """Test that an invalid contract form cannot be submitted and no new contract is added to the list.

    This test loads the contract list page, clicks the "Add Contract" button, and fills in the form with missing
    required fields, then submits the form. It checks that the form was not submitted and no new contract was added
    to the list, by verifying that the number of contracts in the list is zero.

    """
    # Load the contract list page
    self.browser.get(self.base_url)
    self.browser.set_window_size(1024, 768)

    # Click the "Add Contract" button
    add_contract_button = self.browser.find_element_by_id('add-contract')
    add_contract_button.click()

    # Fill in the form with an invalid input (missing required fields)
    form = self.browser.find_element_by_tag_name('form')
    input_name = form.find_element_by_name('name')
    input_name.clear()
    input_description = form.find_element_by_name('description')
    input_description.clear()
    input_start_date = form.find_element_by_name('start_date')
    input_start_date.clear()
    input_end_date = form.find_element_by_name('end_date')
    input_end_date.clear()

    # Submit the form
    submit_button = form.find_element_by_tag_name('button')
    submit_button.click()

    # Check that the form was not submitted and no new contract was added to the list
    contracts = self.browser.find_elements_by_css_selector('.contract')
    self.assertEqual(len(contracts), 0)

def test_cannot_submit_invalid_bid_form(self):
    """Test that an invalid bid form cannot be submitted and no new bid is added to the page.

    1. Load the contract page for the first contract in the list.
    2. Click the "Add Bid" button.
    3. Fill in the form with an invalid input (missing required fields).
    4. Submit the form.
    5. Check that the form was not submitted and no new bid was added to the page.
    """
    # Load the contract detail page
    self.browser.get(self.base_url + '/contract/1')
    self.browser.set_window_size(1024, 768)

    # Click the "Add Bid" button
    add_bid_button = self.browser.find_element_by_id('add-bid')
    add_bid_button.click()

    # Fill in the form with an invalid input (missing required fields)
    form = self.browser.find_element_by_tag_name('form')
    input_description = form.find_element_by_name('description')
    input_description.clear()
    input_amount = form.find_element_by_name('amount')
    input_amount.clear()

    # Submit the form
    submit_button = form.find_element_by_tag_name('button')
    submit_button.click()

    # Check that the form was not submitted and no new bid was added to the list
    bids = self.browser.find_elements_by_css_selector('.bid')
    self.assertEqual(len(bids), 0)
def test_404_page(self):
    """
    Test that attempting to access a non-existent page results in a 404 error page.
    """
    # Try to load a non-existent page
    self.browser.get(self.base_url + '/nonexistent-page')

    # Check that the page title and content indicates a 404 error
    self.assertIn('Page not found', self.browser.title)
    heading = self.browser.find_element_by_tag_name('h1')
    self.assertIn('Page not found', heading.text)