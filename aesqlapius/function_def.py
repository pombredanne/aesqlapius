from enum import Enum, unique
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union
import ast


@dataclass
class ArgumentDefinition:
    name: str
    type_: Any = None
    has_default: bool = False
    default: Any = None


@unique
class ReturnValueOuterFormat(Enum):
    ITERATOR = 1
    LIST = 2
    SINGLE = 3
    #DICT = 4  # TODO


@unique
class ReturnValueInnerFormat(Enum):
    TUPLE = 1
    DICT = 2
    LIST = 3


@dataclass
class ReturnValueDefinition:
    outer_format: ReturnValueOuterFormat
    inner_format: Union[ReturnValueInnerFormat, str]


@dataclass
class FunctionDefinition:
    name: str
    args: List[ArgumentDefinition] = field(default_factory=list)
    returns: Optional[ReturnValueDefinition] = None


def parse_function_definition(source: str) -> FunctionDefinition:
    tree = ast.parse(source)

    assert(len(tree.body) == 1)
    assert(isinstance(tree.body[0], ast.FunctionDef))

    func = tree.body[0]

    func_def = FunctionDefinition(name=func.name)

    # parse arguments
    for arg in func.args.args:
        arg_def = ArgumentDefinition(
            name = arg.arg,
            type_ = arg.annotation.id if arg.annotation else None  # XXX: complex type parsing
        )

        func_def.args.append(arg_def)

    # parse default values
    first_default_idx = len(func.args.args) - len(func.args.defaults)

    for argn, default in enumerate(func.args.defaults, first_default_idx):
        assert(isinstance(default, ast.Constant))

        func_def.args[argn].has_default = True
        func_def.args[argn].default = default.value

    # parse return value
    returns = func.returns

    if isinstance(returns, ast.Constant) and returns.value is None:
        func_def.returns = None
    else:
        assert(isinstance(returns, ast.Subscript))

        if returns.value.id in ('List', 'list'):
            outer_format = ReturnValueOuterFormat.LIST
        elif returns.value.id == 'Iterator':
            outer_format = ReturnValueOuterFormat.ITERATOR
        elif returns.value.id == 'Single':
            outer_format = ReturnValueOuterFormat.SINGLE
        else:
            raise TypeError(f'Unexpected return value type {returns.value.id}')

        if returns.slice.id in ('Tuple', 'tuple'):
            inner_format = ReturnValueInnerFormat.TUPLE
        elif returns.slice.id in ('Dict', 'dict'):
            inner_format = ReturnValueInnerFormat.DICT
        elif returns.slice.id in ('List', 'list'):
            inner_format = ReturnValueInnerFormat.LIST
        else:  # custom type
            inner_format = returns.slice.id

        func_def.returns = ReturnValueDefinition(outer_format, inner_format)

    # check body
    assert(len(func.body) == 1)
    assert(isinstance(func.body[0], ast.Expr))
    assert(isinstance(func.body[0].value, ast.Constant))
    assert(func.body[0].value.value is Ellipsis)

    return func_def
