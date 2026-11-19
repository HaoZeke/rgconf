# Copyright 2023--present rgconf developers
"""The committed parameter map matches the sources it names."""

import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "generated" / "parameter_map.tsv"
REPOS = {"eon": "eOn", "rgmin": "rgmin", "rgsaddle": "rgsaddle", "rgpot": "rgpot", "cpmdc": "cpmdc"}
SOURCES_ENV = "RGCONF_SOURCES"

# Every citation into these repositories is resolved against the source tree.
CHECKED_REPOS = ("rgmin", "rgpot")
# Individual citations into other repositories that are also resolved.
CHECKED_FIELDS = {
    ("rgsaddle", "rgsaddle_hyperplane_ti_config_t", "flags"),
    ("rgsaddle", "rgsaddle_band_config_t", "method"),
}

EXPECTED = [
    ("eon", "include/eon/ParametersOptions.h", "25", "constants_t", "kB", "8.6173324e-5"),
    ("eon", "include/eon/ParametersOptions.h", "26", "constants_t", "timeUnit", "10.1805055"),
    ("eon", "include/eon/ParametersOptions.h", "31", "main_options_t", "job", "JobType::Process_Search"),
    ("rgmin", "include/rgmin.h", "206", "rgmin_control_t", "maxiter", "100"),
    ("rgmin", "include/rgmin.h", "206", "rgmin_control_t", "gtol", "1e-5"),
    ("rgmin", "include/rgmin.h", "207", "rgmin_control_t", "maxmove", "0"),
    ("rgsaddle", "include/rgsaddle.h", "306", "rgsaddle_surface_request_t", "version", ""),
    ("rgsaddle", "include/rgsaddle.h", "307", "rgsaddle_surface_request_t", "flags", ""),
    ("rgsaddle", "include/rgsaddle.h", "308", "rgsaddle_surface_request_t", "n_images", ""),
    ("cpmdc", "schema/Potentials.capnp", "22", "ForceInput", "lengthUnit", '"angstrom"'),
    ("cpmdc", "schema/Potentials.capnp", "23", "ForceInput", "energyUnit", '"eV"'),
    ("cpmdc", "schema/Potentials.capnp", "25", "ForceInput", "charge", "0"),
    ("rgpot", "CppCore/rgpot/LennardJones/LJPot.hpp", "37", "LJConfig", "u0", "1.0"),
    ("rgpot", "CppCore/rgpot/LennardJones/LJPot.hpp", "38", "LJConfig", "cutoff", "15.0"),
    ("rgpot", "CppCore/rgpot/LennardJones/LJPot.hpp", "39", "LJConfig", "psi", "1.0"),
    ("rgpot", "CppCore/rgpot/LennardJones/LJPot.hpp", "43", "LJConfig", "switch_width", "0.0"),
]


def rows():
    for line in MAP.read_text().splitlines()[1:]:
        yield line.split("\t")


def test_expected_rows_are_present():
    have = {(row[0], row[1], row[2], row[3], row[4], row[6]) for row in rows()}
    for item in EXPECTED:
        assert item in have, item


def checked_rows():
    for row in rows():
        repo, _rel, _line, struct, field = row[:5]
        if repo in CHECKED_REPOS or (repo, struct, field) in CHECKED_FIELDS:
            yield row


def source_root():
    value = os.environ.get(SOURCES_ENV)
    if not value or not Path(value).is_dir():
        pytest.skip(f"set {SOURCES_ENV} to a directory holding the sibling source trees")
    return Path(value)


def test_checked_rows_exist():
    found = {row[0] for row in checked_rows()}
    assert set(CHECKED_REPOS) <= found
    for repo, struct, field in CHECKED_FIELDS:
        assert any(row[:1] + row[3:5] == [repo, struct, field] for row in rows()), (repo, struct, field)


def test_rows_quote_the_source_line():
    root = source_root()
    cache = {}
    stale = []
    for row in checked_rows():
        repo, rel, line, struct, field = row[:5]
        path = root / REPOS[repo] / rel
        if path not in cache:
            assert path.is_file(), f"missing source file {path}"
            cache[path] = path.read_text(errors="replace").splitlines()
        lines = cache[path]
        number = int(line)
        if number < 1 or number > len(lines):
            stale.append(f"{repo}:{rel}:{line} is past the end of the file ({struct}.{field})")
        elif not re.search(rf"\b{re.escape(field)}\b", lines[number - 1]):
            stale.append(f"{repo}:{rel}:{line} does not name {field} ({struct}): {lines[number - 1].strip()!r}")
    assert not stale, "\n".join(stale)
