# Vire

## What is Vire?
Vire is a simple Vim / Neovim installer and vimrc + plugin or package manager.

Vire makes it simple to install and keep Vim or Neovim up to date on Windows.

Install Vim:

  `vire -i`

Install Neovim:

  `vire -i -n`

This will download and install the binary from Github and extract to the HOME
directory. The directory will also be added to the user path so that starting
`[g]vim.exe` or `nvim[-qt].exe` is easy. It will install either the 32-bit or
64-bit version depending on the architecture of Python since a mismatch will
prevent Python plugins from working.

Installation on Linux is left to the distro package managers.

Vire also makes it super easy to install your `vimrc`. The recommended method is
to maintain the `vimrc` as a gist on Github. [Here's](https://gist.github.com/genotrance/57d327501443f440f522e2c886dadc1b) my vimrc for example.
All Vire needs is the gist ID and it is able to keep the local copy up to date.
All updates can be made on Github and simply running Vire on each machine will
get everything up to date. This strategy makes it simple to keep multiple
machines in sync.

  `vire gistID`

Lastly, Vire does what every other plugin manager does - install every plugin
defined in the vimrc loaded. One advantage of using Vire is that it does not
depend on Git to download plugins and leverages Vim / Neovim's built-in `pack`
method of loading plugins.

Vire only requires Python which is what most modern Vim / Neovim plugins require
and made the most sense to build upon.

## Installation

First download and install a Python distribution if not already present.

Vire can be installed in multiple ways, easiest being from PyPI:

  `pip install vire`

Or as a regular user:

  `pip install vire --user`

If `pip` isn't available or preferred, one of the following methods can be used
to download:

- Clone the latest source:

  `git clone https://github.com/genotrance/vire`

- Download the latest source ZIP:

  `https://github.com/genotrance/vire/archive/master.zip`

Vire along with all dependencies can then be installed to the standard Python
location using:

  `python setup.py install`

Or as a regular user:

  `python setup.py install --user`

Installing Vire as a regular user will require adding `%APPDATA%\Roaming\Python\PythonVER\Scripts`
or `~/.local/bin` to the path.

Vire can also be used without installation with `python vire.py` but will require
all dependencies to be installed manually.

  `pip install pygithub` for Python 3.x

  `pip install pygithub futures pathlib2` for Python 2.x

After installation, Vire can be run on the command line like an executable.

  `vire -h`

## Typical Scenario

- Download and install Vire

- Install Vim / Neovim if required

  `vire -i [-n]`

- Post vimrc to Github gist if not already

- If you want to use Vire for all plugins:
  - Edit vimrc to remove all function calls related to plugin managers like Pathogen,
    Vundle, vim-plug, etc.
  - Comment out all lines pointing to plugins. This will be used by Vire to download
    and install instead. For example, for Vundle:

    `Plugin 'tpope/vim-fugitive'` => `" Plugin 'tpope/vim-fugitive'`

  - Or for vim-plug:

    `Plug 'tpope/vim-fugitive'` => `" Plug 'tpope/vim-fugitive'`

  - For other plugins, you  will need to add such `" Plug 'user/project'` manually
    for each plugin that needs to be installed.

- If you prefer to use your existing plugin manager to download your plugins,
  you can use Vire to only install the plugin manager and leave the rest of the
  vimrc as is:

  `" Plug 'VundleVim/Vundle.vim'`
  `" Plug 'junegunn/vim-plug'`
  `" Plug 'Shougo/dein.vim'`

- Run Vire to download and install the vimrc and plugins:

  `vire gistID`

- When you need to update, simply run `vire` and it will check if anything has
  changed. Running with `-i` will also check if the app itself has an update.

## Configuration

Vire maintains a `~/.vire.json` to remember things such as the gist ID, 32-bit
mode, Vim or Neovim mode and other details to detect when an update is available.

No manual editing should be required, the command line parameters should be all
that's required.

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

## Dependencies

Vire only requires Python and the PyGithub module at this time. Setuptools is
also required if using `setup.py`.

Vire is tested on Windows with Python 3.6 using the Miniconda distribution and
on Ubuntu Artful with Python 2.7 and 3.6.

## Feedback

Vire is definitely a work in progress and any feedback or suggestions are welcome.
It is hosted on [GitHub](https://github.com/genotrance/vire) with an MIT license
so issues, forks and PRs are most appreciated.
