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

from sv_simpleparser import parse_sv


def test_adder(project_root):
    """Test Adder Example."""
    mod_name_ref = "adder"
    port_name_lst_ref = ["A", "B", "X"]
    param_name_lst_ref = ["DATA_WIDTH", "TEST"]
    port_width_lst_ref = [
        "[DATA_WIDTH-1:0]",
        "[DATA_WIDTH-1:0]",
        "[DATA_WIDTH:0]",
    ]
    file_path = project_root / "tests" / "svfiles_examples" / "adder.sv"

    mod_lst = parse_sv(file_path)

    mod = mod_lst[0]

    mod_name = mod.name
    port_name_lst = [port.name for port in mod.port_lst]
    port_width_lst = [port.width for port in mod.port_lst]
    param_name_lst = [param.name for param in mod.param_lst]

    assert mod_name == mod_name_ref
    assert port_name_lst == port_name_lst_ref
    assert port_width_lst == port_width_lst_ref
    assert param_name_lst == param_name_lst_ref


def test_bcd_adder(project_root):
    """Test BCD Adder Example."""
    mod_name_ref = "bcd_adder"
    port_name_lst_ref = ["a", "b", "cin", "sum", "cout"]
    port_width_lst_ref = ["[3:0]", "[3:0]", None, "[3:0]", None]
    file_path = project_root / "tests" / "svfiles_examples" / "bcd_adder.sv"

    mod_lst = parse_sv(file_path)

    mod = mod_lst[0]
    mod_name = mod.name
    port_name_lst = [port.name for port in mod.port_lst]
    port_width_lst = [port.width for port in mod.port_lst]

    assert mod_name == mod_name_ref
    assert port_name_lst == port_name_lst_ref
    assert port_width_lst == port_width_lst_ref


def test_up_down_counter(project_root):
    """Test up_down_counter Example."""
    mod_name_ref = "up_down_counter"
    port_name_lst_ref = ["out", "up_down", "clk", "reset"]
    param_name_lst_ref = []  # No parameters in this module
    port_width_lst_ref = ["[7:0]", None, None, None]  # Only 'out' has width specification
    port_direction_ref = ["output", "input", "input", "input"]  # Added port directions
    file_path = project_root / "tests" / "svfiles_examples" / "up_down_counter.sv"

    mod_lst = parse_sv(file_path)

    mod = mod_lst[0]

    mod_name = mod.name
    port_name_lst = [port.name for port in mod.port_lst]
    port_width_lst = [port.width for port in mod.port_lst]
    param_name_lst = [param.name for param in mod.param_lst]
    port_direction_lst = [port.direction for port in mod.port_lst]  # Get port directions

    assert mod_name == mod_name_ref
    assert port_name_lst == port_name_lst_ref
    assert port_width_lst == port_width_lst_ref
    assert param_name_lst == param_name_lst_ref
    assert port_direction_lst == port_direction_ref  # Verify port directions


def test_jarbitrary_counter(project_root):
    """Test Jarbitrary Counter."""
    mod_name_ref = "jarbitraryCounter"
    port_name_lst_ref = ["OUTPUT", "clock", "reset"]
    param_name_lst_ref = []  # No parameters in this module
    port_width_lst_ref = ["[2:0]", None, None]  # Only OUTPUT has width specification
    port_direction_ref = ["output", "input", "input"]  # Port directions
    port_type_ref = ["reg", None, None]  # Port types (reg/wire)
    file_path = project_root / "tests" / "svfiles_examples" / "jarbitraryCounter.sv"

    mod_lst = parse_sv(file_path)

    mod = mod_lst[0]

    mod_name = mod.name
    port_name_lst = [port.name for port in mod.port_lst]
    port_width_lst = [port.width for port in mod.port_lst]
    param_name_lst = [param.name for param in mod.param_lst]
    port_direction_lst = [port.direction for port in mod.port_lst]
    port_type_lst = [port.ptype for port in mod.port_lst]  # Get port types

    assert mod_name == mod_name_ref
    assert port_name_lst == port_name_lst_ref
    assert port_width_lst == port_width_lst_ref
    assert param_name_lst == param_name_lst_ref
    assert port_direction_lst == port_direction_ref
    assert port_type_lst == port_type_ref  # Verify port types


def test_param_module(project_root):
    """Test Parameter Module."""
    # Reference values
    mod_name_ref = "param_module"
    port_name_lst_ref = ["clk", "rst_n", "data_in", "data_out", "bidir_bus"]
    param_name_lst_ref = ["WIDTH", "DEPTH", "INIT_VAL", "ENABLE_FEATURE"]
    port_width_lst_ref = [None, None, "[WIDTH-1:0]", "[WIDTH-1:0]", "[DEPTH-1:0]"]
    port_direction_ref = ["input", "input", "input", "output", "inout"]
    port_type_ref = ["wire", "wire", "wire", "reg", "wire"]

    # Instance references
    inst_name_ref = ["u_sub_module", "u_sub_module2"]

    file_path = project_root / "tests" / "svfiles_examples" / "param_module.sv"
    mod_lst = parse_sv(file_path)

    top_mod = next(m for m in mod_lst if m.name == mod_name_ref)

    # Basic module assertions
    assert top_mod.name == mod_name_ref
    assert [port.name for port in top_mod.port_lst] == port_name_lst_ref
    assert [port.width for port in top_mod.port_lst] == port_width_lst_ref
    assert [param.name for param in top_mod.param_lst] == param_name_lst_ref
    assert [port.direction for port in top_mod.port_lst] == port_direction_ref
    assert [port.ptype for port in top_mod.port_lst] == port_type_ref

    # Instance assertions
    assert len(top_mod.inst_decl) == 2
    for i, inst in enumerate(top_mod.inst_decl):
        assert inst.name == inst_name_ref[i]
        assert inst.module == "sub_module"

    # Verify submodule is also parsed
    sub_mod = next(m for m in mod_lst if m.name == "sub_module")
    assert sub_mod is not None
    assert [port.name for port in sub_mod.port_lst] == ["clk", "reset", "input_data", "output_data", "config_bus"]
