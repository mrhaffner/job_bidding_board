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

    def test_authenticated_redirected_from_registration(self) -> None:
        """Tests that an authenticated user is redirected away from registration page."""