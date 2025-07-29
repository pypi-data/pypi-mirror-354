
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from parseable_dataclasses import ParseableDataClassMixin

@dataclass
class SuperTool(ParseableDataClassMixin):
    src: Path
    verbose: bool = False
    timeout: float = 10.0
    retly: int = 3
    prefix: str = "Hello"

    def __call__(self):
        pprint(self)

if __name__ == "__main__":
    tool = SuperTool.parse_args()
    tool()