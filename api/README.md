# GENERAL API DOCUMENTATION

## End Points

| HTTP Method   |  URI                                                      |   Action                               |
| :-------------|:----------------------------------------------------------|:---------------------------------------|
| GET           | http://[hostname]/usiu-research/api/v1.0/home             | Get home page data                     |
| GET           | http://[hostname]/usiu-research/api/v1.0/signup           | Get signup page data                   |
| POST          | http://[hostname]/usiu-research/api/v1.0/signup           | Create new User  Resource              |
| GET           | http://[hostname]/usiu-research/api/v1.0/login            | Get login page                         |
| POST          | http://[hostname]/usiu-research/api/v1.0/login            | Authenticate user data                 |
| PUT           | http://[hostname]/usiu-research/api/v1.0/forgotpassword   | Update User Resource - password        |
| POST          | http://[hostname]/usiu-research/api/v1.0/refresh_token    | Refresh token                          |
|-
| POST          | http://[hostname]/usiu-research/api/v1.0/profile          | Create user profile                    |
| DELETE        | http://[hostname]/usiu-research/api/v1.0/delete_user      | Delete user Resource                   |
| PUT           | http://[hostname]/usiu-research/api/v1.0/updateprofile    | Update user profile                    |
| GET           | http://[hostname]/usiu-research/api/v1.0/data_user        | Get user data                          |
| GET           | http://[hostname]/usiu-research/api/v1.0/data_admin       | Get admin data                         |
| GET           | http://[hostname]/usiu-research/api/v1.0/data_super_admin | Get super admin data                   |
| GET           | http://[hostname]/usiu-research/api/v1.0/data_users       | Get super admin data                   |
|               |                                                           |                                        |                                                                                                      |
|-
| POST          | http://[hostname]/usiu-research/api/v1.0/mail_student     | Create student proposal                |
| POST          | http://[hostname]/usiu-research/api/v1.0/mail_supervisor  | Create supervisor proposal             |
|-
|               | http://[hostname]/usiu-research/api/v1.0/mailproposal     |                                        |   