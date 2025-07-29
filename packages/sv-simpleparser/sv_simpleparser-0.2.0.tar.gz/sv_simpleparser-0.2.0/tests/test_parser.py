# MIT License
#
# Copyright (c) 2025 ericsmacedo
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Test Parser."""

from pathlib import Path

from pytest import mark
from test2ref import assert_refdata

from sv_simpleparser import File, Module, ModuleInstance, Param, Port, parse_file

EXAMPLES_PATH = Path(__file__).parent / "svfiles_examples"
EXAMPLES = tuple(sorted(EXAMPLES_PATH.glob("*.sv")))


@mark.parametrize("example", EXAMPLES)
def test_examples(tmp_path, example):
    """Test All Examples And Compare with 'refdata'."""
    file = parse_file(example)
    (tmp_path / "overview.txt").write_text(file.overview)
    assert_refdata(test_examples, tmp_path, flavor=example.name)


def test_adder(examples):
    """Test Adder Example."""
    file_path = examples / "adder.sv"
    file = File(
        path=file_path,
        modules=(
            Module(
                name="adder",
                params=(
                    Param(ptype="integer", name="DATA_WIDTH", width=None, comment=None),
                    Param(ptype="integer", name="TEST", width=None, comment=None),
                ),
                ports=(
                    Port(
                        direction="input",
                        ptype="unsigned",
                        name="A",
                        width="[DATA_WIDTH-1:0]",
                        comment=["// This is a test\n", "// This is another test\n"],
                    ),
                    Port(direction="input", ptype="unsigned", name="B", width="[DATA_WIDTH-1:0]", comment=None),
                    Port(direction="output", ptype="unsigned", name="X", width="[DATA_WIDTH:0]", comment=None),
                ),
                insts=(ModuleInstance(name="u_test_module", module="test_module"),),
            ),
        ),
    )
    assert file == parse_file(file_path)


def test_param_module(examples):
    """Test Parameter Module."""
    file_path = examples / "param_module.sv"
    file = File(
        path=file_path,
        modules=(
            Module(
                name="param_module",
                params=(
                    Param(ptype=None, name="WIDTH", width=None, comment=["// Width of the input data\n"]),
                    Param(ptype=None, name="DEPTH", width=None, comment=None),
                    Param(ptype=None, name="INIT_VAL", width="[7:0]", comment=None),
                    Param(ptype="logic", name="ENABLE_FEATURE", width=None, comment=None),
                ),
                ports=(
                    Port(direction="input", ptype="wire", name="clk", width=None, comment=None),
                    Port(direction="input", ptype="wire", name="rst_n", width=None, comment=["// active-low reset\n"]),
                    Port(
                        direction="input",
                        ptype="wire",
                        name="data_in",
                        width="[WIDTH-1:0]",
                        comment=["// Input data\n"],
                    ),
                    Port(direction="output", ptype="reg", name="data_out", width="[WIDTH-1:0]", comment=None),
                    Port(direction="inout", ptype="wire", name="bidir_bus", width="[DEPTH-1:0]", comment=None),
                ),
                insts=(
                    ModuleInstance(name="u_sub_module", module="sub_module"),
                    ModuleInstance(name="u_sub_module2", module="sub_module"),
                ),
            ),
            Module(
                name="sub_module",
                params=(
                    Param(ptype=None, name="DATA_WIDTH", width=None, comment=None),
                    Param(ptype=None, name="INIT_VALUE", width="[7:0]", comment=None),
                ),
                ports=(
                    Port(direction="input", ptype="wire", name="clk", width=None, comment=None),
                    Port(direction="input", ptype="wire", name="reset", width=None, comment=None),
                    Port(direction="input", ptype="wire", name="input_data", width="[DATA_WIDTH-1:0]", comment=None),
                    Port(direction="output", ptype="wire", name="output_data", width="[DATA_WIDTH-1:0]", comment=None),
                    Port(direction="inout", ptype="wire", name="config_bus", width="[DATA_WIDTH/2-1:0]", comment=None),
                ),
                insts=(),
            ),
        ),
    )
    assert file == parse_file(file_path)
