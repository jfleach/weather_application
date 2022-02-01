"""
Created on 2019-10-28

This Python module validates the datetime_weather module.

@author: jfleach@jfleach.com

"""

import inspect
import json
import unittest
import requests
from requests.auth import HTTPBasicAuth


class TestDatetimeWeather(unittest.TestCase):
    """
    This test class validates the datetime_weather module.
    """
    @classmethod
    def setUpClass(cls):
        """
        A method to prepare the test fixture.
        """
        cls.username = "admin"
        cls.password = "password"
        cls.zip_code = "80301"
        cls.country_code = "us"
        # Open Weather Map uses the following to define the unit type
        # API Documentation: https://openweathermap.org/current
        # Default: Kelvin, Metric: Celsius, Imperial: Fahrenheit
        cls.units = ["Default", "imperial", "metric"]
        cls.date_time_url = "http://localhost/api/v1/datetime"
        cls.weather_url = "http://localhost/api/v1/weather"

    @staticmethod
    def check_status_code(response):
        """
        This method checks the status code.

        :param: response: The HTTP response.
        :returns: True (for status code 200) or False (for status code 401)
        """
        # Check the HTTP status code
        response_code = response.status_code

        # Return False for Unauthorized
        if response_code == 401:
            return False

        # Return True for OK
        return True

    def test_date_time_auth(self):
        """
        This method verifies that the current date and time can be retrieved with authentication.
        """
        # Log the unit test name
        print("Running: " + inspect.stack()[0][3])

        # Attempt to print the current date and time
        try:
            response = requests.get(self.date_time_url,
                                    auth=HTTPBasicAuth(self.username, self.password))
            # Check the status code
            if self.check_status_code(response):
                print("Passed: date and time is: " + str(response.json()))
            else:
                print("Failed: Unauthorized")
        except Exception as error:  # pylint:disable=broad-except
            print("Failed: %s", str(error))

    def test_date_time_noauth(self):
        """
        This method verifies that the current date and time can be retrieved without authentication.
        """
        # Log the unit test name
        print("Running: " + inspect.stack()[0][3])

        # Attempt to print the current date and time
        try:
            response = requests.get(self.date_time_url)
            # Check the status code
            if not self.check_status_code(response):
                print("Passed: Unauthorized")
            else:
                print("Failed: Could authenticate.")
        except json.decoder.JSONDecodeError:
            print("Passed: Could not authenticate.")

    def test_zip_code_auth(self):
        """
        This method verifies that the weather can be retrieved using the ZIP code with
        authentication.
        """
        # Log the unit test name
        print("Running: " + inspect.stack()[0][3])

        # Attempt to print the weather for the ZIP code for each type of unit
        for unit in self.units:
            try:
                response = requests.get(self.weather_url + "?zip=" + self.zip_code + "&units=" +
                                        unit, auth=HTTPBasicAuth(self.username, self.password))

                # Check the status code
                if self.check_status_code(response):
                    print("Passed: weather is: " + str(response.json()))
                else:
                    print("Failed: Unauthorized")
            except Exception as error:  # pylint:disable=broad-except
                print("Failed: %s", str(error))

    def test_zip_code_noauth(self):
        """
        This method verifies that the weather can be retrieved using the ZIP code without
        authentication.
        """
        # Log the unit test name
        print("Running: " + inspect.stack()[0][3])

        # Attempt to print the weather for the ZIP code
        try:
            response = requests.get(self.weather_url + "?zip=" + self.zip_code)
            # Check the status code
            if not self.check_status_code(response):
                print("Passed: Unauthorized")
            else:
                print("Failed: Could authenticate.")
        except json.decoder.JSONDecodeError:
            print("Passed: Could not authenticate.")

    def test_zip_code_cc_auth(self):
        """
        This method verifies that the weather can be retrieved using the ZIP code and country code
        with authentication.
        """
        # Log the unit test name
        print("Running: " + inspect.stack()[0][3])

        # Attempt to print the weather for the ZIP code using the country code
        try:
            response = requests.get(self.weather_url + "?zip=" + self.zip_code + "," +
                                    self.country_code + "&units=" + self.units[0],
                                    auth=HTTPBasicAuth(self.username, self.password))

            # Check the status code
            if self.check_status_code(response):
                print("Passed: weather is: " + str(response.json()))
            else:
                print("Failed: Unauthorized")
        except Exception as error:  # pylint:disable=broad-except
            print("Failed: %s", str(error))

    @classmethod
    def tearDownClass(cls):
        """
        A method to tear down the test fixture.
        """
        pass  # pylint:disable=unnecessary-pass


if __name__ == '__main__':
    unittest.main()

