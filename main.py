#!/usr/bin/env python3
import sys
import os
import threading
import datetime
import subprocess
import gettext
import locale
import shutil
import argparse

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk

# Настройка локализации
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(BASE_DIR, 'locales')
locale.bindtextdomain('secux-iso', LOCALE_DIR)
gettext.bindtextdomain('secux-iso', LOCALE_DIR)
gettext.textdomain('secux-iso')
_ = gettext.gettext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "build_log.txt")
OFFLINE_REPO_PATH = "/var/cache/pacman/offline-repo"
APP_ID = "secux-iso"
LOCALES_DIR = os.path.join(BASE_DIR, "locales")

def init_i18n():
    """Инициализация системы перевода для Python и GTK"""
    try:
        if os.environ.get("LANG") is None:
             os.environ["LANG"] = "en_US.UTF-8"
        
        locale.setlocale(locale.LC_ALL, '') 
    except locale.Error:
        print("Warning: Failed to set locale. Using default.")

    try:
        lang = gettext.translation(APP_ID, localedir=LOCALES_DIR, fallback=True)
        lang.install()
    except Exception as e:
        print(f"Python translation error: {e}")
        import builtins
        builtins._ = lambda x: x

    try:
        locale.bindtextdomain(APP_ID, LOCALES_DIR)
        
        if hasattr(locale, 'bind_textdomain_codeset'):
            locale.bind_textdomain_codeset(APP_ID, 'UTF-8')
        
        locale.textdomain(APP_ID)
        
        gettext.bindtextdomain(APP_ID, LOCALES_DIR)
        gettext.textdomain(APP_ID)
        
    except Exception as e:
        print(f"GTK/C translation bind error: {e}")


