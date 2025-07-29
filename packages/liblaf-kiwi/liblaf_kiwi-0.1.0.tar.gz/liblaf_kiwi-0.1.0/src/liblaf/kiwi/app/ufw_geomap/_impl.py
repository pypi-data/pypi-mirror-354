import functools
import io
import re
import subprocess as sp
from pathlib import Path
from typing import Any

from liblaf import grapes
from liblaf.grapes.typed import PathLike

with grapes.optional_imports("liblaf-kiwi", "ufw-geomap"):
    import folium
    import folium.plugins
    import geoip2.database
    import geoip2.errors
    import geoip2.models
    import polars as pl


def ufw_geomap_impl(
    *log_files: Path,
    geoip: Path,
    output_csv: Path | None = None,
    output_html: Path | None = None,
) -> None:
    logs: pl.DataFrame = load_logs(*log_files)
    db = geoip2.database.Reader(geoip)
    logs = logs.with_columns(
        pl.col("MESSAGE").map_elements(parse_message, pl.Struct).alias("MESSAGE_PARSED")
    ).unnest("MESSAGE_PARSED")
    logs = logs.with_columns(
        pl.col("SRC")
        .map_elements(functools.partial(query_ip, db=db), pl.Struct)
        .alias("SRC_GEOIP"),
    ).unnest("SRC_GEOIP")
    if output_csv is not None:
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        logs.write_csv(output_csv)
    if output_html is not None:
        plot_data(logs, outfile=output_html)


def load_logs(*logs: Path) -> pl.DataFrame:
    source: Any
    if len(logs) == 0:
        args: list[str] = [
            "journalctl",
            "--boot=all",
            "--identifier=kernel",
            r"--grep=^\[UFW BLOCK\]",
            "--output=json",
        ]
        process: sp.CompletedProcess[str] = sp.run(
            args, stdout=sp.PIPE, check=True, text=True
        )
        source = io.StringIO(process.stdout)
    else:
        source = list(logs)
    data: pl.DataFrame = pl.read_ndjson(source)
    data = data.with_columns(
        pl.col("__REALTIME_TIMESTAMP").cast(pl.UInt64).cast(pl.Datetime)
    )
    return data


def parse_message(message: str) -> dict[str, str]:
    message = message.removeprefix("[UFW BLOCK]")
    message = re.sub(r"\[.*?\]", "", message)
    message = message.strip()
    parsed: dict[str, str] = {}
    for pair in message.split():
        key: str
        value: str
        key, _, value = pair.partition("=")
        parsed[key] = value
    return parsed


@functools.lru_cache
def query_ip(ip: str, db: geoip2.database.Reader) -> dict[str, Any]:
    try:
        city: geoip2.models.City = db.city(ip)
    except geoip2.errors.AddressNotFoundError:
        return {"longitude": None, "latitude": None, "country": None, "city": None}
    return {
        "city": city.city.name,
        "country": city.country.name,
        "latitude": city.location.latitude,
        "longitude": city.location.longitude,
    }


def plot_data(data: pl.DataFrame, outfile: PathLike | None = None) -> folium.Map:
    fig = folium.Map()
    cluster = folium.plugins.FastMarkerCluster(
        data.select("latitude", "longitude").drop_nulls().to_numpy().tolist(),
    )
    fig.add_child(cluster)
    fig.fit_bounds(
        (
            (data["latitude"].min(), data["longitude"].min()),
            (data["latitude"].max(), data["longitude"].max()),
        )  # pyright: ignore[reportArgumentType]
    )
    if outfile is not None:
        outfile = Path(outfile)
        outfile.parent.mkdir(parents=True, exist_ok=True)
        fig.save(outfile)
    return fig
