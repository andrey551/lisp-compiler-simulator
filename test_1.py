import pytest
import os
import contextlib
import io
import logging
import tempfile

from lab3.main import run

@pytest.mark.golden_test("golden/testcase-1.yml")
def test_1(golden, caplog):
    
    caplog.set_level(logging.DEBUG)
    source = "source.lisp"
    input = "in.txt"
    output = "out.txt"
    debug_txt = "debug.txt"
    mcode = "debug.bin"
    
    with open(source, "w", encoding="utf-8") as file:
        file.write(golden["source"])
    
    with open(input, "w", encoding="utf-8") as file:
        file.write(golden["input"])

    with contextlib.redirect_stdout(io.StringIO()) as stdout:
        run(source, mcode, input, output, debug_txt)
    

    with open(output, encoding="utf-8") as file:
        out = file.read()
    file.close()

    with open(debug_txt, encoding="utf-8") as file:
        stacktrace = file.read()

    assert out == golden.out["output"]
    assert stacktrace == golden.out["machine_code"]
    # assert caplog.text == golden.out["log"]