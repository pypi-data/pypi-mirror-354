from pathlib import Path
from unittest import TestCase
from dataclasses import dataclass

from parseable_dataclasses import mixin

@dataclass
class DC1(mixin.ParseableDataClassMixin):
    a: int

@dataclass
class DC2(mixin.ParseableDataClassMixin):
    a: int
    b: float
    c: str

@dataclass
class DC3(mixin.ParseableDataClassMixin):
    a: int
    b: float
    c: str
    d: bool = False

@dataclass
class DC4(mixin.ParseableDataClassMixin):
    a: list[int]

@dataclass
class DC5(mixin.ParseableDataClassMixin):
    a: Path

@dataclass
class DC6(mixin.ParseableDataClassMixin):
    a: tuple[int, str, float]


class Test_ParsearbleDataClassMixin(TestCase):
    def test_parse_dc1(self):
        expected = DC1(10)
        actual = DC1.parse_args("10".split())

        self.assertEqual(expected, actual)

    def test_parse_dc2(self):
        expected = DC2(10, 3.1415, "Hello")
        actual = DC2.parse_args("10 3.1415 Hello".split())

        self.assertEqual(expected, actual)

    def test_parse_dc3(self):
        expected = DC3(10, 3.1415, "Hello", d=True)
        actual = DC3.parse_args("--d 10 3.1415 Hello".split())

        self.assertEqual(expected, actual)
        
        expected = DC3(10, 3.1415, "Hello", d=False)
        actual = DC3.parse_args("--no-d 10 3.1415 Hello".split())

        self.assertEqual(expected, actual)

    def test_parse_dc4(self):
        expected = DC4([1, 2, 3, 4, 5, 6])
        actual = DC4.parse_args("1 2 3 4 5 6".split())

        self.assertEqual(expected, actual)
        
        expected = DC4([])
        actual = DC4.parse_args("".split())

        self.assertEqual(expected, actual)
        
        expected = DC4([0])
        actual = DC4.parse_args("0".split())

        self.assertEqual(expected, actual)

    def test_parse_dc5(self):
        expected = DC5(Path("aaa"))
        actual = DC5.parse_args("aaa".split())

        self.assertEqual(expected, actual)
        
        expected = DC5(Path("."))
        actual = DC5.parse_args(".".split())

        self.assertEqual(expected, actual, msg=DC5.parser().format_help())
        
    def test_parse_dc6(self):
        # expected = DC6((1, "2", 3.0))
        # actual = DC6.parse_args("1 2 3.0".split())

        #self.assertRaises(expected, actual, msg=DC6.ArgumentParser().format_help())
        with self.assertRaises(NotImplementedError):
            DC6.parse_args("1 2 3.0".split())

class TestDecorator(TestCase):
    def test_simple_decoration(self):
        
        @mixin.parseable_dataclass
        @dataclass
        class DC:
            a: int
            b: float
        
        expected = DC(1, 2.0)
        actual = DC.parse_args("1 2.0".split())
        self.assertEqual(expected, actual)

    def test_single_decoration(self):
        
        @mixin.parseable_dataclass
        class DC:
            a: int
            b: float
        
        expected = DC(1, 2.0)
        actual = DC.parse_args("1 2.0".split())
        self.assertEqual(expected, actual)