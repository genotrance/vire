"Vim / Neovim installer and vimrc + plugin manager"

from __future__ import print_function

import argparse
import ctypes
import datetime
import glob
import io
import json
import os
import platform
import re
import requests
import shutil
import sys
import tempfile
import time
import traceback
import zipfile

try:
    import github
except ImportError:
    print("Requires module pygithub")
    sys.exit()

try:
    import pathlib
except ImportError:
    try:
        import pathlib2 as pathlib
    except ImportErrror:
        print("Requires module pathlib2")
        sys.exit()

if os.name == "nt":
    try:
        import winreg
    except ImportError:
        try:
            import _winreg as winreg
        except ImportError:
            print("Requires module winreg")
            sys.exit()

    try:
        import ctypes.wintypes
    except ImportError:
        print("Requires module ctypes.wintypes")
        sys.exit()

__version__ = "0.2.0"

class State(object):
    config = ""
    force = False
    home = os.getenv("HOME") or ""
    install = False
    packpath = ""
    nvimpath = ".local/share/nvim"
    nvimrcpath = ".config/nvim/init.vim"
    vimpath = ".vim"
    vimrcpath = ".vimrc"
    windows = False

    github = None

Config = {
    "bit64": False,
    "neomode": False,
    "neoversion": "",
    "plugins": {},
    "vimrc": "",
    "vimrcupdated": "",
    "vimversion": ""
}

CConfig = {}
Plugins = []

def parsecli():
    parser = argparse.ArgumentParser()
    parser.add_argument("vimrc", nargs="?", help="Gist ID or path to vimrc file")
    parser.add_argument("-b", "--bit32", action="store_true", help="Force 32-bit install")
    parser.add_argument("-f", "--force", action="store_true", help="Force Vim reinstall")
    parser.add_argument("-i", "--install", action="store_true", help="Install Vim/Neovim")
    parser.add_argument("-n", "--neomode", action="store_true", help="Neovim mode")
    parser.add_argument("-v", "--vimmode", action="store_true", help="Vim mode [default]")

    args = parser.parse_args()
    if Config["bit64"] == True and args.bit32 == True:
        Config["bit64"] = False
    State.force = args.force
    State.install = args.install

    if args.vimrc:
        Config["vimrc"] = args.vimrc

    if args.neomode and args.vimmode:
        print("You really want both Vim and Neovim?")
        sys.exit()

    if args.neomode:
        Config["neomode"] = True
    elif args.vimmode:
        Config["neomode"] = False

def within_rate_limit():
    rl = State.github.get_rate_limit()
    if not rl.rate.remaining:
        print("Github rate limit exceeded, wait until", str(rl.rate.reset), "GMT")
        return False

    return True

def setup():
    global Config
    global CConfig

    if os.name == "nt":
        State.windows = True
        State.home = os.getenv("USERPROFILE")
        State.nvimpath = "AppData/Local/nvim"
        State.nvimrcpath = "AppData/Local/nvim/init.vim"
        State.vimpath = "vimfiles"
        State.vimrcpath = "_vimrc"

    State.nvimpath = os.path.join(State.home, State.nvimpath)
    State.nvimrcpath = os.path.join(State.home, State.nvimrcpath)
    State.vimpath = os.path.join(State.home, State.vimpath)
    State.vimrcpath = os.path.join(State.home, State.vimrcpath)

    State.config = os.path.join(State.home, ".vire.json")

    #if "64" in platform.machine():
    if sys.maxsize != 2147483647:
        Config["bit64"] = True

    if os.path.exists(State.config):
        with open(State.config) as fp:
            CConfig = json.load(fp)
            Config.update(CConfig)

    parsecli()

    if Config["neomode"]:
        State.packpath = os.path.join(State.nvimpath, "site", "pack", "vire", "start")
    else:
        State.packpath = os.path.join(State.vimpath, "pack", "vire", "start")

    pathlib.Path(State.packpath).mkdir(parents=True, exist_ok=True)

    State.github = github.Github()

def extract(zfilename, destination):
    print("- Extracting " + os.path.basename(zfilename))
    with zipfile.ZipFile(zfilename) as zf:
        zf.extractall(destination)

