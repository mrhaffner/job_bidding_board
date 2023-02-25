from .tests import FunctionalTest


class AuthorizationPagesTest(FunctionalTest):
    """Tests the basic functionalities associated with a user authentication."""

    def test_valid_login(self) -> None:
        """Tests user authentication"""
        self.browser.get(self.base_url + '/login/')
        self.browser.set_window_size(1024, 768)
        
        # Find the login form fields and submit button
        username_input: WebElement = self.browser.find_element_by_name('username')
        password_input: WebElement = self.browser.find_element_by_name('password')
        submit_button: WebElement = self.browser.find_element_by_css_selector('button[type="submit"]')
        
        # Enter valid login credentials
        username_input.send_keys('your_username')
        password_input.send_keys('your_password')
        
        # Click the submit button to log in
        submit_button.click()
        
        # Verify that the user is redirected to the home page after successful login
        assert self.browser.current_url == self.base_url + '/'
        
        # Verify that the user is logged in, I DONT KNOW HOW TO DO
                
    def test_registration(self) -> None:
        """Tests user registration."""

    def test_logout(self) -> None:
        """Tests loging out a user."""

    def test_authenticated_redirected_from_login(self) -> None:
        """Tests that an authenticated user is redirected away from login page."""

    def test_authenticated_redirected_from_registration(self) -> None:
        """Tests that an authenticated user is redirected away from registration page."""