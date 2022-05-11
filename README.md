# BACKEND :memo: DOCUMENTATION :tada:

*To make contribution or test the app, you might want to see the next step:*

## Setting Up The App

### :joy: So you wanna start!

*Lets :rocket:*

- [x] First clone or fork the repo (it's a free world! No pressure!) `$ git clone https://github.com/Microsoft-21st-Century-Skills-Lab/research-extension-app.git`
- [x] For backend, switch into the backend folder
- [x] Set-up virtual environment, you can use pipenv or virtualenv `$ py -m -r venv env` (you can google), with pycharm its so simple
- [x] Run `$ pip install -r requirements.txt` (:loud_sound: some packages might need manual installation )...not my fault
- [x] Everything in place ? Run `flask run`

# API end points example
[![Build Status](https://travis-ci.org/)

* For requests using httpie: *[https://httpie.io/]()*
* For requests using curl: *[https://curl.haxx.se/download.html]()*

> __Example user, admin and super admin users are created in database initializer class. You can use these users to login, logout and data handlers. For register handler, use new user information, otherwise returns already exist user.__


| Test Users        | Email Address           | Password  |
| ------------- |:-------------:| -----:|
| User      | test_email@example.com | test_password |
| Admin      | admin_email@example.com      |   admin_password |
| Super Admin | sa_email@example.com      |    sa_password |

#### Register:

* HTTPIE Request:
```sh
http POST :8000/usiu-research/api/v1.0/register username=example_username password=example_password email=example@example.com
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" --data '{"username":"example_name","password":"example_password", "email":"example@example.com"}' http://127.0.0.1:8000/usiu-research/api/v1.0/register
```

#### Login:
* HTTPIE Request:
```sh
http POST :8000/usiu-research/api/v1.0/login email=example@example.com password=example_password
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" --data '{"email":"example@example.com", "password":"example_password"}' http://127.0.0.1:8000/usiu-research/api/v1.0/login
```

> Response: Got access token and refresh token!


#### Logout:
* HTTPIE Request:
```sh
http POST :8000/v1/auth/logout Authorization:"Bearer ACCESS_TOKEN" refresh_token=REFRESH_TOKEN
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"refresh_token":"REFRESH_TOKEN"}' http://127.0.0.1:8000/usiu-research/api/v1.0/logout
```

#### Reset Password:
* HTTPIE Request:
```sh
http POST :5000/v1/auth/password_reset Authorization:"Bearer ACCESS_TOKEN" old_pass=<OLD-PASSWORD> new_pass=<NEW-PASSWORD>
```
* Curl Request:
```sh
curl -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" --data '{"old_pass":"OLD-PASSWORD", "new_pass":"NEW-PASSWORD"}' http://127.0.0.1:8000/usiu-research/api/v1.0/password_reset
```


>__There are some example routes in resource/main file. To use them:__


## 
## Links:

### Application Structure
1. [Project Structure](https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/#testing) 
2. [Blueprints](https://flask.palletsprojects.com/en/1.1.x/blueprints/#blueprints)
3. [Rest-Api Quickstart](https://www.analyticsvidhya.com/blog/2022/01/rest-api-with-python-and-flask/)
4. [Sqlite Tuts](https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/)
5. [SQLAlchemy Relationship](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