def extract_asset(zfilename):
    if os.path.exists(os.path.join(State.home, "vim")):
        return

    extract(zfilename, State.home)

def download(url, filename):
    print("- Downloading " + url)
    with requests.get(url, stream=True) as resp, open(filename, 'wb') as fp:
        if resp.ok:
            shutil.copyfileobj(io.BytesIO(resp.content), fp)
        else:
            print("Failed download of " + url)
            return False

    return True

def download_asset(asset):
    zfilename = os.path.join(tempfile.gettempdir(), asset.name)
    if os.path.exists(zfilename) and os.stat(zfilename).st_size == asset.size:
        return zfilename

    if not download(asset.browser_download_url, zfilename):
        return ""

    return zfilename

def add_to_path():
    vimapppath = ""
    if not Config["neomode"]:
        for dr in glob.glob(os.path.join(State.home, "vim", "vim*")):
            for fn in glob.glob(os.path.join(dr, "*.exe")):
                if "vim.exe" in fn:
                    vimapppath = dr
                    break
    else:
        for fn in glob.glob(os.path.join(State.home, "Neovim", "bin", "*.exe")):
            if "nvim-qt.exe" in fn:
                vimapppath = os.path.dirname(fn)
                break

    if vimapppath:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
        gkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 0)
        value = ""
        gvalue = ""
        try:
            gvalue, _ = winreg.QueryValueEx(gkey, "PATH")
            value, _ = winreg.QueryValueEx(key, "PATH")
        except WindowsError:
            pass

        if vimapppath.lower() not in gvalue.lower() and vimapppath.lower() not in value.lower():
            value = value + os.pathsep + vimapppath if value else vimapppath
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, value)
            print("- Adding Vim to path: " + vimapppath)

            SendMessageTimeout = ctypes.windll.user32.SendMessageTimeoutW
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002

            try:
                SendMessageTimeout(HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
                    SMTO_ABORTIFHUNG, 5000)
            except ValueError:
                pass

        winreg.CloseKey(gkey)
        winreg.CloseKey(key)

def delete_vim():
    apppath = "vim"
    if Config["neomode"]:
        apppath = "Neovim"
    apppath = os.path.join(State.home, apppath)

    print("- Deleting", apppath)
    if os.path.exists(apppath):
        shutil.rmtree(apppath)

def get_vim():
    if not State.install:
        return

    name = "Vim"
    repo = "vim/vim-win32-installer"
    version = "vimversion"
    if Config["neomode"]:
        name = "Neovim"
        repo = "neovim/neovim"
        version = "neoversion"

    if not State.windows:
        print("Use package manager to install", name)
        return

    latest = State.github.get_repo(repo).get_latest_release()
    if State.force or latest.tag_name > Config[version] or Config["bit64"] != CConfig["bit64"]:
        print("Updating", name+":", Config[version] + " => " + latest.tag_name)
        for asset in latest.get_assets():
            if "zip" in asset.name and "pdb" not in asset.name:
                if (Config["bit64"] and "64" in asset.name) or (not Config["bit64"] and ("x86" in asset.name or "32" in asset.name)):
                    delete_vim()
                    zfilename = download_asset(asset)
                    if zfilename:
                        extract(zfilename, State.home)
                        add_to_path()
                        Config[version] = latest.tag_name
    else:
        print(name, "up to date:", Config[version])

def get_gist(vimrcpath):
    gist = State.github.get_gist(Config["vimrc"])
    if State.force or "vimrcupdated" not in Config or str(gist.updated_at) > Config["vimrcupdated"]:
        for (gfname, gfile) in gist.files.items():
            if "vimrc" in gfname:
                print("Updating", vimrcpath, "with", gfname)
                with open(vimrcpath, "w") as fp:
                    shutil.copyfileobj(io.StringIO(gfile.content), fp)
                Config["vimrcupdated"] = str(gist.updated_at)
                break
    else:
        print(vimrcpath, "up to date")

def get_submodules(pluginpath):
    submodules = os.path.join(pluginpath, ".gitmodules")
    if os.path.exists(submodules):
        path = ""
        url = ""
        for line in open(submodules).read().splitlines():
            line = line.strip().split("=")
            if line[0].strip() == "path":
                path = line[1].strip()
            elif line[0].strip() == "url":
                url = line[1].strip().replace("https://github.com/", "")
            elif "[" in line:
                path = ""
                url = ""

            if path != "" and url != "":
                get_plugin(url, os.path.join(pluginpath, path))

