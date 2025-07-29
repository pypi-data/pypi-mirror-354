from pathlib import Path
from typing import Annotated

import cyclopts


def ufw_geomap(
    *log_files: Annotated[cyclopts.types.ResolvedExistingFile, cyclopts.Argument()],
    geoip: Annotated[cyclopts.types.ResolvedExistingFile, cyclopts.Parameter()] = Path(  # noqa: B008
        "~/.local/share/geoip/GeoLite2-City.mmdb"
    ).expanduser(),
    output_csv: Annotated[
        cyclopts.types.ResolvedFile | None, cyclopts.Parameter()
    ] = None,
    output_html: Annotated[
        cyclopts.types.ResolvedFile | None, cyclopts.Parameter()
    ] = None,
) -> None:
    from ._impl import ufw_geomap_impl

    ufw_geomap_impl(
        *log_files,
        geoip=geoip,
        output_csv=output_csv,
        output_html=output_html,
    )
