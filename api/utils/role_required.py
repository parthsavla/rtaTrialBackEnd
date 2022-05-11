#!/usr/bin/python
# -*- coding: utf-8 -*-

import functools
import logging

from flask import request
from . import errors as error
from .auth import jwt


def permission(arg):
    def check_permissions(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            # Get request authorization.
            auth = request.authorization
            if auth is None and "Authorization" in request.headers:
                try:
                    auth_type, token = request.headers["Authorization"].split(None, 1)
                    # Generate new token
                    data = jwt.loads(token)
                    if data["admin"] < arg:
                        return error.NOT_ADMIN
                except ValueError as e:
                    logging.error(e)
                    return error.INVALID_INPUT_422
            # return method
            return f(*args, **kwargs)
        # return decorated method
        return decorated
    # return check permission method.
    return check_permissions