def run_build_worker(work_dir, iso_dir, update_repo, online, offline):
    """
    Эта функция выполняется с правами root.
    Она не имеет доступа к GUI, а пишет логи в stdout.
    """
    
    # Функция для логирования, которая сбрасывает буфер (чтобы GUI видел текст сразу)
    def log(msg):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        print(f"{timestamp} {msg}", flush=True)

    # Вспомогательная функция выполнения команд
    def run_cmd(cmd_list, shell=False, cwd=None):
        log(f"> {' '.join(cmd_list) if isinstance(cmd_list, list) else cmd_list}")
        try:
            # Используем stdbuf для отключения буферизации вывода вызываемых программ
            if not shell and cmd_list[0] != "stdbuf":
                cmd_list = ["stdbuf", "-oL"] + cmd_list

            process = subprocess.Popen(
                cmd_list,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=shell,
                cwd=cwd
            )
            for line in process.stdout:
                print(line, end='', flush=True)
                
            process.wait()
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, cmd_list)
        except Exception as e:
            log(f"ОШИБКА выполнения команды: {e}")
            raise e

    def get_metapackages(metapackage) -> list:
        # pacman запускается напрямую, так как мы root
        res = subprocess.run(['pacman', '-Sg', metapackage], check=True, capture_output=True)
        return [i.split(' ')[-1] for i in res.stdout.decode().strip().split("\n") if i]

    def _check_kolbanidze_key() -> bool:
        """Checks if the Kolbanidze PGP key is trusted."""
        key_id = "CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE"
        command = ['/usr/bin/pacman-key', '--list-keys', key_id]
        try:
            result = subprocess.run(command, check=False, capture_output=True)
            code = result.returncode
            return code == 0
        except Exception as e:
            return False

    def _add_kolbanidze_key():
        """Attempts to add the Kolbanidze key."""
        keyring_path = os.path.join(BASE_DIR, "releng/airootfs/usr/share/pacman/keyrings")
        kolbanidze_gpg = os.path.join(keyring_path, "kolbanidze.gpg" )
        log(kolbanidze_gpg)

        if not os.path.exists(kolbanidze_gpg):
            return False 

        command = ["/usr/bin/pacman-key", '--add', kolbanidze_gpg]
        run_cmd(command)
        
        command = ['/usr/bin/pacman-key', '--lsign-key', 'CE48F2CC9BE03B4EFAB02343AA0A42D146D35FCE']
        run_cmd(command)

    try:
        log(_("--- ЗАПУСК СБОРКИ (ROOT MODE) ---"))
        log(_("Рабочая директория: ") + work_dir)
        log(_("ISO директория: ") + iso_dir)
        log(f"Update={update_repo}, Online={online}, Offline={offline}")

        # Проверки
        if online or offline:
            if not os.path.exists(work_dir):
                log(_("Создание рабочей директории: ") + work_dir)
                os.makedirs(work_dir, exist_ok=True)
            if not os.path.exists(iso_dir):
                log(_("Создание ISO директории: ") + iso_dir)
                os.makedirs(iso_dir, exist_ok=True)

        if not online and not offline and not update_repo:
            log(_("Внимание: Не выбран ни один активный режим работы."))
            return

        if not _check_kolbanidze_key():
            log(_("Сертификат kolbanidze не найден. Попытка автоматического добавления."))
            _add_kolbanidze_key()
        
        if update_repo:
            log(_("INFO: Обновление офлайн репозитория ПО: ") + OFFLINE_REPO_PATH)
            if os.path.isdir(OFFLINE_REPO_PATH):
                log(_("Удаление старого репозитория..."))
                shutil.rmtree(OFFLINE_REPO_PATH)
            
            log(_("INFO: Сбор списка пакетов..."))
            
            # Базовый список пакетов
            packages = ['base', 'base-devel', 'linux', 'linux-lts', 'linux-hardened', 
                        'linux-headers', 'linux-lts-headers', 'linux-hardened-headers', 
                        'linux-firmware', 'amd-ucode', 'intel-ucode', 'vim', 'nano', 
                        'efibootmgr', 'sudo', 'plymouth', 'python-pip', 'python-dbus', 
                        'v4l-utils', 'lvm2', 'networkmanager', 'systemd-ukify', 
                        'sbsigntools', 'efitools', 'less', 'git', 'ntfs-3g', 'gvfs', 
                        'gvfs-mtp', 'xdg-user-dirs', 'fwupd', 'sbctl', 'shim-signed', 
                        'mokutil', 'networkmanager-openvpn', 'gnome-tweaks', 'secux-hooks']
            
            packages += ['vlc', 'vlc-plugin-ffmpeg', 'firefox', 'chromium', 
                         'libreoffice', 'keepassxc']

            packages += ['tk', 'python-pexpect', 'python-pillow', 'python-darkdetect', 
                         'python-packaging', 'python-setuptools', 'python-dotenv']
            packages += ['libpam-google-authenticator', 'python-qrcode', 'vte4', 
                         'apparmor', 'ufw', 'secux-security-manager']
            
            # IDP
            packages += ['python-argon2-cffi', 'python-pycryptodome', 'tpm2-tools']

            # Метапакеты
            log(_("Получение пакетов GNOME..."))
            packages += get_metapackages('gnome')
            log(_("Получение пакетов Plasma..."))
            packages += get_metapackages('plasma')
            log(_("Получение пакетов KDE Applications..."))
            packages += get_metapackages('kde-applications')
            log(_("Получение пакетов Xorg..."))
            packages += get_metapackages('xorg')

            # Разрешение зависимостей через pactree
            log(_("Разрешение зависимостей (это может занять время)..."))
            dependencies = []
            
            total_pkg = len(packages)
            for i, package in enumerate(packages):
                if i % 10 == 0:
                    print(_("Обработка зависимостей:") + f" {i}/{total_pkg}", flush=True)
                    
                try:
                    cmd = subprocess.run(["pactree", '-su', package], capture_output=True, check=True)
                    output = cmd.stdout.decode().strip().split('\n')
                    dependencies.extend(output)
                except subprocess.CalledProcessError:
                    log(_("Внимание: не удалось получить дерево для ") + package)

            dependencies = list(set(dependencies))
            dependencies.extend(["xorg", "gnome", "plasma"])

            # Очистка версий (>, <, =)
            cleaned_deps = []
            for dep in dependencies:
                if not dep: continue
                d = dep
                if "<" in d: d = d.split("<")[0]
                if ">" in d: d = d.split(">")[0]
                if "=" in d: d = d.split("=")[0]
                cleaned_deps.append(d)
            
            dependencies = sorted(list(set(cleaned_deps)))

            log(_("Всего пакетов для скачивания: ") + str(len(dependencies)))
            log(_("INFO: Запуск pacman для скачивания пакетов..."))
            if not os.path.exists(OFFLINE_REPO_PATH):
                os.mkdir(OFFLINE_REPO_PATH)

            # Формирование команды pacman
            pacman_args = ["/usr/bin/pacman", '-Sywu', '--noconfirm', '--cachedir', OFFLINE_REPO_PATH] + dependencies
            
            run_cmd(pacman_args)

            repo_db_name = "offline-repo.db.tar.zst"
            repo_files_name = "offline-repo.files.tar.zst"
            repo_db_path = os.path.join(OFFLINE_REPO_PATH, repo_db_name)
            
            files_to_add = []
            try:
                for item in os.listdir(OFFLINE_REPO_PATH):
                    full_path = os.path.join(OFFLINE_REPO_PATH, item)
                    if os.path.isfile(full_path):
                        if item.endswith(('.pkg.tar.zst', '.pkg.tar.xz', '.pkg.tar.gz')) and \
                           not item.endswith('.sig') and \
                           item != repo_db_name and item != repo_files_name:
                            files_to_add.append(full_path)
                            
            except OSError as e:
                msg = _("Ошибка чтения офлайн кэша ") + f"{OFFLINE_REPO_PATH}: {e}"
                log(msg)
                raise Exception(msg)

            if not files_to_add:
                msg = _("Пакеты не найдены в ") + f"{OFFLINE_REPO_PATH}."
                log(msg)
                raise Exception(msg)

            repo_add_cmd = ['/usr/bin/repo-add', repo_db_path] + files_to_add
            try:
                run_cmd(repo_add_cmd)
                log(_("INFO: База данных репозитория успешно обновлена."))
            except Exception as e:
                log(_("Ошибка при создании базы данных репозитория."))
                raise e

        airootfs_path = os.path.join(BASE_DIR, "releng/airootfs")
        build_cache_path = os.path.join(airootfs_path, "var/cache/pacman")
        offline_repo_path = os.path.join(build_cache_path, "offline-repo")
        releng_path = os.path.join(BASE_DIR, "releng")
        default_iso_name = 'Secux-Linux-x86_64.iso'
        iso_src = os.path.join(work_dir, default_iso_name)

        if online:
            if os.path.exists(offline_repo_path):
                shutil.rmtree(offline_repo_path)
            # src = os.path.join(airootfs_path, "etc/pacman_online.conf")
            # dst = os.path.join(airootfs_path, "etc/pacman.conf")
            # shutil.copy(src, dst)
            offline_conf = os.path.join(airootfs_path, "etc/offline_installation.conf")
            if os.path.exists(offline_conf):
                os.remove(offline_conf)

            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)
                os.mkdir(work_dir)
            mkarchiso_cmd = ['/usr/bin/mkarchiso', '-v', '-w', work_dir, '-o', work_dir, releng_path]
            run_cmd(mkarchiso_cmd)
            output_file = f"SecuxLinux-online-{datetime.datetime.today().strftime('%Y-%m-%d_%H-%M')}.iso"
            iso_dst = os.path.join(iso_dir, output_file)
            shutil.move(iso_src, iso_dst)
            log(f"===== {output_file} =====")

        if offline:
            if os.path.exists(offline_repo_path):
                shutil.rmtree(offline_repo_path)
            os.makedirs(build_cache_path, exist_ok=True)
            rsync_cmd = ['/usr/bin/rsync', '-aAXHv', '--delete', OFFLINE_REPO_PATH, build_cache_path]
            run_cmd(rsync_cmd)
            offline_conf = os.path.join(airootfs_path, "etc/offline_installation.conf")
            if not os.path.exists(offline_conf):
                with open(offline_conf, "w") as file:
                    pass
            # src = os.path.join(airootfs_path, "etc/pacman_offline.conf")
            # dst = os.path.join(airootfs_path, "etc/pacman.conf")
            # shutil.copy(src, dst)

            
            if os.path.exists(work_dir):
                shutil.rmtree(work_dir)
                os.mkdir(work_dir)

            mkarchiso_cmd = ['/usr/bin/mkarchiso', '-v', '-w', work_dir, '-o', work_dir, releng_path]
            run_cmd(mkarchiso_cmd)
            output_file = f"SecuxLinux-offline-{datetime.datetime.today().strftime('%Y-%m-%d_%H-%M')}.iso"
            iso_dst = os.path.join(iso_dir, output_file)
            shutil.move(iso_src, iso_dst)
            log(f"===== {output_file} =====")

        log(_("Процесс завершен."))

    except Exception as e:
        log(f"ERROR: {e}")
        sys.exit(1)

