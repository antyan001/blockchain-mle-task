from unittest import mock
import os


def mockenv(**envvars):
    return mock.patch.dict(os.environ, envvars)
