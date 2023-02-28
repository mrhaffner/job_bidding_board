from .tests import FunctionalTest


class AuthorizationPagesTest(FunctionalTest):
    """Tests the basic functionalities associated with a user authentication."""

    def test_valid_login(self) -> None:
        """Tests user authentication"""

    def test_registration(self) -> None:
        """Tests user registration."""

    def test_logout(self) -> None:
        """Tests loging out a user."""

    def test_authenticated_redirected_from_login(self) -> None:
        """Tests that an authenticated user is redirected away from login page."""
        self.browser.get(self.base_url + '/accounts/login') #go to login 
        self.browser.set_window_size(1024,768) 

        enter_username = self.browser.find_element_by_name('username')
        enter_password  = self.browser.find_element_by_name('password')
        click_submit  = self.browser.find_elemtn_by_css_selector('button[type="submit"]')

        enter_username.send_keys('bot')
        enter_password.send_keys("test@123467890") #password is long because it needs comlexity 
        click_submit.click()
        self.browser.get(self.base_url + '/accounts/login')  #now try to go back to login 

        loged_in =self.browser.find_element(By.ID, "login") #if there is a login botton, 
        #then it still needs to log in
        self.assertEqual(len(loged_in),0)

    def test_authenticated_redirected_from_registration(self) -> None:
        """Tests that an authenticated user is redirected away from registration page."""
        self.browser.get(self.base_url + '/accounts/regisnter')
        self.browser.set_window_size(1024,768)

        enter_username = self.browser.find_element_by_name('username')
        enter_password  = self.browser.find_element_by_name('password')
        enter_confirm = self.browser.find_element_by_name('confirm password')
        click_submit  = self.browser.find_elemtn_by_css_selector('button[type="submit"]')


        enter_username.send_keys('newbot')
        enter_password.send_keys("test@123467890") #password is long because it needs comlexity 
        enter_confirm.send_keys("test@123467890")
        #am not sure what other information needs that needs to be filled out so fill out here 
        click_submit.click()
        self.browser.get(self.base_url + '/accounts/register')  #now try to go back to login 

        registered =self.browser.find_element(By.ID, "register") #find the register botton 
        self.assertEqual(len(registered),0) 