def get_ui_path(filename):
    return os.path.join(os.path.join(BASE_DIR, "ui"), filename)

def load_resources():    
    res = Gio.Resource.load(os.path.join(BASE_DIR, "resources.gresource"))
    
    Gio.resources_register(res)

    display = Gdk.Display.get_default()
    icon_theme = Gtk.IconTheme.get_for_display(display)
    
    icon_theme.add_resource_path("/org/secux/builder/icons")

class LanguageManager:
    """Класс для управления сменой языка"""
    
    # Карта: Индекс в DropDown -> Код локали
    LANG_MAP = {
        0: "ru_RU.UTF-8",
        1: "en_US.UTF-8"
    }

    @staticmethod
    def set_language(index):
        new_lang = LanguageManager.LANG_MAP.get(index, "en_US.UTF-8")
        
        # Если язык уже такой, ничего не делаем
        current = os.environ.get("LANG")
        if current and new_lang in current:
            return

        print(f"Switching language to {new_lang}...")
        
        os.environ["LANG"] = new_lang
        
        python = sys.executable
        os.execl(python, python, *sys.argv)



@Gtk.Template(filename=get_ui_path("window.ui"))
class SecuxBuilderWindow(Adw.ApplicationWindow):
    __gtype_name__ = "BuilderPage"
    stack = Gtk.Template.Child()
    row_work_dir = Gtk.Template.Child()
    btn_change_work_dir = Gtk.Template.Child()
    row_iso_dir = Gtk.Template.Child()
    btn_change_iso_dir = Gtk.Template.Child()
    check_online = Gtk.Template.Child()
    check_offline = Gtk.Template.Child()
    check_repo = Gtk.Template.Child()
    btn_start_build = Gtk.Template.Child()
    text_log = Gtk.Template.Child()
    text_buffer = Gtk.Template.Child()
    combo_lang = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        workdir = os.path.join(BASE_DIR, "bin")
        if not os.path.isdir(workdir):
            os.mkdir(workdir)
        self.row_work_dir.set_subtitle(workdir)

        isodir = os.path.join(BASE_DIR, "builds")
        if not os.path.isdir(isodir):
            os.mkdir(isodir)
        self.row_iso_dir.set_subtitle(isodir)

        self._add_action("on_select_work_dir", self.on_select_work_dir)
        self._add_action("on_select_iso_dir", self.on_select_iso_dir)
        self._add_action("on_start_build", self.on_start_build)

        current_lang = os.environ.get("LANG", "ru_RU.UTF-8")
        if "ru" in current_lang.lower():
            initial_index = 0
        else:
            initial_index = 1
        self.combo_lang.set_selected(initial_index)
        self.combo_lang.connect("notify::selected", self.on_language_changed)

    def on_language_changed(self, widget, pspec):
        i = widget.get_selected()
        LanguageManager.set_language(i)


    def _add_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
    
    def on_select_work_dir(self, a, b):
        def update_work_dir(path):
            self.row_work_dir.set_subtitle(path)
        self.select_folder(update_work_dir)

    def on_select_iso_dir(self, a, b):
        def update_iso_dir(path):
            self.row_iso_dir.set_subtitle(path)
        self.select_folder(update_iso_dir)

    def select_folder(self, callback, initial_path=None):
        dialog = Gtk.FileDialog.new()
        dialog.set_title(_("Выберите папку"))
        
        if initial_path:
            dialog.set_initial_folder(Gio.File.new_for_path(initial_path))
        
        def on_response(dlg, result):
            try:
                folder = dlg.select_folder_finish(result)
                callback(folder.get_path())
            except GLib.Error:
                callback(None)
        
        dialog.select_folder(parent=self, cancellable=None, callback=on_response)

    def on_start_build(self, a, b):
        self.stack.set_visible_child_name("progress_page")

        self.text_buffer.set_text("")
        self.log(_("Инициализация процесса сборки..."))
        params = {
            'workdir': self.row_work_dir.get_subtitle(),
            'isodir': self.row_iso_dir.get_subtitle(),
            'online': self.check_online.get_active(),
            'offline': self.check_offline.get_active(),
            'update': self.check_repo.get_active()
        }
        thread = threading.Thread(target=self._run_pkexec_process, args=(params,), daemon=True)
        thread.start()

    def _run_pkexec_process(self, params):
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)
        
        cmd = [
            "/usr/bin/pkexec", 
            python_exe, 
            script_path,
            "--worker",
            "--workdir", params['workdir'],
            "--isodir", params['isodir']
        ]
        
        if params['update']: cmd.append("--update")
        if params['online']: cmd.append("--online")
        if params['offline']: cmd.append("--offline")

        self.log("Запрос привилегий root через pkexec...")
        self.log(f"Command: {' '.join(cmd)}")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                self.update_console(line)
            
            process.wait()
            
            if process.returncode == 0:
                self.update_console(_("\nСборка/Обновление завершено успешно.\n"))
            elif process.returncode == 126 or process.returncode == 127:
                self.update_console(_("\nОшибка аутентификации или отмена пользователем.\n"))
            else:
                self.update_console(_("\nПроцесс завершился с кодом ошибки: ") + str(process.returncode))

        except Exception as e:
            self.log(f"PKEXEC ERROR: {e}")


    def update_console(self, text):
        # print(text)
        GLib.idle_add(self._append_text, text)

    def _append_text(self, text):
        end_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert(end_iter, text)
        
        # Автоскролл вниз
        parent = self.text_log.get_parent()
        if isinstance(parent, Gtk.Viewport):
             parent = parent.get_parent()
             
        if isinstance(parent, Gtk.ScrolledWindow):
            adj = parent.get_vadjustment()
            if adj:
                adj.set_value(adj.get_upper() - adj.get_page_size())

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_message = f"{timestamp} {message}"

        self.update_console(f"{full_message}\n")
        
        print(full_message)

        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(full_message + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

class SecuxApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="org.secux.builder",
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)

    def do_activate(self):
        win = SecuxBuilderWindow(application=self)
        win.present()

if __name__ == "__main__":
    # Парсим аргументы
    init_i18n()
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true", help=_("Запуск в режиме Worker (Root)"))
    parser.add_argument("--workdir", default="")
    parser.add_argument("--isodir", default="")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--offline", action="store_true")

    # Используем parse_known_args, чтобы GTK аргументы не ломали парсер, если они передадутся
    args, unknown = parser.parse_known_args()

    if args.worker:
        # === РЕЖИМ WORKER (ROOT) ===
        # Здесь нет GTK, только логика
        run_build_worker(
            work_dir=args.workdir,
            iso_dir=args.isodir,
            update_repo=args.update,
            online=args.online,
            offline=args.offline
        )
    else:
        # === РЕЖИМ GUI (USER) ===
        load_resources()
        app = SecuxApp()
        app.run(sys.argv)
