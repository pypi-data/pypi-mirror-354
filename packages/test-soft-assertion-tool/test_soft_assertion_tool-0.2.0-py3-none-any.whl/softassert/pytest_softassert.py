import pytest
from softassert.assertion import SoftAssert

def pytest_runtest_teardown(item, nextitem):
    try:
        SoftAssert.verify()
    except AssertionError as e:
        raise e
