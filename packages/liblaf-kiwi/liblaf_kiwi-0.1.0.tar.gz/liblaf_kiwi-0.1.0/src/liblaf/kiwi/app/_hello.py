from typing import Annotated

import cyclopts


def hello(name: Annotated[str, cyclopts.Argument()] = "world", /) -> None:
    print(f"Hello, {name}!")
