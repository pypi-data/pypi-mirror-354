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


"""The parser.

The parser offers two methods:

* [sv_simpleparser.parser.parse_file][]
* [sv_simpleparser.parser.parse_text][]
"""

import logging
from dataclasses import dataclass
from pathlib import Path

from . import datamodel as dm
from ._hdl import SystemVerilogLexer
from ._token import Module

LOGGER = logging.getLogger(__name__)


@dataclass
class _ModInstance:
    """Represents an instance of a module within another module.

    Attributes:
        name: Instance name
        module: Name of the module being instantiated
        connections: List of port connections in order of declaration
    """

    name: str | None = None
    module: str | None = None
    connections: list[str] | None = None

    def proc_tokens(self, token, string):
        if token == Module.Body.Instance.Name:
            self.name = string
        elif token == Module.Body.Instance.Connections:
            self.connections = string


@dataclass
class _PortDeclaration:
    """Represents a port declaration block in SystemVerilog.

    Attributes:
        direction: Port direction ('input', 'output', 'inout')
        ptype: Port type ('wire', 'reg', 'logic', etc.)
        name: List of port names in this declaration
        width: Bus width specification if applicable
        comment: List of associated comments
    """

    direction: str
    ptype: str | None = None
    name: list[str] | None = None
    width: str | None = None
    comment: list[str] | None = None

    def proc_tokens(self, token, string):
        """Processes Module.Port tokens and extract data."""
        if token == Module.Port.PortDirection:
            self.direction = string
        elif token == Module.Port.PortType:
            self.ptype = string
        elif token == Module.Port.PortName:
            if self.name is None:
                self.name = [string]
            else:
                self.name.append(string)
        elif token == Module.Port.PortWidth:
            self.width = string
        elif token == Module.Port.Comment:
            if self.comment is None:
                self.comment = [string]
            else:
                self.comment.append(string)


@dataclass
class _ParamDeclaration:
    """Represents a parameter declaration block in SystemVerilog.

    Attributes:
        ptype: Parameter type ('integer', 'real', etc.)
        name: List of parameter names in this declaration
        width: Bus width specification if applicable
        comment: List of associated comments
    """

    ptype: str | None = None
    name: list[str] | None = None
    width: str | None = None
    comment: list[str] | None = None

    def proc_tokens(self, token, string):
        """Processes Module.Param tokens and extract data."""
        if token == Module.Param.ParamType:
            self.ptype = string
        elif token == Module.Param.ParamName:
            if self.name is None:
                self.name = [string]
            else:
                self.name.append(string)
        elif token == Module.Param.ParamWidth:
            self.width = string
        elif token == Module.Param.Comment:
            if self.comment is None:
                self.comment = [string]
            else:
                self.comment.append(string)


