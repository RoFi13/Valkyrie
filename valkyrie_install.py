"""Installer for downloading all Valkyrie Pipeline requirements."""

import argparse
from enum import Enum
import logging
import os
from pathlib import Path, PurePath
import shutil
import subprocess
import re
import sys

LOG = logging.getLogger(os.path.basename(__file__))
CURRENT_DIRECTORY = PurePath(__file__).parent


class BuildMode(Enum):
    """The style of execution to run."""

    DEV = 0
    DEPLOY = 1


def process_line(line, mode: BuildMode = BuildMode.DEPLOY) -> None:
    """Process each requirements line and clone only github Valkyrie packages."""
    line = line.strip()
    sys.stdout.write(f"Processing line: {line}...\n")

    # Check if the line matches the pattern for a Git repository
    match_found = re.search(
        r"git\+https://RoFi@github\.com/RoFi13/[\w-]+@v[\d]+\.[\d]+\.[\d]+", line
    )
    sitepackages_directory = PurePath(CURRENT_DIRECTORY, "sitepackages").as_posix()
    if not os.path.exists(sitepackages_directory):
        os.mkdir(sitepackages_directory)

    if not match_found:
        sys.stdout.write(
            "Line isn't a valid Valkyrie github URL. Treating package as a normal "
            "Python dependency. Downloading to sitepackages folder...\n"
        )
        # Install other packages listed in requirements.txt normally
        subprocess.run(["pip", "install", "--target=sitepackages", line], check=True)
        return

    sys.stdout.write("Requirement matches Valkyrie Repo Git pattern.\n")
    organization_name = line.split("/")[3]
    package_name = line.split("/")[4].split("@")[0]
    version_tag = line.split("@")[-1]
    package_url = f"https://RoFi@github.com/{organization_name}/{package_name}"

    sys.stdout.write(f"Package URL: {package_url}\n")
    sys.stdout.write(f"Package Name: {package_name}\n")
    sys.stdout.write(f"Version Tag: {version_tag}\n")

    # Check if package folder already exist. If it does, then delete and replace
    package_path = Path(Path(os.path.abspath(__file__)).parent, package_name)
    if os.path.exists(package_path):
        sys.stdout.write("Package directory already exists. Removing...\n")
        shutil.rmtree(package_path)

    # Clone the repository into a directory named after the package
    sys.stdout.write(f"Cloning {package_url} into {package_name}...\n")
    subprocess.run(
        [
            "git",
            "clone",
            "--depth=1",
            "--branch",
            version_tag,
            package_url,
            package_name,
        ],
        check=False,
    )

    # Remove .git directory
    if mode == BuildMode.DEPLOY:
        sys.stdout.write("IS FOR DEPLOYMENT!!")
        if os.path.exists(f"{package_path}\\.git"):
            sys.stdout.write(f"Found .git folder. Deleting... {package_path}\\.git\n")
            subprocess.run(
                ["rmdir", "/s", "/q", f"{package_path}\\.git"], shell=True, check=True
            )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Installer to help with automatically cloning remote git repos that "
            "the Valkyrie Pipeline requires."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=["dev", "deploy"],
        default="deploy",
        help=(
            "Mode to determine whether or not to keep the .git folders of the "
            "required repositories."
        ),
    )

    args = parser.parse_args(argv)

    selected_mode = BuildMode.DEPLOY
    if args.mode == "dev":
        selected_mode = BuildMode.DEV

    """Clone all Valkyrie pipeline required github packages."""
    sys.stdout.write("Downloading Valkyrie required Packages...\n")
    with open("requirements.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            process_line(line, selected_mode)

    sys.stdout.write("Packages installed.\n")


if __name__ == "__main__":
    main()
