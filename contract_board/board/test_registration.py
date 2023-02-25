def test_user_registration(self) -> None:
    # get the url for the registration page
    url: str = reverse('register')
    # test that the registration page can be accessed
    response: HttpResponse = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # create a new user by posting data to the registration page
    response: HttpResponse = self.client.post(url, {
        'username': 'testuser',
        'password1': 'testpassword123',
        'password2': 'testpassword123',
    })
    # test that the user was successfully created and redirected to the homepage
    self.assertEqual(response.status_code, 302)

    # retrieve the user object from the database
    user: User = User.objects.get(username='testuser')
    # test that the user object exists
    self.assertIsNotNone(user)
