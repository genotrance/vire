from setuptools import setup

import os.path

version = ""
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "vire.py")) as f:
    for line in f.readlines():
        if "__version__" in line:
            version = line.strip().replace('"', '').split()[-1]
            break

long_description = ""
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read().split("\n\n")[1].replace("\n", " ").split("? ")[1]

setup(
    name = "vire",
    version = version,
    description = "Vim / Neovim installer and plugin manager",
    long_description = long_description,
    url = "https://github.com/genotrance/vire",
    author = "Ganesh Viswanathan",
    author_email = "dev@genotrance.com",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Utilities"
    ],
    keywords = "vim vimrc neovim plugin",
    py_modules = ["vire"],
    install_requires = [
        "pygithub",
        'futures;python_version<"3.0"',
        'pathlib2;python_version<"3.0"'
    ],
    data_files = [
        ("lib/site-packages/vire", [
            "HISTORY.txt",
            "LICENSE.txt",
            "README.md"
        ])
    ],
    entry_points = {
        "console_scripts": [
            "vire=vire:main"
        ]
    },
    project_urls = {
        "Bug Reports": "https://github.com/genotrance/vire/issues",
        "Source": "https://github.com/genotrance/vire"
    }
)
