# LinuxDiskMark
### Released February 2026
### Version 1.0.0
### Updated February 1.0.0

<br/>

## Description
LinuxDiskMark is a graphical disk benchmarking application
designed to look and function like CrystalDiskMark on Windows.
It uses `fio` to benchmark the disk under varios conditions
and displays the results.

<br/>

## Requirements

This project requires `fio`, which will be automatically installed.

### Memory
This application uses approximately 256 KiB of memory.

### Storage
This application uses approximately XY MiB of storage for the .deb package
and approximately XY MiB of storage for the .rpm package. fio requires about
2 MiB of storage.

<br/>

## Installation

Download the appropriate package
[here](liam-ralph.github.io/projects/linuxdiskmark).

I have also added two development packages to my website, which include a number
of other files used to create the .deb and .rpm packages, as well as some
documentation. These are not required to install the package, but may be useful
for those looking to edit it.

<br/>

## Operating System Support

Support is assumed for all Debian- and Fedora-based distros. Below is a list of
all distros for which support has been confirmed.

### Debian Based

 - Ubuntu 24.04.3
 - Ubuntu 25.04
 - Linux Mint 22.3
 - Debian 13
 - MX Linux 23.6
 - Pop!_OS 24.04

Pop!_OS 22.04 is not supported, but you can compile the executable yourself (for
instructions, see the developer package).

### Fedora Based

 - Fedora 43
 - Nobara 43