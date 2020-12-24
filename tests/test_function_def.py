import pytest

from aesqlapius.function_def import (
    ArgumentDefinition,
    FunctionDefinition,
    ReturnValueDefinition,
    ReturnValueInnerFormat,
    ReturnValueOuterFormat,
    parse_function_definition
)


def test_simple():
    assert parse_function_definition(
        'def Foo() -> None: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=None
    )


def test_args_unannotated():
    assert parse_function_definition(
        'def Foo(a, b, c) -> None: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[
            ArgumentDefinition(name='a'),
            ArgumentDefinition(name='b'),
            ArgumentDefinition(name='c'),
        ],
        returns=None
    )


def test_args():
    assert parse_function_definition(
        'def Foo(a: int, b: str, c: float) -> None: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[
            ArgumentDefinition(name='a'),
            ArgumentDefinition(name='b'),
            ArgumentDefinition(name='c'),
        ],
        returns=None
    )


def test_default_args():
    assert parse_function_definition(
        'def Foo(a: int, b: int=2, c: int=3) -> None: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[
            ArgumentDefinition(name='a'),
            ArgumentDefinition(name='b', has_default=True, default=2),
            ArgumentDefinition(name='c', has_default=True, default=3),
        ],
        returns=None
    )


def test_returns_outer_iterator():
    assert parse_function_definition(
        'def Foo() -> Iterator[Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.ITERATOR,
            inner_format=ReturnValueInnerFormat.TUPLE
        )
    )


def test_returns_outer_list():
    assert parse_function_definition(
        'def Foo() -> List[Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.LIST,
            inner_format=ReturnValueInnerFormat.TUPLE
        )
    )


def test_returns_outer_single():
    assert parse_function_definition(
        'def Foo() -> Single[Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.SINGLE,
            inner_format=ReturnValueInnerFormat.TUPLE
        )
    )


def test_returns_outer_dict():
    assert parse_function_definition(
        'def Foo() -> Dict[0, Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.DICT,
            inner_format=ReturnValueInnerFormat.TUPLE,
            outer_dict_by=0
        )
    )

    assert parse_function_definition(
        'def Foo() -> Dict["colname", Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.DICT,
            inner_format=ReturnValueInnerFormat.TUPLE,
            outer_dict_by='colname'
        )
    )


def test_returns_outer_dict_remove_key():
    assert parse_function_definition(
        'def Foo() -> Dict[-0, Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.DICT,
            inner_format=ReturnValueInnerFormat.TUPLE,
            outer_dict_by=0,
            remove_key_column=True
        )
    )

    assert parse_function_definition(
        'def Foo() -> Dict[-"colname", Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.DICT,
            inner_format=ReturnValueInnerFormat.TUPLE,
            outer_dict_by='colname',
            remove_key_column=True
        )
    )


def test_returns_inner_tuple():
    assert parse_function_definition(
        'def Foo() -> Single[Tuple]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.SINGLE,
            inner_format=ReturnValueInnerFormat.TUPLE
        )
    )


def test_returns_inner_dict():
    assert parse_function_definition(
        'def Foo() -> Single[Dict]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.SINGLE,
            inner_format=ReturnValueInnerFormat.DICT
        )
    )


def test_returns_inner_value():
    assert parse_function_definition(
        'def Foo() -> Single[Value]: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[],
        returns=ReturnValueDefinition(
            outer_format=ReturnValueOuterFormat.SINGLE,
            inner_format=ReturnValueInnerFormat.VALUE
        )
    )


def test_returns_invalid_outer():
    with pytest.raises(TypeError):
        parse_function_definition('def Foo() -> BadType[List]: ...')


def test_returns_invalid_inner():
    with pytest.raises(TypeError):
        parse_function_definition('def Foo() -> List[BadType]: ...')


@pytest.mark.xfail
def test_accepts_complex_arg_annotations():
    assert parse_function_definition(
        'def Foo(arg: Tuple[str, int]) -> None: ...'
    ) == FunctionDefinition(
        name='Foo',
        args=[
            ArgumentDefinition(name='arg'),
        ]
    )


@pytest.mark.xfail
def test_accepts_complex_return_annotations():
    parse_function_definition('def Foo() -> Single[Value[bool]]: ...')
    parse_function_definition('def Foo() -> Single[Value[Tuple[str, int]]]: ...')