def get_plugin(reponame, location=None):
    global Plugins

    if os.path.splitext(reponame)[1] == ".git":
        reponame = reponame[:-4]
    reponame = reponame.replace("\\", "/")

    plugin = os.path.basename(reponame)

    if location == None:
        pluginpath = os.path.join(State.packpath, plugin)
    else:
        pluginpath = location

    if plugin in Plugins:
        return

    Plugins.append(plugin)

    if not plugin in Config["plugins"] or not os.path.exists(pluginpath) or glob.glob(pluginpath + "/*") == []:
        Config["plugins"][plugin] = {
            "last_checked": time.time(),
            "sha": ""
        }
    elif not State.force and Config["plugins"][plugin]["last_checked"] + 3600 > time.time():
        get_submodules(pluginpath)
        return

    repo = State.github.get_repo(reponame)
    commits = repo.get_commits()
    latest = commits[0].sha

    Config["plugins"][plugin]["last_checked"] = time.time()
    Config["plugins"][plugin]["location"] = pluginpath

    if latest != Config["plugins"][plugin]["sha"]:
        if os.path.exists(pluginpath):
            print("Updating plugin", reponame)
            shutil.rmtree(pluginpath)
        else:
            print("Loading plugin", reponame)
        zplugin = os.path.join(tempfile.gettempdir(), plugin + "-" + latest + ".zip")
        if not os.path.exists(zplugin):
            if not download("https://github.com/" + reponame + "/archive/" + latest + ".zip", zplugin):
                return
        zextract = os.path.join(tempfile.gettempdir(), plugin)
        extract(zplugin, zextract)
        renamed = ""
        for pdir in glob.glob(zextract + "/*"):
            renamed = pdir
        if renamed != "":
            files = glob.glob(renamed + "/*") or []
            dotfiles = glob.glob(renamed + "/.*") or []
            files.extend(dotfiles)
            os.mkdir(pluginpath)
            for pfs in files:
                os.rename(pfs, pfs.replace(renamed, pluginpath))
            try:
                os.remove(renamed)
                os.remove(zextract)
            except:
                pass

        Config["plugins"][plugin]["sha"] = latest

        get_submodules(pluginpath)

def get_vimrc():
    if Config["vimrc"] == "":
        print("No vimrc specified")
        return

    dest = State.nvimrcpath if Config["neomode"] else State.vimrcpath
    if Config["vimrcupdated"] == "" and os.path.exists(dest) and not State.force:
        print("vimrc already exists - run with -f to overwrite")
        return

    pathlib.Path(os.path.dirname(dest)).mkdir(parents=True, exist_ok=True)
    if os.path.exists(Config["vimrc"]):
        print("Copying", Config["vimrc"], "to", dest)
        shutil.copyfile(Config["vimrc"], dest)
    else:
        get_gist(dest)

    if os.path.exists(dest):
        with open(dest) as fp:
            for line in fp.readlines():
                match = re.match("\"[ ]+Plug(?:in)?[ ]+'(.*?)'", line)
                if match:
                    get_plugin(match.group(1))

    # Cleanup
    for pdir in glob.glob(os.path.join(State.packpath, "*")):
        if os.path.basename(pdir) not in Plugins:
            print("Removing", pdir)
            shutil.rmtree(pdir)

    if "plugins" in Config:
        for plugin in list(Config["plugins"]):
            if not "location" in Config["plugins"][plugin] or not os.path.exists(Config["plugins"][plugin]["location"]):
                del Config["plugins"][plugin]

def save():
    with open(State.config, "w") as fp:
        json.dump(Config, fp)

def main():
    try:
        setup()
        get_vim()
        get_vimrc()
    except github.GithubException as e:
        if e.status == 403:
            within_rate_limit()
        elif e.status == 404:
            print("Gist ID not found")
        else:
            print(e)
    except SystemExit:
        pass
    except:
        traceback.print_exc(file=sys.stdout)

    save()

if __name__ == "__main__":
    main()
