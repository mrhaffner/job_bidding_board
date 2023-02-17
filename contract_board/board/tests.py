from datetime import date, datetime
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

    def validate_contract_listing(self, contract_listing, contract, num_bids=0, low_bid='None'):
        """
        Asserts that every item in a contract listing matches the correct item in a dictionary.
        The keys of the dictionary correspond to the "name" of the listing elements.
        """
        title = contract_listing.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(title.text, contract['contract_title'])
        name = contract_listing.find_element(By.CLASS_NAME, 'listing-agency-name')
        self.assertEquals(name.text, contract['agency_name'])
        end_date = contract_listing.find_element(By.CLASS_NAME, 'listing-bidding-end-date')
        self.assert_date_equality(end_date.text, contract['bidding_end_date'])
        lowest_bid = contract_listing.find_element(By.CLASS_NAME, 'listing-lowest-bid')
        if low_bid != 'None':
            self.assertEquals(float(lowest_bid.text[1:]), low_bid)
        else:
            self.assertEquals(lowest_bid.text, low_bid)
        number_bids = contract_listing.find_element(By.CLASS_NAME, 'listing-number-bids')
        self.assertEquals(number_bids.text, str(num_bids))

    def validate_bid_listing(self, bid_listing, bid):
        """
        Asserts that every item in a contract listing matches the correct item in a dictionary.
        The keys of the dictionary correspond to the "name" of the listing elements.
        """
        title = bid_listing.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(title.text, bid['contractor_name'])
        amount = bid_listing.find_element(By.CLASS_NAME, 'bid-amount')
        self.assertEquals(float(amount.text[1:]), + float(bid['amount']))
        contact = bid_listing.find_element(By.CLASS_NAME, 'bid-contact-information')
        self.assertEquals(contact.text, bid['contact_information'])
        list_date = bid_listing.find_element(By.CLASS_NAME, 'bid-date-placed')
        self.assert_date_equality(list_date.text)

    def assert_date_equality(self, str_date, number_date=None):
        """Asserts that two date strings of specified format are equal."""
        if number_date:
            date_object_1 = datetime.strptime(number_date, '%m/%d/%y').date()
        else:
            date_object_1 = date.today()
        try:
            date_object_2 = datetime.strptime(str_date, '%B %d, %Y').date()
        except ValueError:
            date_object_2 = datetime.strptime(str_date, '%b. %d, %Y').date()
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
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024, 768)

        # create new contract
        contract = CONTRACT_DATA1
        self.fill_form_from_dictionary(contract)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)

        # go to new contract page
        contract_item = self.browser.find_elements(By.CLASS_NAME, 'contract-listing')[0]
        contract_link = contract_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        self.browser.get(contract_link)

        # check contract contains correct information
        contract_listing = self.browser.find_element(By.ID, 'contract')

        title = contract_listing.find_element(By.TAG_NAME, 'h2')
        self.assertEquals(title.text, contract['contract_title'])
        name = contract_listing.find_element(By.CLASS_NAME, 'contract-agency-name')
        self.assertEquals(name.text, contract['agency_name'])
        contact = contract_listing.find_element(By.CLASS_NAME, 'contract-contact-information')
        self.assertEquals(contact.text, contract['contact_information'])
        end_date = contract_listing.find_element(By.CLASS_NAME, 'contract-bidding-end-date')
        self.assert_date_equality(end_date.text, contract['bidding_end_date'])
        lowest_bid = contract_listing.find_element(By.CLASS_NAME, 'contract-lowest-bid')
        self.assertEquals(lowest_bid.text, 'None')
        description = contract_listing.find_element(By.CLASS_NAME, 'contract-job-description')
        self.assertEquals(description.text, contract['job_description'])

        # check bid form submission adds bid to contract
        number_bids1 = len(self.browser.find_elements(By.CLASS_NAME, 'bid-listing'))
        bid = BID_DATA1
        self.fill_form_from_dictionary(bid)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        number_bids2 = len(self.browser.find_elements(By.CLASS_NAME, 'bid-listing'))
        self.assertEqual(number_bids1, number_bids2 - 1)

        # check new bid contains correct information
        bid_listing = self.browser.find_element(By.CLASS_NAME, 'bid-listing')
        self.validate_bid_listing(bid_listing, bid)

        # check adding second bid keeps bids in order
        bid = BID_DATA2
        self.fill_form_from_dictionary(bid)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        new_bid = self.browser.find_elements(By.CLASS_NAME, 'bid-listing')[0]
        contractor_name = new_bid.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(contractor_name.text, bid['contractor_name'])

        # check number and lowest of bid updates correctly on contract list page
        self.browser.get(self.base_url)
        first_contract = self.browser.find_element(By.CLASS_NAME, 'contract-listing')
        lowest_bid = min(float(BID_DATA1['amount']), float(BID_DATA2['amount']))
        self.validate_contract_listing(first_contract, contract, 2, lowest_bid)

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