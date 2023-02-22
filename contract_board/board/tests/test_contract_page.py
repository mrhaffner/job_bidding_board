from datetime import date

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .tests import FunctionalTest


class ContractPageTest(FunctionalTest):
    """Tests the basic functionality of the contract page."""

    def validate_contract(self, contract_listing, contract_dict, bid=None):
        """
        Asserts that every item in a contract matches the correct item in a dictionary.
        The keys of the dictionary correspond to the "name" of the listing elements.
        For the contract on the contract.html page.
        """
        title = contract_listing.find_element(By.TAG_NAME, 'h2')
        self.assertEquals(title.text, contract_dict['contract_title'])
        name = contract_listing.find_element(By.CLASS_NAME, 'contract-agency-name')
        self.assertEquals(name.text, contract_dict['agency_name'])
        contact = contract_listing.find_element(By.CLASS_NAME, 'contract-contact-information')
        self.assertEquals(contact.text, contract_dict['contact_information'])
        end_date = contract_listing.find_element(By.CLASS_NAME, 'contract-bidding-end-date')
        self.assertEquals(end_date.text, contract_dict['bidding_end_date'])
        lowest_bid = contract_listing.find_element(By.CLASS_NAME, 'contract-lowest-bid')
        if bid is None:
            self.assertEquals(lowest_bid.text, 'None')
        else:
            self.assertEquals(float(lowest_bid.text[1:]), float(bid))
        description = contract_listing.find_element(By.CLASS_NAME, 'contract-job-description')
        self.assertEquals(description.text, contract_dict['job_description'])

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
        self.assertEquals(list_date.text, date.today().strftime('%m/%d/%y'))

    def test_contract_page(self):
        """"Tests the basic functionalities of adding bids to a contract."""
        # load a contract page
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024, 768)

        # create new contract
        contract1 = self.random_contract_dict()
        self.fill_form_from_dictionary(contract1)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)

        # go to new contract page
        contract_item = self.browser.find_elements(By.CLASS_NAME, 'contract-listing')[0]
        contract_link = contract_item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        self.browser.get(contract_link)

        # check contract contains correct information
        contract_listing = self.browser.find_element(By.ID, 'contract')
        self.validate_contract(contract_listing, contract1)

        # check bid form submission adds bid to contract
        number_bids1 = len(self.browser.find_elements(By.CLASS_NAME, 'bid-listing'))
        bid1 = self.random_bid_dict()
        self.fill_form_from_dictionary(bid1)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        number_bids2 = len(self.browser.find_elements(By.CLASS_NAME, 'bid-listing'))
        self.assertEqual(number_bids1, number_bids2 - 1)

        # check new bid contains correct information
        bid_listing = self.browser.find_element(By.CLASS_NAME, 'bid-listing')
        self.validate_bid_listing(bid_listing, bid1)

        # check adding second bid keeps bids in order
        bid2 = self.random_bid_dict()
        self.fill_form_from_dictionary(bid2)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        new_bid = self.browser.find_elements(By.CLASS_NAME, 'bid-listing')[0]
        contractor_name = new_bid.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(contractor_name.text, bid2['contractor_name'])

        # check lowest bid updates correctly
        contract_listing = self.browser.find_element(By.ID, 'contract')
        lowest_bid = str(min(float(bid1['amount']), float(bid2['amount'])))
        self.validate_contract(contract_listing, contract1, lowest_bid)

    def test_contractor_view(self):
        """Tests that a contractor can see the create bid form."""

    def test_contractee_view(self):
        """Tests that a contractee cannot see the create bid form."""

    def test_must_be_logged_in_to_visit(self):
        """Tests that an unauthenticated user is redirected to login page."""

    def test_cannot_submit_invalid_bid_form(self):
        pass