class _SvModule:
    """Represents a complete SystemVerilog module with all its components.

    Attributes:
        name: Name of the module
        port_lst: List of Port objects
        param_lst: List of Param objects
        inst_dict: Dictionary of module instances (instance name -> module)
        port_decl: List of PortDeclaration objects
        param_decl: List of ParamDeclaration objects
        inst_decl: List of instance declarations
    """

    def __init__(self):
        self.name: str | None = None
        self.port_lst: list[dm.Port] = []
        self.param_lst: list[dm.Param] = []
        self.inst_dict: dict[str, str] = {}

        self.port_decl: list[_PortDeclaration] = []
        self.param_decl: list[_ParamDeclaration] = []
        self.inst_decl: list[_ModInstance] = []

    def _gen_port_lst(self):
        for decl in self.port_decl:
            for name in decl.name:
                port = dm.Port(
                    name=name, direction=decl.direction, ptype=decl.ptype, width=decl.width, comment=decl.comment
                )
                self.port_lst.append(port)

    def _gen_param_lst(self):
        for decl in self.param_decl:
            for name in decl.name:
                param = dm.Param(name=name, ptype=decl.ptype, width=decl.width, comment=decl.comment)
                self.param_lst.append(param)

    def _gen_inst_dict(self):
        for decl in self.inst_decl:
            self.inst_dict[decl.name] = decl.module

    def proc_tokens(self, token, string):
        # Capture a new port declaration object if input/output keywords are found
        if token[:2] == ("Module", "Port"):
            if token[-1] == ("PortDirection"):
                self.port_decl.append(_PortDeclaration(direction=string))
            else:
                self.port_decl[-1].proc_tokens(token, string)

        # Capture parameters, when Module.Param tokens are found
        elif token[:2] == ("Module", "Param"):
            if token is Module.Param:
                self.param_decl.append(_ParamDeclaration())
            else:
                self.param_decl[-1].proc_tokens(token, string)

        # Capture Modules
        elif token[:2] == ("Module", "ModuleName"):
            self.name = string

        # Capture instances
        elif token[:3] == ("Module", "Body", "Instance"):
            if token == Module.Body.Instance.Module:
                self.inst_decl.append(_ModInstance(module=string))
            else:
                self.inst_decl[-1].proc_tokens(token, string)

    def __str__(self):  # noqa: C901
        output = []

        # Module name
        output.append(f"Module: {self.name}\n")

        # Parameters
        if self.param_lst:
            output.append("Parameters:")
            for param in self.param_lst:
                param_info = [
                    f"  {param.name}",
                    f"type={param.ptype}" if param.ptype else "",
                    f"width={param.width}" if param.width else "",
                    f"comment={param.comment}" if param.comment else "",
                ]
                output.append(" ".join(filter(None, param_info)))
            output.append("")

        # Parameter Declarations
        if self.param_decl:
            output.append("Parameter Declarations:")
            for decl in self.param_decl:
                decl_info = [
                    f"  {', '.join(decl.name)}",
                    f"type={decl.ptype}" if decl.ptype else "",
                    f"width={decl.width}" if decl.width else "",
                    f"comment={decl.comment}" if decl.comment else "",
                ]
                output.append(" ".join(filter(None, decl_info)))
            output.append("")

        # Ports
        if self.port_lst:
            output.append("Ports:")
            for port in self.port_lst:
                port_info = [
                    f"  {port.direction} {port.name}",
                    f"type={port.ptype}" if port.ptype else "",
                    f"width={port.width}" if port.width else "",
                    f"comment={port.comment}" if port.comment else "",
                ]
                output.append(" ".join(filter(None, port_info)))
            output.append("")

        # Port Declarations
        if self.port_decl:
            output.append("Port Declarations:")
            for decl in self.port_decl:
                decl_info = [
                    f"  {decl.direction} {', '.join(decl.name)}",
                    f"type={decl.ptype}" if decl.ptype else "",
                    f"width={decl.width}" if decl.width else "",
                    f"comment={decl.comment}" if decl.comment else "",
                ]
                output.append(" ".join(filter(None, decl_info)))
            output.append("")

        # Instances
        if self.inst_dict:
            output.append("Instances:")
            for inst_name, inst in self.inst_dict.items():
                output.append(f"  {inst_name} ({inst.module})")
                if inst.connections:
                    output.append("    Connections:")
                    output.extend(f"      {conn}" for conn in inst.connections)
            output.append("")

        return "\n".join(output)


def parse_file(file_path: Path | str) -> dm.File:
    """Parse a SystemVerilog file.

    Args:
        file_path: Path to the SystemVerilog file.

    Returns:
        Parsed Data
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    return parse_text(file_path.read_text(), file_path=file_path)


def parse_text(text: str, file_path: Path | str | None = None) -> dm.File:
    """Parse a SystemVerilog text.

    Args:
        text: SystemVerilog Statements.

    Keyword Args:
        file_path: Related File Path.

    Returns:
        Parsed Data
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    module_lst = _parse_text(text)

    modules = tuple(
        dm.Module(
            name=mod.name,
            params=mod.param_lst,
            ports=mod.port_lst,
            insts=tuple(dm.ModuleInstance(name=inst.name, module=inst.module) for inst in mod.inst_decl),
        )
        for mod in module_lst
    )

    return dm.File(path=file_path, modules=modules)


def _parse_text(text: str):
    lexer = SystemVerilogLexer()
    module_lst = []
    for token, string in lexer.get_tokens(text):
        LOGGER.debug(f"({token}, {string})")
        # New module was found
        if token == Module.ModuleStart:
            module_lst.append(_SvModule())
        elif "Module" in token[:]:
            module_lst[-1].proc_tokens(token, string)

    for mod in module_lst:
        mod._gen_port_lst()
        mod._gen_param_lst()
        mod._gen_inst_dict()

    return module_lst
