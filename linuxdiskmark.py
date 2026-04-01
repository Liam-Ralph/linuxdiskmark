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

from PIL import Image, ImageGrab, ImageTk

# System

import os
import platform
import pwd
import setproctitle
import subprocess
import sys

# Other

import datetime
import json
import keyboard
import threading


# Paths

PATH_DATA = "/usr/share/linuxdiskmark/data/"
PATH_LOGO = "/usr/share/linuxdiskmark/logo.png"
PATH_DOC = "/usr/share/doc/linuxdiskmark/"

sudo_user = os.environ.get("SUDO_USER")
if sudo_user:
    PATH_HOME = pwd.getpwnam(sudo_user).pw_dir + "/"
else:
    PATH_HOME = pwd.getpwuid(os.getuid()).pw_dir + "/"

# Other Constants

RW_NAMES = ["Read", "Write", "Mix"]


# Classes

class Test:
    def __init__(self, random, block_size, queues, threads, units):
        self.random = random
        self.random_str = "RND" if random else "SEQ"
        self.block_size = block_size
        self.queues = queues
        self.threads = threads
        self.units = units


# Home Window Functions

def open_window_home(open_window = None):
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

    global hardware
    global profile
    global mix

    global background
    global foreground
    global highlight
    global bg_image
    global font

    global profiles

    # Result Variables

    global results
    global result_labels

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

    # add new OptionMenus here

    # Main Frame

    # Main Frame Widget Functions

    def create_row(parent, half_size = False):
        frame = tkinter.Frame(
            parent,
            width = window_width,
            height = 50 if not half_size else 25,
            bg = background
        )
        frame.pack_propagate(False)
        frame.pack(
            padx = 5,
            pady = 1
        )
        return frame

    def create_test_button(parent, text, benchmark):
        button = tkinter.Button(
            parent,
            text = text,
            font = (font, 12),
            width = 5,
            height = 4,
            fg = foreground,
            bg = highlight,
            activebackground = shift_color(highlight, True),
            command = lambda: run_benchmark(benchmark)
        )
        button.pack(
            side = tkinter.LEFT
        )

    # Main Frame - Row 1

    frame_row_1 = create_row(frame_main)
    create_test_button(frame_row_1, "All", 4)

    # Main Frame - Row 1-1

    frame_row_1_1 = create_row(frame_row_1, True)

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

    partitions_raw = subprocess.run(
        "lsblk -o LABEL,MOUNTPOINT,FSUSE% -nr",
        shell = True,
        capture_output = True,
        text = True
    ).stdout.strip().split("\n")

    partition_names = []
    partition_paths = []

    for partition_raw in partitions_raw:
        partition = partition_raw.split(" ")
        if len(partition) == 3 and "/" in partition[1] and "/boot" not in partition[1]:
            name = partition[0].replace("\\x20", " ")
            used = int(partition[2][:-1])
            partition_names.append(f"{name}: {used}%")
            path = partition[1].replace("\\x20", " ")
            partition_paths.append(path)

    if test_path in partition_paths:
        init_val = partition_names[partition_paths.index(test_path)]
    else:
        init_val = test_path

    test_path_var = tkinter.StringVar(value = init_val)
    test_path_options = partition_names + ["Choose Folder"]

    def test_path_command(event):

        if test_path_var.get() in partition_names:

            partition_name = test_path_var.get()
            setting_value = partition_paths[partition_names.index(partition_name)]
            test_path_var.set(
                partition_name if len(partition_name) <= 23 else partition_name[:20] + "..."
            )

        else:

            setting_value = tkinter.filedialog.askdirectory(
                parent = window_home,
                initialdir = "/",
                mustexist = True
            )
            test_path_var.set(
                setting_value if len(setting_value) <= 23 else setting_value[-20:] + "..."
            )

        change_setting("test_path", setting_value)

    tkinter.OptionMenu(
        frame_row_1_1,
        test_path_var,
        *test_path_options,
        command = test_path_command
    ).pack(
        side = tkinter.LEFT,
        padx = 1
    )

    unit_var = tkinter.StringVar(value = unit)
    unit_options = ["MB/s", "GB/s", "IOPS", "μs"]
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

    frame_row_1_2 = create_row(frame_row_1, True)

    if profile != "demo":

        for col in range(3 if mix else 2):

            frame = tkinter.Frame(
                frame_row_1_2,
                width = 180,
                height = 25,
                bg = background
            )
            frame.pack_propagate(False)
            frame.pack(
                side = tkinter.LEFT,
                padx = 1
            )

            tkinter.Label(
                frame,
                text = f"{RW_NAMES[col]} ({unit})",
                font = (font, 12),
                bg = background,
                fg = foreground
            ).pack()

    else:

        demo_test = profiles[hardware][profile][0]

        tkinter.Label(
            frame_row_1_2,
            text = (
                f"{demo_test.random_str} {demo_test.block_size}, " +
                f"Q={demo_test.queues}, T={demo_test.threads}" # e.g. SEQ 1MiB, Q=8, T=1
            ),
            font = (font, 12),
            bg = background,
            fg = foreground
        ).pack()

    # Main Frame - Row 2+

    if profile != "demo":

        for row_num in [2, 3, 4, 5]:

            test_num = row_num - 2
            test = profiles[hardware][profile][test_num]

            frame_row = create_row(frame_main)
            text = (
                (test.random_str) + test.block_size.replace("iB", "") + "\n" +
                f"Q{test.queues}T{test.threads}"
            )
            create_test_button(frame_row, text, test_num)

            for col in range(3 if mix else 2):

                frame_col = tkinter.Frame(
                    frame_row,
                    width = 180,
                    height = 48,
                    bd = 1,
                    relief = tkinter.SOLID,
                    bg = background
                )
                frame_col.pack_propagate(False)
                frame_col.pack(
                    side = tkinter.LEFT,
                    padx = 1
                )

                result_label = tkinter.Label(
                    frame_col,
                    text = f"{round_pad(results[col][test_num][unit], 2)}",
                    font = (font, 28),
                    bg = background,
                    fg = foreground
                )
                result_label.pack(
                    side = tkinter.RIGHT
                )
                result_labels[col].append(result_label)

    else:

        # Main Frame - Row 2

        frame_row_2 = tkinter.Frame(
            frame_main,
            width = window_width,
            height = 200,
            bg = background
        )
        frame_row_2.pack_propagate(False)
        frame_row_2.pack(
            padx = 5,
            pady = 1
        )

        for col in range(2):

            frame_result = tkinter.Frame(
                frame_row_2,
                width = window_width / 2,
                height = 200,
                bd = 1,
                relief = tkinter.SOLID,
                bg = background
            )
            frame_result.pack_propagate(False)
            frame_result.pack(
                side = tkinter.LEFT,
                padx = 3
            )

            label_nw = tkinter.Label(
                frame_result,
                text = RW_NAMES[col],
                font = (font, 12),
                width = len(RW_NAMES[col]) + 2,
                height = 2,
                bg = background,
                fg = foreground
            )
            label_nw.place(
                relx = 0,
                rely = 0,
                anchor = tkinter.NW
            )

            label_result = tkinter.Label(
                frame_result,
                text = f"{round_pad(results[col][0][unit], 2)}",
                font = (font, 32),
                height = 4,
                bg = background,
                fg = foreground
            )
            label_result.pack(
                anchor = tkinter.CENTER
            )
            result_labels[col].append(label_result)

            label_se = tkinter.Label(
                frame_result,
                text = unit,
                font = (font, 12),
                width = len(unit) + 2,
                height = 2,
                bg = background,
                fg = foreground
            )
            label_se.place(
                relx = 1,
                rely = 1,
                anchor = tkinter.SE
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

    if open_window == "profile":
        open_window_profile_settings()
    elif open_window == "font":
        open_window_font_settings()

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

    # 0-3 are a num, 4 is all
    pass

# Info Functions

def open_web_info():

    pass

def open_window_info():

    pass

# Settings Window Functions

def open_window_profile_settings():

    pass

def open_window_font_settings():

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

    with open(PATH_DATA + "settings.json", "r+") as file:
        settings_raw = json.load(file)
        settings_raw[setting] = value
        file.seek(0)
        json.dump(settings_raw, file, indent = 4)
        file.truncate()

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

    keyboard.add_hotkey("ctrl+q", open_window_profile_settings)
    keyboard.add_hotkey("ctrl+f", open_window_font_settings)

    keyboard.add_hotkey("f1", open_web_info)

def get_result_text():

    # Result Variable

    global results

    # Header and Units

    text = (
        "-" * 78 + "\n" +
        "LinuxDiskMark " + version + " (C) 2026 Liam Ralph\n" +
        "https://liam-ralph.github.io/projects/linuxdiskmark\n" +
        "-" * 78 + "\n" +
        "* MB/s = 1,000,000 bytes/s [SATA/600 = 6000,000,000 bytes/s]\n" +
        "* KB = 1000 bytes, KiB = 1024 bytes\n\n"
    )

    # Results

    results_text = ["[Read]\n", "[Write]\n"]
    if mix:
        results_text.append("[Mix]\n")

    for test_num in range(4 if profile != "demo" else 1):

        test = profiles[hardware][profile][test_num]
        test_text = (
            f"  {test.random_str} {test.block_size.rjust(7)} " +
            f"(Q={str(test.queues).rjust(3)}, T={str(test.threads).rjust(2)}): "
        )

        for i in range(3 if mix else 2):

            test_results = results[i][test_num]
            results_text[i] += (
                test_text +
                f"{round_pad(test_results['MB/s'], 3).rjust(9)} MB/s " +
                f"[{round_pad(test_results['IOPS'], 1).rjust(9)} IOPS] " +
                f"<{round_pad(test_results['us'], 2).rjust(9)} us>\n"
            )

    for i in range(3 if mix else 2):
        text += results_text[i] + "\n"

    # Settings and User Info

    text += (
        f"Profile: {profile}\n" +
        f"   Test: {test_size} (x{test_count}) [{test_path}]\n" +
        f"   Time: Measure {profiles[hardware]["measure_time"]} sec / " +
        f"Interval {profiles[hardware]["interval_time"]} sec\n"
        f"   Date: {datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")}\n"
    )

    os = "Linux"
    with open("/etc/os-release") as file:
        file_line = file.readline()
        while ("PRETTY_NAME=\"" not in file_line):
            file_line = file.readline()
        os = file_line.replace("PRETTY_NAME=\"", "").replace("\"\n", "")
    text += f"     OS: {os} [Kernel: {platform.release()}] ({platform.architecture()[0]})\n"

    return text

