# Parseable dataclasses

This library provides `parse_args` method to your dataclass.

## Install

`pip install git+https://github.com/m5ep12/parseable_dataclasses.git`

## Examples

### Simple dataclass

```python
@parseable_dataclass
@dataclass
class DC:
    a: int
    b: str
    opt: float = 3.141592
```

or

```python
@parseable_dataclass
class DC:
    a: int
    b: str
    opt: float = 3.141592
```

and parse

```python
assert, hasattr(DC, "parse_args")
dc = DC.parse_args("1 hello".split())
# dc(a=1, b="hello", opt=3.141592)
dc = DC.parse_args("1 hello 2.71828".split())
# dc(a=1, b="hello", opt=2.71828)
```

### Generate help-text

```python
dc = DC.parse_args(["-h"])
usage: DC [-h] [--opt OPT] a b

positional arguments:
  a           int
  b           str

options:
  -h, --help  show this help message and exit
  --opt OPT   float
```

### Make CLI

```python
from pathlib import Path
from pprint import pprint
from parseable_dataclasses import parseable_dataclass

@parseable_dataclass
class SuperTool:
    src: list[Path]
    verbose: bool = False
    timeout: float = 10.0
    retly: int = 3
    prefix: str = "Hello"

    def __call__(self):
        # implementation your tool
        pprint(self)

if __name__ == "__main__":
    tool = SuperTool.parse_args()
    tool()
```

```bash
$ python examples/make_cli.py -h
usage: SuperTool [-h] [--verbose | --no-verbose] [--timeout TIMEOUT] [--retly RETLY] [--prefix PREFIX] src

positional arguments:
  src                   Path

options:
  -h, --help            show this help message and exit
  --verbose, --no-verbose
                        bool (default: False)
  --timeout TIMEOUT     float (default: 10.0)
  --retly RETLY         int (default: 3)
  --prefix PREFIX       str (default: Hello)

$ python examples/make_cli.py --verbose aaa/bbb.py
SuperTool(src=WindowsPath('aaa/bbb.py'),
          verbose=True,
          timeout=10.0,
          retly=3,
          prefix='Hello')

$ 
```

## Limitations

### tuple

Due to my inability, I have not implemented to accept a complex tuple like following.
(I'd like to convert this dataclass, but I can't find a nice implementation...)

```python
@parseable_dataclass
@dataclass
class SomeClass:
    a: tuple[int, str, float]
```
