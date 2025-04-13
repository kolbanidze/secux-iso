# 🛡️ Secux Linux Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Build your own Secux Linux ISO images with ease! This tool helps you create installable media for Secux Linux, a security-focused distribution based on Arch Linux 🐧.

**Author:** [kolbanidze](https://github.com/kolbanidze)

---

## ✨ What is Secux Linux?

Secux Linux aims to be a **secure Linux distribution** built upon the solid foundation of Arch Linux. Key components include:

*   **Secux Linux Installer:** A custom installer designed for Secux Linux.
*   **Security Manager:** Tools and configurations focused on enhancing system security.
*   **KIRTapp Integration:** Includes integration points for KIRTapp (developed by a partner), although it's *not* installed by default in the built ISO for various reasons.

This builder automates the process of creating both online and offline installation ISOs.

---

## 🚀 Features

*   **🖥️ GUI & ⌨️ CLI Modes:** Use a graphical interface (built with CustomTkinter) or run entirely from the command line.
*   **☁️ Online Builds:** Create smaller ISOs that download packages during installation.
*   **💾 Offline Builds:** Create larger, self-contained ISOs with a built-in package repository for offline installation.
*   **🔄 Offline Software Updates:** Easily update the bundled versions of Secux Installer, Secux Apps, and KIRTapp from their Git repositories.
*   **📦 Offline Repository Management:** Update the local offline package repository used for offline builds.
*   **📁 Customizable Directories:** Specify custom working (`--bin`) and output (`--output`) directories.
*   **🌐 Multi-Language Support:** Supports English and Russian (auto-detects system locale or can be set via flag).
*   **🎨 UI Customization:** Adjust GUI scaling (`--scaling`) and enable dark mode (`--dark-theme`).
*   **🛠️ Dependency Management:** Includes helpers to check and install required dependencies.
*   **🔑 Key Management:** Handles PGP keys required for custom Secux repositories.

---

## 🧱 Requirements

*   **OS:** An Arch Linux based distribution 🐧.
*   **Privileges:** Root access is required 🔑 (uses `pacman`, `mkarchiso`, mounts, etc.).
*   **Critical Dependencies:**
    *   `archiso`
    *   `git`
    *   `rsync`
    *   `pacman-contrib` (for `pactree`)
    *   `python` (usually >= 3.8)
    *   `python-pip`
    *   `python-pillow`
    *   `python-requests`
    *   `tk`
    *   `bash`
*   **Python Pip Packages:**
    *   `customtkinter`
*   **Internet Connection:** Required for dependency installation, ISO builds, and updating components.

---

## ⚙️ Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/kolbanidze/secux-iso
    cd secux-iso
    ```

2.  **Install Dependencies:**
    *   **Recommended:** Use the built-in helper (run as root):
        ```bash
        sudo python main.py --install-all-dependencies
        ```
    *   **Manual:** If the helper fails or you prefer manual installation (run as root):
        ```bash
        # Install Pacman packages
        sudo pacman -Syu --needed archiso git rsync pacman-contrib python-pip python-pillow python-requests python-packaging python-darkdetect tk bash

        # Install Pip package(s) - Use --break-system-packages if needed on newer pip/Arch
        sudo pip install customtkinter --break-system-packages
        ```

---

## 🚀 How to Use

Run the script using `python main.py`. Root privileges are required.

```bash
sudo python main.py [OPTIONS]
