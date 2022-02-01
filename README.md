# Weather Application 

The following document describes the installation and usage instructions.

## Base Operating System Installation

It is recommended that the user installs [Xubuntu 18.04](https://xubuntu.org/release/18-04) to run this code. 

## Git Source Code

The user can clone the repository by issuing the following command:

```
$ git clone https://github.com/jfleach/weather.git
```

## Docker Installation

Follow the instructions at https://docs.docker.com/install/linux/docker-ce/ubuntu to install the Docker Community Edition and also install Docker Compose.

```
$ sudo apt-get install docker-compose
```

It may be necessary to add the user to the docker group.  After issuing the following command, logout or cycle the shell.

```
$ usermod -aG docker $(whoami)
```

Bring up the the Docker container and application by issuing the following command:

```
$ docker-compose up --build
```

## Testing the Application

Run the unit tests by issuing the following command:

```
$ python3 test_datetime_weather.py
```

##### Note:
> Open Weather Map sometimes returns incorrect weather descriptions.  I have seen it return "light rain" or "cloud" when it should be "clear".

## Viewing the Documentation

View the Swagger documentation at: http://localhost/swagger

##### Note:
> If you want to use the country code, use "80301,us" for the ZIP code and country code if executing via Swagger.  Use "Default", "imperial", or "metric" for the units if executing via Swagger.
