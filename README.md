# Secux Linux Builder

[![Russian](https://img.shields.io/badge/README-на_русском-red.svg)](README.ru.md)

This repository contains the source code of Secux Linux Builder, necessary for building Secux Linux ISO images. 

<p align="center">
    <img src="https://raw.githubusercontent.com/kolbanidze/secux-iso/refs/heads/main/welcome.en.png" width=384>
</p>

## Launch

To launch the builder: `python main.py`

After launching the installation, it will restart in `worker` mode. To obtain root access, pkexec is used.

### Technical Information
* The interface is written in Python using GTK 4 and Libadwaita.
* Interaction with the disk and the system is carried out through `subprocess` as root. 
* Dependencies:
    * `python-gobject`
    * `libadwaita`
    * `gtk4`
    * `archiso`
    * `rsync`
    * `pacman-contrib`
    * `pacman`
    * An Arch Linux-based distribution (for example, Secux Linux)