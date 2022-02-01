# Created on 2019-10-15
# John Leach <jfleach@jfleach.com>

# Pull the Alpine Linux image for Python 3.7
FROM python:3.7-alpine

# Use the temp directory
WORKDIR /tmp

# Copy over the Python library requirements file
COPY requirements.txt requirements.txt

# Install the Python requirements
RUN pip3 install -r requirements.txt

# Make a static directory for the Swagger JSON file
RUN mkdir -p $WORKDIR/static

# Copy over the Swagger JSON file
COPY static/swagger.json $WORKDIR/static/swagger.json

# Copy over the Flask date, time, and weather application
COPY datetime_weather.py datetime_weather.py

# Start the Flask date, time, and weather application
CMD python3 datetime_weather.py
