import logging
import pytest
import contextlib
import io

from lab3.main import run

@pytest.mark.golden_test("golden/testcase-4.yml")
def test_1(golden, caplog):

    caplog.set_level(logging.DEBUG)
    
    source = "temp/source4.lisp"
    input = "temp/in4.txt"
    output = "temp/out4.txt"
    debug_txt = "temp/debug4.txt"
    mcode = "temp/debug4.bin"
    
    with open(source, "w", encoding="utf-8") as file:
        file.write(golden["source"])
    file.close()
    with open(input, "w", encoding="utf-8") as file:
        file.write(golden["input"])
    file.close()

    run(source, mcode, input, output, debug_txt)

    with open(output, encoding="utf-8") as file:
        out = file.read()
    file.close()

    with open(debug_txt, encoding="utf-8") as file:
        stacktrace = file.read()

    assert out == golden.out["output"]
    assert stacktrace == golden.out["machine_code"]
    assert caplog.text == golden.out["log"]