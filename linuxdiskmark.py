# Copyright (C) 2026 Liam Ralph
# https://github.com/liam-ralph

# This program, including this file, is licensed under the
# MIT (Expat) License.
# See LICENSE or this project's source for more information.
# Project source: https://github.com/liam-ralph/linuxdiskmark

# LinuxDiskMark, a disk benchmarking tool using fio,
# inspired by CrystalDiskMark.

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
import platform
import setproctitle
import subprocess
import sys

# Other

import datetime
import keyboard
import threading


# Paths

global PATH_DATA
global PATH_LOGO
global PATH_DOC

PATH_DATA = "/usr/share/linuxdiskmark/data"
PATH_LOGO = "/usr/share/linuxdiskmark/logo.png"
PATH_DOC = "/usr/share/doc/linuxdiskmark"


# Home Window Functions

def open_window_home(open_settings = False):
    """
    Open home/main window.
    """

    # Home Window Variable

    global window_home

    # Info Variables

    global names
    global created
    global version
    global updated

    # Settings Variables

    global test_count
    global test_size
    global test_path

    global profile
    global mix

    global background
    global foreground
    global highlight
    global bg_image
    global font

    # Result Variables

    global results_read
    global results_write
    global results_mixed

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

    if mix:
        window_width = 660
    else:
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
        command = lambda event: run_file_command(file_var)
    ).pack(
        side = tkinter.LEFT
    )

    tkinter.Button(
        frame_header,
        text = "Settings",
        font = (font, 10),
        width = 9,
        height = 1,
        fg = foreground,
        bg = background,
        command = open_window_settings
    ).pack(
        side = tkinter.LEFT
    )

    tkinter.Button(
        frame_header,
        text = "Info",
        font = (font, 10),
        width = 6,
        height = 1,
        fg = foreground,
        bg = background,
        command = open_window_info
    ).pack(
        side = tkinter.LEFT
    )

    # Main Frame

    frame_row_1 = tkinter.Frame(
        frame_main,
        width = window_width,
        height = 50,
        bg = background
    )
    frame_row_1.pack_propagate(False)
    frame_row_1.pack(
        padx = 5,
        pady = 1
    )

    frame_row_2 = tkinter.Frame(
        frame_main,
        width = window_width,
        height = 50,
        bg = background
    )
    frame_row_2.pack_propagate(False)
    frame_row_2.pack(
        padx = 5,
        pady = 1
    )

    frame_row_3 = tkinter.Frame(
        frame_main,
        width = window_width,
        height = 50,
        bg = background
    )
    frame_row_3.pack_propagate(False)
    frame_row_3.pack(
        padx = 5,
        pady = 1
    )

    frame_row_4 = tkinter.Frame(
        frame_main,
        width = window_width,
        height = 50,
        bg = background
    )
    frame_row_4.pack_propagate(False)
    frame_row_4.pack(
        padx = 5,
        pady = 1
    )

    frame_row_5 = tkinter.Frame(
        frame_main,
        width = window_width,
        height = 50,
        bg = background
    )
    frame_row_5.pack_propagate(False)
    frame_row_5.pack(
        padx = 5,
        pady = 1
    )

    # Main Frame - Row 1

    tkinter.Button(
        frame_row_1,
        text = "All",
        font = (font, 12),
        width = 5,
        height = 4,
        fg = foreground,
        bg = highlight,
        activebackground = shift_color(highlight, True),
        command = lambda: run_benchmark(0)
    ).pack(
        side = tkinter.LEFT
    )

    frame_row_1_1 = tkinter.Frame(
        frame_row_1,
        width = window_width - 60,
        height = 25,
        bg = background
    )
    frame_row_1_1.pack_propagate(False)
    frame_row_1_1.pack(
        side = tkinter.TOP,
        padx = 1
    )

    frame_row_1_2 = tkinter.Frame(
        frame_row_1,
        width = window_width - 60,
        height = 25,
        bg = background
    )
    frame_row_1_2.pack_propagate(False)
    frame_row_1_2.pack(
        side = tkinter.TOP,
        padx = 1
    )

    # Main Frame - Row 1-1

    test_count_var = tkinter.IntVar(value = test_count)
    test_count_options = list(range(1, 10))
    tkinter.OptionMenu(
        frame_row_1_1,
        test_count_var,
        *test_count_options,
        command = lambda event: change_setting("test_count", test_count_var.get())
    ).pack(
        side = tkinter.LEFT,
        padx = 1
    )

    test_size_var = tkinter.StringVar(value = test_size)
    test_size_options = [
        "16MiB", "32MiB", "64MiB", "128MiB", "256MiB", "512MiB",
        "1GiB", "2GiB", "4GiB", "8GiB", "16GiB", "32GiB", "64GiB"
    ]
    tkinter.OptionMenu(
        frame_row_1_1,
        test_size_var,
        *test_size_options,
        command = lambda event: change_setting("test_size", test_size_var.get())
    ).pack(
        side = tkinter.LEFT,
        padx = 1
    )

    # placeholder for test path

    unit_var = tkinter.StringVar(value = unit)
    unit_options = ["MB/s", "GB/s"]
    tkinter.OptionMenu(
        frame_row_1_1,
        unit_var,
        *unit_options,
        command = lambda event: change_setting("unit", unit_var.get())
    ).pack(
        side = tkinter.LEFT,
        padx = 1
    )

    # Main Frame - Row 1-2

    frame_row_1_2_col_1 = tkinter.Frame(
        frame_row_1_2,
        width = 180,
        height = 25,
        bg = background
    )
    frame_row_1_2_col_1.pack_propagate(False)
    frame_row_1_2_col_1.pack(
        side = tkinter.LEFT,
        padx = 1
    )

    tkinter.Label(
        frame_row_1_2_col_1,
        text = f"Read ({unit})",
        font = (font, 12),
        bg = background,
        fg = foreground
    ).pack()

    frame_row_1_2_col_2 = tkinter.Frame(
        frame_row_1_2,
        width = 180,
        height = 25,
        bg = background
    )
    frame_row_1_2_col_2.pack_propagate(False)
    frame_row_1_2_col_2.pack(
        side = tkinter.LEFT,
        padx = 1
    )

    tkinter.Label(
        frame_row_1_2_col_2,
        text = f"Write ({unit})",
        font = (font, 12),
        bg = background,
        fg = foreground
    ).pack()

    if mix:

        frame_row_1_2_col_3 = tkinter.Frame(
            frame_row_1_2,
            width = 180,
            height = 25,
            bg = background
        )
        frame_row_1_2_col_3.pack_propagate(False)
        frame_row_1_2_col_3.pack(
            side = tkinter.LEFT,
            padx = 1
        )

        tkinter.Label(
            frame_row_1_2_col_3,
            text = f"Mix ({unit})",
            font = (font, 12),
            bg = background,
            fg = foreground
        ).pack()

    # Main Frame - Row 2

    tkinter.Button(
        frame_row_2,
        text = "",
        font = (font, 12),
        width = 5,
        height = 4,
        fg = foreground,
        bg = highlight,
        activebackground = shift_color(highlight, True),
        command = lambda: run_benchmark(1)
    ).pack(
        side = tkinter.LEFT
    )

    # Main Frame - Row 3

    tkinter.Button(
        frame_row_3,
        text = "",
        font = (font, 12),
        width = 5,
        height = 4,
        fg = foreground,
        bg = highlight,
        activebackground = shift_color(highlight, True),
        command = lambda: run_benchmark(2)
    ).pack(
        side = tkinter.LEFT
    )

    # Main Frame - Row 4

    tkinter.Button(
        frame_row_4,
        text = "",
        font = (font, 12),
        width = 5,
        height = 4,
        fg = foreground,
        bg = highlight,
        activebackground = shift_color(highlight, True),
        command = lambda: run_benchmark(3)
    ).pack(
        side = tkinter.LEFT
    )

    # Main Frame - Row 5

    tkinter.Button(
        frame_row_5,
        text = "",
        font = (font, 12),
        width = 5,
        height = 4,
        fg = foreground,
        bg = highlight,
        activebackground = shift_color(highlight, True),
        command = lambda: run_benchmark(4)
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

    # Open Settings Window

    if open_settings:
        open_window_settings()

    # Window Mainloop

    window_home.mainloop()

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

def run_benchmark(benchmark_num):

    pass

# Info Window Functions

def open_window_info():

    pass

# Settings Window Functions

def open_window_settings():

    pass

# Settings Functions

def change_setting(setting, value):

    global test_count
    global test_size
    global test_data
    global test_path

    global profile
    global mix

    global background
    global foreground
    global highlight
    global bg_image
    global font

    global unit
    global language

    with open(PATH_DATA + "/settings.txt", "r+") as file:
        settings_raw = file.read()
        settings_raw = settings_raw.replace(
            f"{setting}: {globals()[setting]}", f"{setting}: {value}"
        )
        file.seek(0)
        file.write(settings_raw)

    globals()[setting] = value

# File Header Command Functions

def run_file_command(file_var):

    command_names = ["Copy", "Save Text", "Save Image", "Exit"]
    command_functions = [copy_text, save_text, save_image, exit_program]

    command_functions[command_names.index(file_var.get())]()
    file_var.set("File")

def listen_for_commands():

    keyboard.add_hotkey("ctrl+shift+c", copy_text)
    keyboard.add_hotkey("ctrl+t", save_text)
    keyboard.add_hotkey("ctrl+s", save_image)
    keyboard.add_hotkey("alt+f4", exit_program)

def copy_text():

    # Result Variables

    global results_read
    global results_write
    global results_mixed

    # Text Formatting

    text = (
        "-" * 78 + "\n" +
        "LinuxDiskMark " + version + " (C) 2026 Liam Ralph\n" +
        "https://liam-ralph.github.io/projects/linuxdiskmark\n" +
        "-" * 78 + "\n" +
        "* MB/s = 1,000,000 bytes/s [SATA/600 = 6000,000,000 bytes/s]\n" +
        "* KB = 1000 bytes, KiB = 1024 bytes\n\n"
    )

    if results_read is not None:
        text += (
            "[Read]\n" +
            "\n"
        )

    if results_write is not None:
        text += (
            "[Write]\n" +
            "\n"
        )

    if results_mixed is not None:
        text += (
            "[Mixed]\n" +
            "\n"
        )

    text += (
        "Profile: " + profile + "\n"
        "   Test: " + f"{test_size} (x{test_count}) [{test_path}]\n" +
        "   Date: " + datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S") + "\n"
    )

    with open("/etc/os-release") as file:
        file_line = file.readline()
        while ("PRETTY_NAME=\"" not in file_line):
            file_line = file.readline()
        text += (
            "     OS: " + file_line.replace("PRETTY_NAME=\"", "").replace("\"\n", "") +
            f" [Kernel: {platform.release()}]\n"
        )

    # Copying to Clipboard

    clipboard_tk = tkinter.Tk()
    clipboard_tk.withdraw()
    clipboard_tk.clipboard_clear()
    clipboard_tk.clipboard_append(text)
    clipboard_tk.update()
    clipboard_tk.destroy()

def save_text():

    pass

def save_image():

    pass

def exit_program():

    global exit_flag

    exit_flag = True
    window_home.destroy()

# Other Functions

def shift_color(color, lighten, amount = 30):

    color = color.lstrip("#")
    r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

    if r < amount and g < amount and b < amount:
        lighten = True
    elif r > 255 - amount and g > 255 - amount and b > 255 - amount:
        lighten = False

    if lighten:
        r = min(255, r + amount)
        g = min(255, g + amount)
        b = min(255, b + amount)
    else:
        r = max(0, r - amount)
        g = max(0, g - amount)
        b = max(0, b - amount)

    return f"#{r:02x}{g:02x}{b:02x}"


# Main Function

def main():
    """
    Main Function. Run startup and open home window.
    """

    # Info Variables

    global names
    global created
    global version
    global updated

    # Settings Variables

    global test_count
    global test_size
    global test_data
    global test_path

    global profile
    global mix

    global background
    global foreground
    global highlight
    global bg_image
    global font

    global unit
    global language

    # Result Variables

    global results_read
    global results_write
    global results_mixed

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

    test_count = int(settings_raw[1].replace("test_count: ", ""))
    test_size = settings_raw[2].replace("test_size: ", "")
    test_data = settings_raw[3].replace("test_data: ", "")
    test_path = settings_raw[4].replace("test_path: ", "")

    profile = settings_raw[7].replace("profile: ", "")
    mix = (settings_raw[8].replace("mix: ", "") == "True")

    background = settings_raw[11].replace("background: ", "")
    foreground = settings_raw[12].replace("foreground: ", "")
    highlight = settings_raw[13].replace("highlight: ", "")
    bg_image = settings_raw[14].replace("bg_image: ", "")
    font = settings_raw[15].replace("font: ", "")

    unit = settings_raw[18].replace("unit: ", "")
    language = settings_raw[19].replace("language: ", "")

    # Results

    results_read = [0, 0, 0, 0]
    results_write = [0, 0, 0, 0]

    if mix:
        results_mixed = [0, 0, 0, 0]
    else:
        results_mixed = None

    # Process Title

    setproctitle.setproctitle("linuxdiskmark")

    # Home Window

    open_window_home()

# Run Main Function

if __name__ == "__main__":
    main()