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

# Other
import keyboard
import threading


# Paths

global PATH_DATA
global PATH_LOGO
global PATH_DOC

PATH_DATA = "/usr/share/linuxdiskmark/data"
PATH_LOGO = "/usr/share/linuxdiskmark/logo.png"
PATH_DOC = "/usr/share/doc/linuxdiskmark"


# Threading Functions

def listen_for_commands():

    global header_vars

    header_command_functions = [
        run_copy, run_save_text, run_save_image, run_exit,
    ]
    header_command_keybinds = [
        "ctrl+shift+c", "ctrl+t", "ctrl+s", "alt+f4"
    ]

    while True:
        for i in range(len(header_command_keybinds)):
            if keyboard.is_pressed(header_command_keybinds[i]):
                header_command_functions[i]()

# Header Command Functions

def run_copy():

    clipboard_tk = tkinter.Tk()
    clipboard_tk.withdraw()
    clipboard_tk.clipboard_clear()
    clipboard_tk.clipboard_append("Temp")
    clipboard_tk.update()
    clipboard_tk.destroy()

def run_save_text():

    pass

def run_save_image():

    pass

def run_exit():

    global exit_flag

    exit_flag = True
    window_home.destroy()

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

    # Header Variables

    global header_vars

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

    header_vars = [
        tkinter.StringVar(value = "File"), tkinter.StringVar(value = "Settings"),
        tkinter.StringVar(value = "Profile"), tkinter.StringVar(value = "Theme"),
        tkinter.StringVar(value = "Help"), tkinter.StringVar(value = "Language")
    ]

    file_options = ["Copy", "Save Text", "Save Image", "Exit"]
    tkinter.OptionMenu(
        frame_header,
        header_vars[0],
        *file_options,
        command = lambda event: run_header_command(0, file_options.index(header_vars[0].get()))
    ).pack(
        side = tkinter.LEFT
    )

    settings_options = []
    tkinter.OptionMenu(
        frame_header,
        header_vars[1],
        *settings_options,
        command = lambda event: run_header_command(1, settings_options.index(header_vars[1].get()))
    ).pack(
        side = tkinter.LEFT
    )

    profile_options = []
    tkinter.OptionMenu(
        frame_header,
        header_vars[2],
        *profile_options,
        command = lambda event: run_header_command(2, profile_options.index(header_vars[2].get()))
    ).pack(
        side = tkinter.LEFT
    )

    theme_options = []
    tkinter.OptionMenu(
        frame_header,
        header_vars[3],
        *theme_options,
        command = lambda event: run_header_command(3, theme_options.index(header_vars[3].get()))
    ).pack(
        side = tkinter.LEFT
    )

    help_options = []
    tkinter.OptionMenu(
        frame_header,
        header_vars[4],
        *help_options,
        command = lambda event: run_header_command(4, help_options.index(header_vars[4].get()))
    ).pack(
        side = tkinter.LEFT
    )

    language_options = []
    tkinter.OptionMenu(
        frame_header,
        header_vars[5],
        *language_options,
        command = lambda event: run_header_command(5, language_options.index(header_vars[5].get()))
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

    # Start Threading

    command_thread = threading.Thread(target = listen_for_commands)
    command_thread.daemon = True
    command_thread.start()

    # Window Mainloop

    window_home.mainloop()

def run_header_command(header_num, dropdown_num):
    """
    Reset the header variable to its default value, and run the command
    associated with the header and dropdown number.
    
    :param header_num: The header number. 0 = File, 1 = Settings, 2 = Profile,
    3 = Theme, 4 = Help, 5 = Language
    :param dropdown_num: The dropdown number. Used to run the command associated
    with the header and dropdown numbers. 
    """

    # Header Variable

    global header_vars

    headers = ["File", "Settings", "Profile", "Theme", "Help", "Language"]
    # dropdown_lists = [
    #     ["Copy", "Save Text", "Save Image", "Exit"],
    #     ["Test Data", "Default", "NVMe SSD", "Flash Memory", "Settings"],
    #     [
    #         "Default", "Peak Performance", "Real World Performance", "Demo",
    #         "Default [+Mix]", "Peak Performance [+Mix]", "Real World Performance [+Mix]"
    #     ],
    #     ["Read&Write [+Mix]", "Read [+Mix]", "Write [+Mix]"],
    #     [
    #         "Zoom", "Font Setting", "Random", "Dark", "DarkRed", "Default", "Digital8", "Flower",
    #         "Green", "LegendOfGreen", "LegendOfOrange"
    #     ],
    #     ["Select Language"]
    # ]
    header_vars[header_num].set(headers[dropdown_num])

    # Commands

    header_command_functions = [
        run_copy, run_save_text, run_save_image, run_exit,
    ]
    header_command_functions[header_num]()


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