def copy_text():

    text = get_result_text()

    # Copying to Clipboard

    clipboard_tk = tkinter.Tk()
    clipboard_tk.withdraw()
    clipboard_tk.clipboard_clear()
    clipboard_tk.clipboard_append(text)
    clipboard_tk.update()
    clipboard_tk.destroy()

def fix_permissions(path):

    sudo_user = os.environ.get("SUDO_USER")
    if sudo_user:
        pw = pwd.getpwnam(sudo_user)
        uid, gid = pw.pw_uid, pw.pw_gid
    else:
        uid = os.getuid()
        gid = os.getgid()

    os.chown(path, uid, gid)
    os.chmod(path, 0o644)

def save_text():

    path = tkinter.filedialog.asksaveasfilename(
        parent = window_home,
        filetypes = [("Text Files", "*.txt")],
        defaultextension = ".txt",
        initialdir = PATH_HOME
    )

    with open(path, "w") as file:
        file.write(get_result_text())

    fix_permissions(path)

def save_image():

    global window_home

    path = PATH_HOME + "Pictures"
    if not os.path.exists(path):
        path = PATH_HOME
    path = tkinter.filedialog.asksaveasfilename(
        parent = window_home,
        filetypes = [("PNG Files", "*.png")],
        defaultextension = ".png",
        initialdir = path
    )

    def capture_window():

        ImageGrab.grab(
            bbox = (
                window_home.winfo_rootx(),
                window_home.winfo_rooty(),
                window_home.winfo_rootx() + window_home.winfo_width(),
                window_home.winfo_rooty() + window_home.winfo_height()
            )
        ).save(path)

        fix_permissions(path)

    window_home.after(1000, capture_window)

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

