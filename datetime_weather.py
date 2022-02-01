"""
Created on 2019-10-15

This Python module serves up Endpoints to find the date, time, and weather.

@author: jfleach@jfleach.com

"""

import datetime as dt
import requests
import zipcodes
from flask import Flask, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.security import generate_password_hash, check_password_hash

# Define the Open Weather Map API Key and Endpoint
API_KEY = "ac800d396d7773c968b317cec17e9f82"
API_URL = "http://api.openweathermap.org/data/2.5/weather"


class Weather():
    """
    This class checks the weather.
    """
    @classmethod
    def check_zip_code(cls, zip_code):
        """
        This method checks for a valid ZIP Code.

        :param zip_code: The ZIP Code to query.
        :returns: True or False
        """
        # Return True if the ZIP Code is valid
        try:
            if zipcodes.matching(zip_code) == []:
                return False
            return True
        except ValueError:
            return False

    @classmethod
    def check_units(cls, units):
        """
        This method checks for valid units.

        :param units: The units to check.
        :returns: True or False
        """
        # Return True for supported units
        if units in ("Default", "imperial", "metric"):
            return True

        # Return False for unsupported units
        return False

    @classmethod
    def return_weather(cls, weather_response):
        """
        This method returns the weather as JSON.

        :param weather_response: The weather response.
        :returns: The weather.
        """
        # Return the weather
        weather = {}
        weather["temperature"] = weather_response["main"]["temp"]
        weather["description"] = weather_response["weather"][0]["description"]
        return weather

    def run(self):
        """
        This method runs the Flask application.
        """
        # Setup the datetime and weather Endpoints
        app = Flask(__name__)
        auth = HTTPBasicAuth()

        users = {
            "admin": generate_password_hash("password"),
        }

        # Setup the Swagger Endpoint
        swagger_url = '/swagger'
        api_url = '/static/swagger.json'
        swagger_blueprint = get_swaggerui_blueprint(
            swagger_url,
            api_url,
            config={
                'app_name': "Weather Application"
            }
        )
        app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)

        # Setup error handling for various HTTP status codes
        @app.errorhandler(400)
        def handle_400_error(_error):  # pylint:disable=unused-variable
            """
            This method returns the HTTP status code 400.

            :returns: Status code 400.
            """
            return make_response(jsonify({'error': 'Bad request'}), 400)

        @app.errorhandler(401)
        def handle_401_error(_error):  # pylint:disable=unused-variable
            """
            This method returns the HTTP status code 401.

            :returns: Status code 401.
            """
            return make_response(jsonify({'error': 'Unauthorized'}), 401)

        @app.errorhandler(404)
        def handle_404_error(_error):  # pylint:disable=unused-variable
            """
            This method returns the HTTP status code 404.

            :returns: Status code 404.
            """
            return make_response(jsonify({'error': 'Not found'}), 404)

        @app.errorhandler(500)
        def handle_500_error(_error):  # pylint:disable=unused-variable
            """
            This method returns the HTTP status code 500.

            :returns: Status code 500.
            """
            return make_response(jsonify({'error': 'Internal server error'}), 500)

        @auth.verify_password
        def verify_password(username, password):  # pylint: disable=unused-variable
            if username in users:
                return check_password_hash(users.get(username), password)
            return False

        @app.route("/api/v1/datetime", methods=["GET"])
        @auth.login_required
        def datetime():  # pylint: disable=unused-variable
            # Get the current date and time
            date_time = {}
            date_time['datetime'] = dt.datetime.now()

            # Return the current date and time as JSON
            return date_time

        @app.route("/api/v1/weather", methods=["GET"])
        @auth.login_required
        def weather():  # pylint: disable=unused-variable
            # Retrieve the ZIP code
            zip_code = request.args.get("zip")
            units = request.args.get("units")
            # Check for supported units
            if self.check_units(units):
                # Detect the country code
                if ',' in zip_code:
                    # Split upon a comma
                    zip_code_split = zip_code.split(',')
                    # Check for a valid ZIP code
                    if self.check_zip_code(zip_code_split[0]):
                        # Get the weather with the ZIP code and country code
                        weather_response = requests.get(url=API_URL,
                                                        params=dict(zip=zip_code_split[0] + "," +
                                                                    zip_code_split[1], units=units,
                                                                    APPID=API_KEY)).json()
                        # Return the weather temperature and description
                        return self.return_weather(weather_response)
                # Check for a valid ZIP code
                if self.check_zip_code(zip_code):
                    # Get the weather with the ZIP code
                    weather_response = requests.get(url=API_URL, params=dict(zip=zip_code,
                                                                             units=units,
                                                                             APPID=API_KEY)).json()
                    # Return the weather temperature and description
                    return self.return_weather(weather_response)
                # Return a bad request for ZIP codes that don't exist
                return make_response(jsonify({'error': 'Bad request'}), 400)
            # Return a bad request for unsupported units
            return make_response(jsonify({'error': 'Bad request'}), 400)

        # Start the Flask server
        app.run(host="0.0.0.0", port=8080, threaded=True)


if __name__ == "__main__":
    APP = Weather
    Weather.run(APP)

