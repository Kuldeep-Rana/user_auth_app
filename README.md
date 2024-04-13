
# User Registration and Login App

This is a simple Flask application for user registration and login, using MongoDB as the database.

## Features

- User registration: Allows users to register with a username and password.
- User login: Allows registered users to log in with their username and password.
- Health Check: Provides a health check endpoint to verify the status of the application.

## Prerequisites

Before running this application, make sure you have the following installed:

- Python
- MongoDB

## Run following commands to install mongo db and flask dependencies.

``` pip install Flask pymongo ```

# Sample curl request for testing

* Registration

```
curl --location 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data '{
    "username" :"Kuldeep",
    "password" : "hellotest"
}' 

```
* Login
```
curl --location 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data '{
"username" :"Kuldeep",
"password" : "hellotest"
}'
```
* Health check
```
curl --location 'http://127.0.0.1:5000/health'
```

