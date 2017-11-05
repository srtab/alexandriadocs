from django.test import LiveServerTestCase
from django.urls import reverse
from django.core import mail

from accounts.models import User
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


class FunctionalTestCase(LiveServerTestCase):
    """ """
    host = 'app'

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        self.driver = webdriver.Remote(
            command_executor="http://selenium-chrome:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()
        self.driver.quit()


class LoginTest(FunctionalTestCase):
    """ """

    def test_login(self):
        User.objects.create_user(
            username='username', email='email@email.com', password='pass')
        # The user visit the login url
        self.driver.get(self.live_server_url + reverse('account_login'))
        # She noticed the page title and heading contains Login
        self.assertIn('Login', self.driver.title)
        self.assertEqual(
            'Login', self.driver.find_element_by_tag_name('h1').text)
        # The user try to login with the form
        self.driver.find_element_by_name('login').send_keys('email@email.com')
        self.driver.find_element_by_name('password').send_keys('pass')
        self.driver.find_element_by_id("loginForm").submit()
        print(mail.outbox)
        self.assertEqual(
            self.driver.current_url, self.live_server_url + reverse('account_email_verification_sent'))
