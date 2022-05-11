#!flask/bin/python
# -*- coding: utf-8 -*-

# All error message codes can be customized right here
# Alternatively, feel free to fashion your own to suit your unique needs.

SERVER_ERROR_500 = ({"message": "An error occurred."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"message": "Invalid input."}, 422)
ALREADY_EXIST = ({"message": "Already exists."}, 409)
UNAUTHORIZED = ({"message": "Wrong credentials."}, 401)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
NOT_ADMIN = ({"message": "Access permission denied."}, 403)
