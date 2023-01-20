from pathlib import Path

from setuptools import find_packages, setup

NAME = "canvasdl"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.readlines()
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    url="https://github.com/quintenroets/canvasdl",
    download_url=(
        "https://github.com/quintenroets/canvasdl/archive/refs/tags/v1.3.0.tar.gz"
    ),
    description="course content synchronizer",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    name=NAME,
    version="1.3",
    packages=find_packages(),
    setup_requires=read("setup_requirements.txt"),
    install_requires=read("requirements.txt"),
    package_data={"canvasdl": ["assets/**"]},
    entry_points={
        "console_scripts": [
            "canvasdl = canvasdl:main",
            "canvasdlcheck = canvasdl.core.checkservice:main",
        ]
    },
)
