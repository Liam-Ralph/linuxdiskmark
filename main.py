# Copyright (C) 2026 Liam Ralph
# https://github.com/liam-ralph

# This program, including this file, is licensed under the
# MIT (Expat) License.
# See LICENSE or this project's source for more information.
# Project source: https://github.com/liam-ralph/linuxdiskmark

# LinuxDiskMark, a disk benchmarking tool using fio.

# To convert this script into a standalone Python program, change
# the paths under Paths, and remove the section "Getting Root
# Privileges" (up to "Info and Settings Reading")


# Imports

# Tkinter

import tkinter
import tkinter.filedialog
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import ttk

# System

import os
import setproctitle
import subprocess
import sys


# Paths

global PATH_DATA
global PATH_LOGO
global PATH_DOC

PATH_DATA = "/usr/share/linuxdiskmark/data"
PATH_LOGO = "/usr/share/linuxdiskmark/logo.png"
PATH_DOC = "/usr/share/doc/linuxdiskmark"


# Functions

def open_window_home(window_dimensions = [800, 600], settings_dimensions = None):
    """
    Open home/main window. Non-default settings are used when the windows are
    reloaded after a settings change.

    :param window_dimensions: The dimensions to open the home window at.
    Defaults to 800 by 600.
    :param settings_dimensions: The dimensions to open the settings window at.
    Defaults to None, in which case the settings window will not be opened.
    """


# Main Function

def main():
    """
    Main Function. Run startup and open home window.
    """

    # Info and Settings Variables

    global names
    global created
    global version
    global updated

    global background
    global foreground
    global text_color
    global bg_image
    global font

    # Exit Flag

    global exit_flag

    # Getting Root Privileges

    if os.geteuid() != 0:

        # Get Display and XAuthority

        env = os.environ.copy()
        display = env.get("DISPLAY", ":0") # Default to :0 if missing
        xauthority = env.get("XAUTHORITY", "/tmp/xauth_XIOaut")

        # Relaunch with Pkexec

        command = [
            "pkexec",
            "env",
            f"DISPLAY={display}",
            f"XAUTHORITY={xauthority}",
            sys.executable
        ] + sys.argv
        os.execvp("pkexec", command)

    # Info and Settings Reading

    with open(PATH_DATA + "/info.txt", "r") as file:
        info_raw = file.read().split("\n")
    names = info_raw[0].replace("Names: ", "")
    created = info_raw[1].replace("Created: ", "")
    version = info_raw[2].replace("Version: ", "")
    updated = info_raw[3].replace("Updated: ", "")

    with open(PATH_DATA + "/settings.txt", "r") as file:
        settings_raw = file.read().split("\n")
    background = settings_raw[0].replace("background: ", "")
    foreground = settings_raw[1].replace("foreground: ", "")
    text_color = settings_raw[2].replace("text-color: ", "")
    bg_image = settings_raw[3].replace("bg_image: ", "")
    font = settings_raw[4].replace("font: ", "")

    # Process Title

    setproctitle.setproctitle("linuxdiskmark")

    # Home Window

    open_window_home()

# Run Main Function

if __name__ == "__main__":
    main()