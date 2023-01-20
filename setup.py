from setuptools import find_packages, setup

NAME = "canvasdl"


def read(filename):
    try:
        with open(filename) as fp:
            content = fp.read().split("\n")
    except FileNotFoundError:
        content = []
    return content


setup(
    author="Quinten Roets",
    author_email="quinten.roets@gmail.com",
    description="",
    name=NAME,
    version="1.1",
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
