import pytest
import os
import contextlib
import io
import logging
import tempfile

from lab3.main import run

@pytest.fixture
@pytest.mark.golden_test("golden/testcase-1.yml")
def test_1(golden, caplog):
    
    caplog.set_level(logging.DEBUG)
    source = "temp/source1.lisp"
    input = "temp/in1.txt"
    output = "temp/out1.txt"
    debug_txt = "temp/debug1.txt"
    mcode = "temp/debug1.bin"
    
    with open(source, "w", encoding="utf-8") as file:
        file.write(golden["source"])
    file.close()
    with open(input, "w", encoding="utf-8") as file:
        file.write(golden["input"])
    file.close()
    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        run(source, mcode, input, output, debug_txt)
    file.close()

    with open(output, encoding="utf-8") as file:
        out = file.read()
    file.close()

    with open(debug_txt, encoding="utf-8") as file:
        stacktrace = file.read()

    assert out == golden.out["output"]
    assert stacktrace == golden.out["machine_code"]
    # assert caplog.text == golden.out["log"]