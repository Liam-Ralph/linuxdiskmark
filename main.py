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

from PIL import Image, ImageTk

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

def check_exit_flag():
    """
    Check whether the exit flag is active. If the exit flag is active, the
    program will exit (user closed home window). If the exit flag is inactive,
    the windows are being reloaded (e.g. after settings change) and the program
    does not exit.
    """

    global exit_flag

    if exit_flag:
        sys.exit()

def open_window_home():
    """
    Open home/main window.
    """

    # Home Window Variable

    global window_home

    # Info and Settings Variables

    global names
    global created
    global version
    global updated

    global background
    global foreground
    global highlight
    global bg_image
    global font

    # Global Buttons

    global button_all
    global button_1
    global button_2
    global button_3
    global button_4

    # Graphs

    global graph_r1
    global graph_r2
    global graph_r3
    global graph_r4

    global graph_w1
    global graph_w2
    global graph_w3
    global graph_w4

    # Exit Flag

    global exit_flag

    exit_flag = True

    # Window Setup

    window_width = 480
    window_height = 320

    window_home = tkinter.Tk()
    window_home.geometry(f"{window_width}x{window_height}")
    window_home.resizable(width = False, height = False)
    window_home.configure(bg = background)
    window_home.title("LinuxDiskMark " + version)
    window_home.protocol("WM_DELETE_WINDOW", check_exit_flag)
    window_home.iconphoto(
        True,
        ImageTk.PhotoImage(Image.open(PATH_LOGO))
    )
    window_home.update()

    # Home Screen

    frame_header = tkinter.Frame(
        window_home,
        width = window_width,
        height = 25,
        bg = background
    )
    frame_header.pack_propagate(False)
    frame_header.pack()

    frame_main = tkinter.Frame(
        window_home,
        width = window_width,
        height = window_height - 60,
        bg = background
    )
    frame_main.pack_propagate(False)
    frame_main.pack()

    frame_footer = tkinter.Frame(
        window_home,
        width = window_width,
        height = 35,
        bg = background
    )
    frame_footer.pack_propagate(False)
    frame_footer.pack()

    window_home.update()

    # Header Frame

    file_var = tkinter.StringVar(value = "File")
    file_options = ["Copy", "Save Text", "Save Image", "Exit"]
    tkinter.OptionMenu(
        frame_header,
        file_var,
        *file_options,
        command = lambda event: run_header_command(file_var.get())
    ).pack(
        side = tkinter.LEFT
    )

    # Footer Frame

    tkinter.Text(
        frame_footer,
        height = 1,
        font = (font, 10),
        bg = background,
        fg = foreground
    ).pack(
        padx = 5,
        pady = 5
    )

    window_home.update()

    # Window Mainloop

    window_home.mainloop()

def run_header_command(command):

    match command:

        case "Copy":

            clipboard_tk = tkinter.Tk()
            clipboard_tk.withdraw()
            clipboard_tk.clipboard_clear()
            clipboard_tk.clipboard_append("Temp")
            clipboard_tk.update()
            clipboard_tk.destroy()


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
    global highlight
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
    highlight = settings_raw[2].replace("highlight: ", "")
    bg_image = settings_raw[3].replace("bg_image: ", "")
    font = settings_raw[4].replace("font: ", "")

    # Process Title

    setproctitle.setproctitle("linuxdiskmark")

    # Home Window

    open_window_home()

# Run Main Function

if __name__ == "__main__":
    main()