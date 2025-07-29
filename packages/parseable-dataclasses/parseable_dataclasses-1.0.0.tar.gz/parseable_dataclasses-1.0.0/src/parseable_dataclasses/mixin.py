""" parseable-dataclasses
    Examples:
        ```python
        @parseable_dataclass
        @dataclass
        class DC:
            a: int
            b: str
            opt: float = 3.141592
        
        assert, hasatter(DC, "parse_args")
        dc = DC.parse_args(["1 hello"].split())
        # dc(a=1, b="hello", opt=3.141592)
        dc = DC.parse_args(["1 hello 2.71828"].split())
        # dc(a=1, b="hello", opt=2.71828)
    
        # or

        @parseable_dataclass
        class DC:
            a: int
            b: str
            opt: float = 3.141592
        ```
"""
from abc import ABC
from dataclasses import MISSING, dataclass, fields, Field, is_dataclass
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, BooleanOptionalAction
from typing import Literal, Self, Sequence, assert_never, get_args, get_origin

# I referenced https://github.com/lidatong/dataclasses-json

def parseable_dataclass(cls: type):
    """parsearble_dataclass

    Args:
        cls (type): an dataclass

    Returns:
        cls (type): an parseable_dataclass
    """
    if issubclass(cls, ParseableDataClassMixin):
        return cls

    if not is_dataclass(cls):
        cls = dataclass(cls)
    assert not hasattr(cls, "parse_args")
    cls.parse_args = classmethod(ParseableDataClassMixin.parse_args.__func__) # type: ignore
    cls.parser = classmethod(ParseableDataClassMixin.parser.__func__) # type: ignore
    ParseableDataClassMixin.register(cls)
    return cls

class ParseableDataClassMixin(ABC):

    @classmethod
    def parse_args(cls, args: Sequence[str] | None = None) -> Self:
        """parse_args to generate an instance

        Args:
            args (Sequence[str] | None, optional): Defaults to None.

        Returns:
            Self:
        """
        parser = cls.parser()
        namespace = parser.parse_args(args=args)
        return cls(**vars(namespace))

    @classmethod
    def parser(cls, *args, **kw_args) -> ArgumentParser:
        """generate the instance of ArgumentParser to parse

        Raises:
            NotImplementedError:
            assert_never:

        Returns:
            ArgumentParser: 
        """
        assert is_dataclass(cls), f"This mixin must be inherited to a dataclass, but {cls=} is not in dataclasses."
        if len(args) == 0 and "prog" not in kw_args:
            kw_args["prog"] = cls.__name__
        if "formatter_class" not in kw_args:
            kw_args["formatter_class"] = ArgumentDefaultsHelpFormatter
        parser = ArgumentParser(*args, **kw_args)
        for field in fields(cls):
            name = field.name if _is_positional(field) else "--" + field.name
            default = field.name if _is_positional(field) else "--" + field.name
            if _is_positional(field):
                name = field.name
                default = None
            else:
                name = "--" + field.name
                if field.default is not MISSING:
                    default = field.default
                else:
                    assert callable(field.default_factory), f"default_factory must be callable, but {field.default_factory=} is not callable!"
                    default = field.default_factory()

            match field.type:
                case type() as t if t in (int, float, str):
                    # p: T
                    text = t.__name__
                    parser.add_argument(name, default=default, type=t, help=text)
                case type() as t if t == bool:
                    # p: bool
                    text = t.__name__
                    parser.add_argument(name, default=default, action=BooleanOptionalAction, help=text)
                case type() as t if t == list:
                    # p: list
                    text = "list[str]"
                    parser.add_argument(name, default=default, nargs="*", type=str, help=text)
                case type() as t if t == tuple:
                    # p: tupe
                    text = "tuple[str, ...]"
                    parser.add_argument(name, default=default, nargs="*", type=str, help=text)
                case type() as t if callable(t):
                    # p: Cls, i.e. Path
                    text = t.__name__
                    parser.add_argument(name, default=default, type=t, help=text)
                case t if get_origin(t) == list:
                    # p: list[T]
                    arg: type = get_args(t)[0]
                    text = f"list[{arg.__name__}]"
                    parser.add_argument(name, default=default, nargs="*", type=arg, help=text)
                case t if get_origin(t) == tuple:
                    # p: tuple[*Ts]
                    raise NotImplementedError("I'm so sorry, tuple[*Ts] has not been implemented yet!")
                    ts = get_args(t)
                    text = "(" + ",".join([arg.__name__ for arg in ts if isinstance(arg, type)]) + ")"
                    parser.add_argument(name, default=default, nargs=len(ts), type=str, help=text)
                case t if get_origin(t) == Literal:
                    # p: Literal[...]
                    ts = get_args(t)
                    types = set(map(type, ts))
                    assert len(types) == 1, "all the types of a literal field must be the same, but there are multiple types in this literal field as {types=}."
                    typeofliteral = types.pop()
                    text = typeofliteral.__name__
                    parser.add_argument(name, default=default, choices=ts, type=typeofliteral, help=text)
                case _ as never:
                    raise assert_never(never) # type: ignore
        return parser


def _is_positional(field: Field) -> bool:
    """return True if input is a positional field

    Args:
        field (Field):

    Returns:
        bool: True/False
    """
    return field.default is MISSING and field.default_factory is MISSING

def _is_optional(field: Field) -> bool:
    """return True if input is a optional field

    Args:
        field (Field):

    Returns:
        bool: True/False
    """
    return not _is_positional(field)