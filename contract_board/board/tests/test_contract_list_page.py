from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .tests import FunctionalTest


class ContractListPageTest(FunctionalTest):
    """Tests the basic functionality of the contract list page."""

    def validate_contract_listing(self, contract_listing, contract, num_bids=0, low_bid='None'):
        """
        Asserts that every item in a contract listing matches the correct item in a dictionary.
        The keys of the dictionary correspond to the "name" of the listing elements.
        For contracts on the contract_list.html page.
        """
        title = contract_listing.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(title.text, contract['contract_title'])
        name = contract_listing.find_element(By.CLASS_NAME, 'listing-agency-name')
        self.assertEquals(name.text, contract['agency_name'])
        end_date = contract_listing.find_element(By.CLASS_NAME, 'listing-bidding-end-date')
        self.assertEquals(end_date.text, contract['bidding_end_date'])
        lowest_bid = contract_listing.find_element(By.CLASS_NAME, 'listing-lowest-bid')
        if low_bid != 'None':
            self.assertEquals(float(lowest_bid.text[1:]), low_bid)
        else:
            self.assertEquals(lowest_bid.text, low_bid)
        number_bids = contract_listing.find_element(By.CLASS_NAME, 'listing-number-bids')
        self.assertEquals(number_bids.text, str(num_bids))

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
        contract1 = self.random_contract_dict()
        self.fill_form_from_dictionary(contract1)
        submit_button = self.browser.find_element(By.ID, 'submit')
        submit_button.send_keys(Keys.RETURN)
        number_contracts_2 = len(self.browser.find_elements(By.CLASS_NAME, 'contract-listing'))
        self.assertEqual(number_contracts_1, number_contracts_2 - 1)

        # check new contract contains correct information
        first_contract = self.browser.find_element(By.CLASS_NAME, 'contract-listing')
        self.validate_contract_listing(first_contract, contract1)

    def test_bid_info_updates_correctly(self):
        """
        Tests that adding a bid on the contract page updates the relevant fields on the contract
        list.
        """

    def test_contractor_view(self):
        """Tests that a contractor cannot see the create contract form."""

    def test_contractee_view(self):
        """Tests that a contractee can see the create contract form."""

    def test_must_be_logged_in_to_visit(self):
        """Tests that an unauthenticated user is redirected to login page."""

    def test_cannot_submit_invalid_contract_form(self):
        """Tests that a contract with invalid forms cannot be created."""