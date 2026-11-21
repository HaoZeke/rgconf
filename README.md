# rgconf

`rgconf` is the parameter-resolution and provenance library for the
OmniPotentRPC stack. It turns layered Cap'n Proto configuration defaults,
files, environment variables, command-line options, and runtime edits into one
validated configuration. Every resolved value retains its origin, and
configuration snapshots can be recorded in an RFC 9162 transparency log.

The project provides a Rust library, the `rgconf` command-line program, a C
ABI, and Python bindings.

## Install

The v0.1.0 release is available as source. From a shell with Git and
Rust, check out the release and install the command-line program.

```console
git clone --branch v0.1.0 https://github.com/OmniPotentRPC/rgconf.git
cd rgconf
cargo install --locked --path crates/rgconf-cli
```

To use the Rust library, run this command in the consuming Cargo project.

```console
cargo add rgconf --git https://github.com/OmniPotentRPC/rgconf.git --tag v0.1.0
```

For the Python bindings, activate a virtual environment and install the
package from the release checkout.

```console
python -m pip install ./python
```

## Quick start

Create `job.ini`:

```ini
[Optimizer]
converged_force = 0.03
```

Resolve it using the legacy EON profile:

```console
rgconf resolve --profile eonLegacyIni --ini job.ini
```

The equivalent Python call is:

```python
from rgconf import resolve_ini

resolved = resolve_ini(
    "eonLegacyIni",
    """[Optimizer]
converged_force = 0.03
""",
    "job.ini",
)
print(resolved)
```

## Documentation

The [user guide](https://omnipotentrpc.github.io/rgconf/) covers resolution,
schema extension, deprecation, parameters, precedence, and upstream
compatibility. Generate the Rust API documentation from the checkout with
`cargo doc --locked -p rgconf --open`. See the
[changelog](https://github.com/OmniPotentRPC/rgconf/blob/main/CHANGELOG.md) for
release notes.

The public C interface is declared in [`include/rgconf.h`](include/rgconf.h).

## License

MIT. See [LICENSE](LICENSE).
