# Vire

## What is Vire?
Vire is a simple Vim / Neovim installer and vimrc + plugin or package manager.

Vire is able to install Vim or Neovim on Windows, leaving installation on Linux
to the distro package managers. Unlike other plugin managers, it also provides
a strategy to maintain and maintain a central vimrc, making it simple to keep
multiple machines in sync.

Vire also does not depend on the presence of Git which, though typically will
be available on most machines, might be one too many a requirement simply to
get your environment up and running.

Vire only requires Python which is what most modern Vim / Neovim plugins require
and made most sense to build upon.

## Installation

First download and install a Python distribution if not already present.

Vire can be obtained in multiple ways:

Eventually, Vire will be posted on PyPi enabling a simple:
  `pip install vire`

Or as a regular user:
  `pip install vire --user`

Until then, one of the following methods can be used:

- Clone the latest source:
  `git clone https://github.com/genotrance/vire`

- Download the latest source ZIP:
  `https://github.com/genotrance/vire/archive/master.zip`

Vire along with all dependencies can be installed to the standard Python location using: 
  `python setup.py install`

As a regular user, `python setup.py install --user` should work but it will
require adding `%APPDATA%\Roaming\Python\PythonVER\Scripts` or `~/.local/bin`
to the path.

Vire can also be used without installation with `python vire.py` but will require
all dependencies to be installed manually.
  `pip install pygithub`

After installation, Vire can be run on the command line like an executable.
  `vire -h`

## Configuration

Coming soon.

## Usage

```
usage: vire [-h] [-b] [-f] [-i] [-n] [-v] [vimrc]

positional arguments:
  vimrc          Gist ID or path to vimrc file

optional arguments:
  -h, --help     show this help message and exit
  -b, --bit32    Force 32-bit install
  -f, --force    Force Vim reinstall
  -i, --install  Install Vim/Neovim
  -n, --neomode  Neovim mode
  -v, --vimmode  Vim mode [default]
```

## Examples

## Dependencies

Vire only requires Python and the PyGithub module at this time. Setuptools is
also required if using `setup.py`.

Vire is tested on Windows with Python 3.6 using the Miniconda distribution and
on Ubuntu Artful with Python 2.7 and 3.6.

## Feedback

Vire is definitely a work in progress and any feedback or suggestions are welcome. 
It is hosted on [GitHub](https://github.com/genotrance/vire) with an MIT license
so issues, forks and PRs are most appreciated.
