# Copyright 2023--present rgconf developers

from rgconf import abi_version, resolve_ini

ABI = (0 << 16) | (1 << 8) | 0


def test_abi_version_matches_header():
    assert abi_version() == ABI


def test_resolve_ini_reads_optimizer_force():
    text = "[Optimizer]\nconverged_force = 0.03\n"
    body = resolve_ini("eonLegacyIni", text, "client.ini")
    assert "optimizer.convergence.forceToleranceEvPerAngstrom=0.03" in body


def test_native_extension_is_loaded():
    from rgconf import _core

    assert _core.resolve_ini
    assert _core.abi_version() == ABI


def test_native_resolution_exposes_instanton_defaults():
    from rgconf import _core

    lines = _core.resolve_ini("eonLegacyIni", "", "client.ini").splitlines()
    assert "instanton.numBeads=16 defaultValue" in lines


def test_eon_lineb_resolves_the_selected_potential():
    ini = "[Main]\njob = lineb\n[Potential]\npotential = morse_pt\n[Lineb]\nenergy = -0.55\n"
    resolved = resolve_ini("eonLegacyIni", ini)
    assert "potential.arm=morse " in resolved
    assert "lineb.energyEv=-0.55 " in resolved
