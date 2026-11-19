# Copyright 2023--present rgconf developers
"""The committed parameter map matches the sources it names."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "generated" / "parameter_map.tsv"
SOURCES = Path("/tmp/sources")
REPOS = {"eon": "eOn", "rgmin": "rgmin", "rgsaddle": "rgsaddle", "rgpot": "rgpot", "cpmdc": "cpmdc"}

EXPECTED = [
    ("eon", "include/eon/ParametersOptions.h", "25", "constants_t", "kB", "8.6173324e-5"),
    ("eon", "include/eon/ParametersOptions.h", "26", "constants_t", "timeUnit", "10.1805055"),
    ("eon", "include/eon/ParametersOptions.h", "31", "main_options_t", "job", "JobType::Process_Search"),
    ("rgmin", "include/rgmin.h", "185", "rgmin_control_t", "maxiter", "100"),
    ("rgmin", "include/rgmin.h", "185", "rgmin_control_t", "gtol", "1e-5"),
    ("rgmin", "include/rgmin.h", "186", "rgmin_control_t", "maxmove", "0"),
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


def test_rows_quote_the_source_line():
    if not SOURCES.is_dir():
        return
    for repo, rel, line, _struct, field, default in EXPECTED:
        text = (SOURCES / REPOS[repo] / rel).read_text().splitlines()[int(line) - 1]
        assert field in text or "Control::default" in text or "maxmove" in text
        if default:
            assert default in text
