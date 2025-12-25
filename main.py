#!/usr/bin/env python3
import sys
import os
import threading
import datetime
import subprocess
import gettext
import locale

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

LOG_FILE = "build_log.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_ui_path(filename):
    return os.path.join(os.path.join(BASE_DIR, "ui"), filename)

def load_resources():    
    res = Gio.Resource.load("resources.gresource")
    
    Gio.resources_register(res)

    display = Gdk.Display.get_default()
    icon_theme = Gtk.IconTheme.get_for_display(display)
    
    icon_theme.add_resource_path("/org/secux/builder/icons")


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
    check_apps = Gtk.Template.Child()
    check_repo = Gtk.Template.Child()
    btn_start_build = Gtk.Template.Child()
    text_log = Gtk.Template.Child()
    text_buffer = Gtk.Template.Child()

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

        action_work = Gio.SimpleAction.new("on_select_work_dir", None)
        action_work.connect("activate", self.on_select_work_dir)
        self.add_action(action_work)

        action_iso = Gio.SimpleAction.new("on_select_iso_dir", None)
        action_iso.connect("activate", self.on_select_iso_dir)
        self.add_action(action_iso)

        action_build = Gio.SimpleAction.new("on_start_build", None)
        action_build.connect("activate", self.on_start_build)
        self.add_action(action_build)

    
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
        self.log("Запуск процесса сборки...")
        
        thread = threading.Thread(target=self._installation_sequence, daemon=True)
        thread.start()

    def _installation_sequence(self):
        try:
            self.log(_("Проверка конфигурации..."))
            
            online_build = self.check_online.get_active()
            offline_build = self.check_offline.get_active()
            update_apps = self.check_apps.get_active()
            update_repo = self.check_repo.get_active()

            work_dir_path = self.row_work_dir.get_subtitle()
            iso_dir_path = self.row_iso_dir.get_subtitle()
            
            if online_build or offline_build:
                if not os.path.isdir(work_dir_path):
                    self.log(_("Ошибка. Рабочая директория не найдена."))
                    return
                if not os.path.isdir(iso_dir_path):
                    self.log_("Ошибка. ISO директория не найдена.")
                    return

                self.log(_("Рабочая директория: ") + work_dir_path)
                self.log(_("ISO директория: ") + iso_dir_path)
            
            if not online_build and not offline_build:
                self.log(_("Внимание. Не выбран тип сборки (онлайн/офлайн)."))
            
            if update_apps:
                self.log(_("Обновление приложений..."))
                secux_installer_path = os.path.join(BASE_DIR, "releng/airootfs/usr/local/share/secux-installer")

            # if online_build:
            #     self.log("Запуск сборки Online образа...")
            #     self.execute(["echo", "Building Online ISO..."])
            #     # self.execute(["sudo", "./build_iso.sh", "--online"], cwd=self.work_dir_path)
            #     GLib.usleep(2000000)

            # if offline_build:
            #     self.log("Запуск сборки Offline образа...")
            #     self.execute(["echo", "Building Offline ISO..."])
            #     GLib.usleep(2000000)

            self.log("Сборка завершена успешно!")
            self.execute(["echo", "Done."])

        except Exception as e:
            self.log(f"КРИТИЧЕСКАЯ ОШИБКА ПОТОКА: {e}")

    def update_console(self, text):
        # print(text) # Дублирование в терминал, если нужно
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

    def execute(self, cmd: list, input_str: str = None, shell=False, cwd=None):
        """
        Выполняет команду, пишет вывод в лог UI.
        """
        cmd_str = " ".join(cmd)
        self.log(f"> {cmd_str}")

        try:           
            process = subprocess.Popen(
                cmd, # Убрал принудительный sudo для списка, добавляйте его в cmd при вызове если надо
                stdin=subprocess.PIPE if input_str else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=shell,
                cwd=cwd
            )

            if input_str:
                stdout_data, _ = process.communicate(input=input_str + "\n")
                if stdout_data:
                    self.update_console(stdout_data)
            else:
                # Читаем вывод построчно в реальном времени
                for line in process.stdout:
                    self.update_console(line)
            
            process.wait()
            
            if process.returncode != 0:
                self.log(f"ERROR: Command failed with code {process.returncode}")
                return process.returncode
            
            return 0

        except Exception as e:
            self.log(f"EXECUTION ERROR: {e}")
            return 1

class SecuxApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="org.secux.builder",
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)

    def do_activate(self):
        win = SecuxBuilderWindow(application=self)
        win.present()

if __name__ == "__main__":
    load_resources()
    app = SecuxApp()
    app.run(sys.argv)
