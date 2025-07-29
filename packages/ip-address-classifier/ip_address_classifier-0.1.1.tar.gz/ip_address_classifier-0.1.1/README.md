# ip-address-classifier

[![PyPI version](https://badge.fury.io/py/ip-address-classifier.svg)](https://pypi.org/project/ip-address-classifier/)

A Python CLI tool that classifies IPv4 addresses by class (A–E), and also tells you if the address is:

- Public or Private  
- Loopback  
- Invalid

---

## Installation

```bash
pipx install ip-address-classifier
```

> ⚠️ If `ipclass` isn’t recognized after install, run:

```bash
pipx ensurepath
exec $SHELL  # or restart your terminal
```

---

## Usage

```bash
ipclass
```

You’ll be prompted to enter a valid IPv4 address (e.g. `192.168.1.1`)  
The tool will return:

- The address class (A–E)
- Whether it’s public or private
- If it’s loopback or invalid

---

## Tech Stack

- Python 3.12
- Poetry
- CLI entrypoint via `pyproject.toml`

---

## License

MIT — see [LICENSE](./LICENSE)
