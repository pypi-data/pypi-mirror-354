import functools
import io
import itertools
import subprocess as sp
from collections.abc import Generator
from pathlib import Path

from liblaf import grapes

with grapes.optional_imports("liblaf-kiwi", "ufw-geomap"):
    import polars as pl

SCHEMA_OVERRIDES: dict[str, type] = {
    "__MONOTONIC_TIMESTAMP": pl.UInt64,
    "__REALTIME_TIMESTAMP": pl.Datetime,
    "__SEQNUM": pl.UInt64,
    "_SOURCE_BOOTTIME_TIMESTAMP": pl.UInt64,
    "_SOURCE_MONOTONIC_TIMESTAMP": pl.UInt64,
    "PRIORITY": pl.UInt64,
    "SYSLOG_FACILITY": pl.UInt64,
}


def load_logs(*logs: Path) -> pl.DataFrame:
    data: pl.DataFrame = pl.concat(
        df.select(columns())
        for df in itertools.chain(
            load_logs_journalctl(*logs),
            load_logs_csv(*logs),
            load_logs_jsonl(*logs),
        )
    )
    data = data.unique(("__CURSOR", "__REALTIME_TIMESTAMP"))
    return data


@functools.cache
def columns() -> list[str]:
    args: list[str] = [
        "journalctl",
        "--boot=all",
        "--identifier=kernel",
        r"--grep=^\[UFW BLOCK\]",
        "--output=json",
        "--lines=1",
    ]
    process: sp.CompletedProcess[str] = sp.run(
        args, stdout=sp.PIPE, check=True, text=True
    )
    data: pl.DataFrame = pl.read_ndjson(io.StringIO(process.stdout))
    return data.columns


def load_logs_journalctl(*logs: Path) -> Generator[pl.DataFrame]:
    if len(logs) > 0:
        return
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
    yield _load_logs_jsonl(io.StringIO(process.stdout))


def load_logs_csv(*logs: Path) -> Generator[pl.DataFrame]:
    for file in logs:
        if file.suffix != ".csv":
            continue
        yield pl.read_csv(file, schema_overrides=SCHEMA_OVERRIDES)


def load_logs_jsonl(*logs: Path) -> Generator[pl.DataFrame]:
    source: list[Path] = [
        file
        for file in logs
        if file.name.endswith((".jsonl", ".jsonl.gz", ".ndjson", ".ndjson.gz"))
    ]
    if len(source) == 0:
        return
    yield _load_logs_jsonl(source)


def _load_logs_jsonl(
    source: str | Path | list[str] | list[Path] | io.IOBase | bytes,
) -> pl.DataFrame:
    data: pl.DataFrame = pl.read_ndjson(source)
    data = data.with_columns(
        pl.col("__REALTIME_TIMESTAMP").cast(pl.UInt64).cast(pl.Datetime)
    )
    for column, dtype in SCHEMA_OVERRIDES.items():
        if column in data.columns:
            data = data.with_columns(pl.col(column).cast(dtype))
    return data
