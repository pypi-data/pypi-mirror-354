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

from importlib.resources import files

from jinja2 import Environment, FileSystemLoader
from rich.table import Table, box

template_path = files("sv_simpleparser.Templates")


def gen_instance(module_obj):
    module_name = module_obj.name
    port_lst = [port.name for port in module_obj.port_lst]
    param_lst = [param.name for param in module_obj.param_lst]
    param_lst = [param.name for param in module_obj.param_lst]

    environment = Environment(loader=FileSystemLoader(template_path))

    if param_lst:
        inst_temp = environment.get_template("instance_with_param_template")

        instance_file = inst_temp.render(module_name=module_name, param_list=param_lst, port_list=port_lst)
    else:
        inst_temp = environment.get_template("instance_template")

        instance_file = inst_temp.render(module_name=module_name, port_list=port_lst)

    return instance_file


def remove_slashes_and_newlines(input_string):
    # Replace '//' with an empty string
    result = input_string.replace("//", "")
    # Replace '\n' with an empty string
    result = result.replace("\n", "")
    return result.strip()


def gen_markdown_table(module_obj):
    module_name = module_obj.name
    port_lst = [port.name for port in module_obj.port_lst]
    width_lst = [rf"{port.width[:-1]}]" if port.width is not None else "1" for port in module_obj.port_lst]
    comment_lst = [
        remove_slashes_and_newlines(port.comment[0]) if port.comment is not None else "" for port in module_obj.port_lst
    ]
    direction_lst = [port.direction for port in module_obj.port_lst]

    table = Table(title=f"{module_name} interface", box=box.MARKDOWN)

    table.add_column("Signal Name", no_wrap=True)
    table.add_column("Width", justify="center", no_wrap=True)
    table.add_column("I/O", justify="center", no_wrap=True)
    table.add_column("Functional Description")

    for port, width, direction, comment in zip(port_lst, width_lst, direction_lst, comment_lst, strict=False):
        table.add_row(port, width, direction, comment)

    return table
