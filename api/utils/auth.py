#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JsonWebToken

# JWT creation.
jwt = JsonWebToken(os.getenv('SECRET_KEY'), expires_in=3600)

# Refresh token creation.
refresh_jwt = JsonWebToken(os.getenv('REFRESH_KEY'), expires_in=7200)

# Auth object creation.
auth = HTTPTokenAuth(scheme='Bearer')