def round_pad(num, digits):
    return f"{round(num, digits):.{digits}f}"


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

    global hardware
    global profile
    global mix

    global background
    global foreground
    global highlight
    global bg_image
    global font

    global unit
    global language

    global profiles

    # Result Variables

    global results
    global result_labels

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

    with open(PATH_DATA + "info.json", "r") as file:
        info_raw = json.load(file)
    names = info_raw["names"]
    created = info_raw["created"]
    version = info_raw["version"]
    updated = info_raw["updated"]

    with open(PATH_DATA + "settings.json", "r") as file:
        settings_raw = json.load(file)

    test_count = settings_raw["test_count"]
    test_size = settings_raw["test_size"]
    test_data = settings_raw["test_data"]
    test_path = settings_raw["test_path"]

    hardware = settings_raw["hardware"]
    profile = settings_raw["profile"]
    mix = settings_raw["mix"]

    background = settings_raw["background"]
    foreground = settings_raw["foreground"]
    highlight = settings_raw["highlight"]
    bg_image = settings_raw["bg_image"]
    font = settings_raw["font"]

    unit = settings_raw["unit"]
    language = settings_raw["language"]

    with open(PATH_DATA + "profiles.json", "r") as file:
        profiles_raw = json.load(file)

    profiles = {
        "default": {
            "default": [],
            "peak_performance": [],
            "real_world_performance": [],
            "demo": [],
            "measure_time": 0,
            "interval_time": 0
        },
        "nvme_ssd": {
            "default": [],
            "peak_performance": [],
            "real_world_performance": [],
            "demo": [],
            "measure_time": 0,
            "interval_time": 0
        },
        "flash_memory": {
            "default": [],
            "peak_performance": [],
            "real_world_performance": [],
            "demo": [],
            "measure_time": 0,
            "interval_time": 0
        }
    }

    hardware_names = ["default", "nvme_ssd", "flash_memory"]
    profile_names = ["default", "peak_performance", "real_world_performance", "demo"]

    for i in range(3):
        tests_raw = profiles_raw[hardware_names[i]]
        for ii in range(4):
            tests = tests_raw[profile_names[ii]]
            for test in tests.values():
                profiles[hardware_names[i]][profile_names[ii]].append(
                    Test(
                        test["random"],
                        test["block_size"],
                        test["queues"],
                        test["threads"],
                        test["unit"]
                    )
                )
        profiles[hardware_names[i]]["measure_time"] = tests_raw["measure_time"]
        profiles[hardware_names[i]]["interval_time"] = tests_raw["interval_time"]

    # Results

    results = [
        [
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0}
        ],
        [
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0}
        ],
        [
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0},
            {"MB/s": 0, "IOPS": 0, "us": 0}
        ]
    ]
    result_labels = [[], [], []]

    # Process Title

    setproctitle.setproctitle("linuxdiskmark")

    # Home Window

    open_window_home()

# Run Main Function

if __name__ == "__main__":
    main()