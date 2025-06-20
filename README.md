# Marketplace Requirements Management tool

A Python script to clone the [Akamai Compute Marketplace apps repository](https://github.com/akamai-compute-marketplace/marketplace-apps), find all `requirements.txt` files for each app, and check or generate pinned Python package versions based on the latest available on [PyPI](https://pypi.org).

---

## Features

- Clone a fresh copy of the marketplace-apps repo.
- Recursively find all `requirements.txt` files.
- Compare currently pinned package versions to the latest available versions on PyPI.
- Generate updated pinned requirements files with the latest package versions.
- Filter by one or multiple apps.
- Quiet cloning with no git output.
- Outputs results in a clean, tabulated format.
- Supports both long and short command line flags.

---

## Requirements

- Python 3.7+
- `requests` Python package
- `tabulate` Python package
- Git installed and available in your system `PATH`

---

## Installation

1. Clone this repository or download the script file `check_marketplace_requirements.py`.

2. Install the required Python packages:

## Usage


```
python3 check_marketplace_requirements.py -h
usage: check_marketplace_requirements.py [-h] [-a APP] [-g]

📦 Check or generate pinned Python package versions for Marketplace app requirements.

options:
  -h, --help         show this help message and exit
  -a APP, --app APP  Filter by app directory name(s). Can specify multiple times or comma-separated list.
  -g, --gen          Generate new pinned requirements with latest versions

Examples:

  Show all current vs. latest package versions across all apps:
    python check_marketplace_requirements.py

  Show version info for specific apps:
    python check_marketplace_requirements.py -a linode-marketplace-postgresql linode-marketplace-wordpress

  Or comma-separated:
    python check_marketplace_requirements.py -a linode-marketplace-postgresql,linode-marketplace-wordpress

  Generate updated pinned versions for all apps:
    python check_marketplace_requirements.py -g

  Generate updated pinned versions for specific apps:
    python check_marketplace_requirements.py -a linode-marketplace-postgresql -a linode-marketplace-wordpress -g
```
