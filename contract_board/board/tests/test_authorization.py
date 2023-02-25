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
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024,768)
        loged_in =self.browser.find_element(By.ID, "login") #if there is a login botton, 
        #then it still needs to log in
        self.assertEqual(len(loged_in),0)

    def test_authenticated_redirected_from_registration(self) -> None:
        """Tests that an authenticated user is redirected away from registration page."""
        self.browser.get(self.base_url)
        self.browser.set_window_size(1024,768)
        registered =self.browser.find_element(By.ID, "Register")
        self.assertEqual(len(registered),0) 