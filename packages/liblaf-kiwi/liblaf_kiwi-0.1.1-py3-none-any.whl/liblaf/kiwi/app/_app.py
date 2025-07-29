import sys
from typing import Annotated

import cyclopts

from liblaf import grapes
from liblaf.kiwi._version import __version__

from ._hello import hello
from .ufw_geomap import ufw_geomap

app = cyclopts.App(name="kiwi", version=__version__)


@app.meta.default
def _(
    *tokens: Annotated[str, cyclopts.Parameter(show=False, allow_leading_hyphen=True)],
    log_level: Annotated[
        grapes.LogLevel, cyclopts.Parameter(env_var="LOGGING_LEVEL")
    ] = grapes.LogLevel.WARNING,
) -> int | None:
    grapes.init_logging(level=log_level)
    return app(tokens)


app.command(hello)
app.command(ufw_geomap)


def main() -> None:
    status: int | None = app.meta()
    if status is not None:
        sys.exit(status)
