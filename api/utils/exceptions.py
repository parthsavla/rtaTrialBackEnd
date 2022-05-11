#!/usr/bin/python
# -*- coding: utf-8 -*-

"""User defined exceptions"""


class Error(Exception):
    """Base class for other exceptions."""
    pass


class DatabaseError(Error):
    """Exception raised when database session & commit fails.
    Reasons:
        - failed database connection
        - database generated error
    """

    def __init__(self, message="Database Failure: commit could not take place,"
                               " check db connection and/or configuration"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class MailException(Error):
    """Exception raised when database session & commit fails.
    Reasons:
        - failed mail delivery
        - Either the recipient mail is wrong.
    """

    def __init__(self, message="Mailing Failure: Mail sending failed, check the input"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
