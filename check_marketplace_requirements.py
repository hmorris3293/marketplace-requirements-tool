import os
import tempfile
import shutil
import subprocess
import requests
import re
from pathlib import Path
from tabulate import tabulate
import argparse

REPO_URL = "https://github.com/akamai-compute-marketplace/marketplace-apps.git"
REPO_NAME = "marketplace-apps"

def clone_repo(temp_dir):
    repo_path = os.path.join(temp_dir, REPO_NAME)
    subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, repo_path],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return repo_path

def find_requirements_files(repo_path, app_filters=None):
    all_reqs = list(Path(repo_path).rglob("requirements.txt"))
    if app_filters:
        # flatten comma separated values, strip spaces, lowercase
        filters = []
        for arg in app_filters:
            filters.extend([f.strip().lower() for f in arg.split(",") if f.strip()])
        filtered = [f for f in all_reqs if any(app_filter in str(f).lower() for app_filter in filters)]
        return filtered
    return all_reqs

def parse_requirements(file_path):
    packages = []
    with open(file_path) as f:
        for line in f:
            match = re.match(r"([a-zA-Z0-9_.-]+)==([^\s]+)", line.strip())
            if match:
                packages.append(match.groups())
    return packages

def get_latest_version(pkg_name):
    try:
        r = requests.get(f"https://pypi.org/pypi/{pkg_name}/json", timeout=5)
        r.raise_for_status()
        return r.json()["info"]["version"]
    except Exception:
        return "Error"

def main():
    parser = argparse.ArgumentParser(
        description="📦 Check or generate pinned Python package versions for Marketplace app requirements.",
        epilog="""
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
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "-a", "--app",
        action="append",
        help="Filter by app directory name(s). Can specify multiple times or comma-separated list."
    )
    parser.add_argument("-g", "--gen", action="store_true", help="Generate new pinned requirements with latest versions")

    args = parser.parse_args()

    temp_dir = tempfile.mkdtemp()
    try:
        repo_path = clone_repo(temp_dir)
        requirements_files = find_requirements_files(repo_path, app_filters=args.app)

        if not requirements_files:
            print("No requirements.txt found matching the specified app(s).")
            return

        requirements_files.sort()

        for req_file in requirements_files:
            app_relative_path = req_file.relative_to(repo_path).parent
            packages = parse_requirements(req_file)

            if args.gen:
                print(f"\n# {app_relative_path}/requirements.txt (latest pinned)")
                for name, _ in packages:
                    latest_version = get_latest_version(name)
                    print(f"{name}=={latest_version}")
            else:
                results = []
                for name, current_version in packages:
                    latest_version = get_latest_version(name)
                    results.append([
                        str(app_relative_path),
                        name,
                        current_version,
                        latest_version
                    ])
                print()  # Blank line before each table for readability
                print(tabulate(results, headers=["App Path", "Package", "Current", "Latest"]))
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
