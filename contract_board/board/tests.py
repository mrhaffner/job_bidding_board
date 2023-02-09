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

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.base_url = 'http://127.0.0.1:8000/'


    def tearDown(self):
        self.browser.quit()


    def fill_form_from_dictionary(self, form_data):
        for id, value in form_data.items():
            element = self.browser.find_element(By.ID, id)
            element.send_keys(value)


    def test_iteration_1(self):
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024, 768)
        title = self.browser.find_element(By.CLASS_NAME, "title")

        # test html/css loads properly - smoke test
        self.assertAlmostEqual(
            title.location["x"] + title.size["width"] / 2,
            1008 / 2, # screen actual width / 2
            delta=10
        )

        # check contract form submission adds contract to board
        contract = CONTRACT_DATA1
        self.fill_form_from_dictionary(contract)
        submit_button = self.browser.find_element(By.ID, 'button')
        submit_button.send_keys(Keys.RETURN)

        first_contract = self.browser.find_element(By.CLASS_NAME, 'contract-listing')

        title = first_contract.find_element(By.TAG_NAME, 'h3')
        self.assertEquals(title.text, contract.contract_title)

        # check new contract contains correct information
        contract_divs = first_contract.find_elements(By.TAG_NAME, 'div')
        contract_items = [div.find_elements(By.TAG_NAME, 'span')[1] for div in contract_divs]
        self.assertEquals(contract_items[0].text, contract.agency_name)
        self.assertEquals(contract_items[1].text, contract.bidding_end_date)
        self.assertEquals(contract_items[2].text, 'None')
        self.assertEquals(contract_items[3].text, '0')

        # check adding second contract keeps contracts in order
        # check clicking contract redirects to correct contract page

        # check layout/style of contract page
        # check contract contains correct information
        # check bid form submission adds bid to contract
        # check new bid contains correct information
        # check adding second bid keeps bids in order

        # check number of bids updates correctly on contract list page
        # check lowest bid updates correctly on contract list page


        # for later Iteration 2
        # check if contract list is empty, empty options displays