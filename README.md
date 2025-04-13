# 🛡️ Secux Linux Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Russian](https://img.shields.io/badge/README-in_Russian-red.svg)](README.ru.md)

Build your own Secux Linux ISO images with ease! This tool helps you create installable media for Secux Linux, a security-focused distribution based on Arch Linux 🐧.

**Author:** [kolbanidze](https://github.com/kolbanidze)

---

## ✨ What is Secux Linux?

Secux Linux aims to be a **secure Linux distribution** built upon the solid foundation of Arch Linux. Key components include:

*   **Secux Linux Installer:** A custom installer designed for Secux Linux.
*   **Security Manager:** Tools and configurations focused on enhancing system security.
*   **KIRTapp Integration:** Includes integration for KIRTapp (developed by a partner), although it's *not* installed by default in the Secux Linux for various reasons.

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
```

**Modes:**

*   **GUI Mode (Default):**
    ```bash
    sudo python main.py
    ```
    A graphical window will appear allowing you to select build options.
*   **CLI Mode:**
    ```bash
    sudo python main.py --cli [OTHER_OPTIONS]
    ```
    The script will run directly in your terminal based on the provided command-line flags.

**Common Examples:**

*   **Create an Online ISO (GUI):**
    ```bash
    sudo python main.py
    # Check "Create Online Build", optionally change directories, click "Build"
    ```
*   **Create an Offline ISO (CLI):**
    ```bash
    sudo python main.py --cli --offline
    ```
*   **Update Offline Software & Repo, then Build Offline ISO (CLI):**
    ```bash
    sudo python main.py --cli --update-offline-software --update-offline-repo --offline
    ```
*   **Run GUI in Russian with 125% Scaling:**
    ```bash
    sudo python main.py --russian --scaling 125
    ```

---

## 🔧 Command-Line Options

*   `-h, --help`: Show help message and exit.
*   `-r, --russian` / `--no-russian` 🌐: Use Russian language in GUI (or force English with `--no-russian`). Defaults to auto-detect based on system locale.
*   `-c, --cli` / `--no-cli` ⌨️: Disable GUI and run in command-line mode. Default is `--no-cli` (GUI).
*   `-n, --online` / `--no-online` ☁️: Create an online build ISO. Requires internet during installation.
*   `-f, --offline` / `--no-offline` 💾: Create an offline build ISO. Includes packages for offline installation.
*   `-b BIN, --bin BIN` 📁: Working directory for building (default: `./bin`).
*   `-o OUTPUT, --output OUTPUT` 💿: Directory for final ISO images (default: `./builds`).
*   `-u, --update-offline-software` 🔄: Update bundled offline software (Secux Installer/Apps, KIRTapp) by cloning/pulling from Git before building.
*   `-i, --update-offline-repo` 📦: Update the local offline package repository used for offline builds. Downloads packages and rebuilds the repo DB.
*   `-s SCALING, --scaling SCALING` 🔍: GUI scaling percentage (e.g., `100`, `125`, `150`). Default: `100`.
*   `-d, --dark-theme` 🌙: Use dark theme in the GUI.
*   `--version` ℹ️: Show version and exit.
*   `--install-all-dependencies` 🛠️: Attempt to install all required `pacman` and `pip` dependencies and exit.

---

## ☁️ Online vs. 💾 Offline Builds
*   **Online Build (`--online`):**
    *   Produces a *smaller* ISO file.
    *   Requires a working internet connection on the target machine during Secux Linux installation to download packages.
    *   Faster to build the ISO itself.
*   **Offline Build (`--offline`):**
    *   Produces a *larger* ISO file.
    *   Includes a repository of packages directly on the ISO.
    *   Allows installation on machines *without* an internet connection.
    *   Requires downloading all necessary packages *before* building the ISO (can be time-consuming, especially the first time or when using `--update-offline-repo`).

---

## 🔄 Offline Repository & Software Updates

*   **`--update-offline-software (-u)`:** Use this flag if you want the latest versions of `secux-installer`, `secux-apps`, and `KIRTapp` included in your *next* build. It fetches the latest code from their respective Git repositories.
*   **`--update-offline-repo (-i)`:** Use this flag to refresh the entire set of packages used for offline builds. It will:
    1.  Determine the necessary packages and dependencies (based on the lists in the script).
    2.  Download the latest versions of these packages using `pacman`.
    3.  Create/update the offline repository database (`offline-repo.db.tar.zst`) in `/var/cache/pacman/offline-repo`.
    This can take a significant amount of time and download bandwidth. You typically only need to do this periodically or if you need newer base packages for the offline installation.

---

## 🤝 Contributing

Contributions are welcome! If you find bugs or have suggestions, please open an issue on the GitHub repository. Pull requests are also appreciated.

---

## 📜 License

This project is licensed under the **MIT License**. See the LICENSE file for details.
