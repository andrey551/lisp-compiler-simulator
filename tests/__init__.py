from main import run
import pytest
import logging
dirs = ['testcase-1/', 'testcase-2/', 'testcase-3/', 'testcase-4/']

@pytest.mark.golden_test("golden/*.yml")
def test_hw(golden, caplog):
    caplog.set_level(logging.DEBUG)

    # for i in dirs:
    #     source = 
    #     with open(i + 'code.lisp')
