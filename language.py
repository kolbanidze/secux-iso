class Locale:
    def __init__(self, language: str) -> None:
        if language == "en":
            self.CURRENT_LANGUGAGE = "en"
            self.arch_based = "To build Secux Linux you need Arch Linux or a distribution based on it"
            self.not_installed_use = "not installed. To install, use"
            self.missing_deps = "Missing dependencies were found on startup. Use the flag to install automatically"
            self.root = 'Run the application only as root'
            self.cli_on = "CLI mode enabled"
            self.releng_error = "Directory releng not found. Unable to create Secux Linux image"
            self.internet_error = "To build Secux Linux you need a stable internet connection"
            self.not_installed_deps = "Required dependencies are not installed"
            self.offline_repo_autocreate = "An offline repository will be created automatically."
            self.scaling_error = "Incorrect scaling specified. Revert to default 100%"
            self.scaling = "Scaling"
            self.workdir = "Work directory"
            self.changedir = "Change directory"
            self.isoimagesfolder = "ISO images output"
            self.online_build = "Online build"
            self.offline_build = "Offline build"
            self.online_label = "Minimal ISO image. Internet connection\nrequired for installation/system."
            self.offline_label = "ISO image with all applications and \npackages required for installation."
            self.update_apps = "Download/update apps"
            self.offline_os = "The offline repository contains the system, all necessary\npackages and dependencies for installing Secux Linux."
            self.offline_repo = "Download/update offline repository"
            self.build = "Build"
            self.building = 'For now, you can sit back and relax.\nTechnical information about the assembly process:'
            self.failed_to_create_dir = "Failed to create directory. Returning to default. Error:"
            self.empty_cli = 'Error: Received empty command list, skipping.'
            self.executing_command = "Executing Command:"
            self.error_writing_to_stdin = "Error writing to stdin:"
            self.stdin_failed = "Command failed due to stdin error."
            self.error_reading_stdout = "Error reading stdout:"
            self.stderr = "stderr"
            self.error_reading_stderr = "Error reading stderr:"
            self.command_success = "Command finished successfully (Code:"
            self.command_failed = "Command failed (Code:"
            self.command_not_found = "Error: Command not found:"
            self.unexpected_error = "An unexpected error occurred during command execution:"
            self.executing_function = "Executing Function:"
            self.error_during_function_execution = "Error during function execution:"
            self.return_value = "Return value:"
            self.couldnt_return_value = "(Could not represent return value:"
            self.function = "Function"
            self.failed = "failed."
            self.succeed = "finished successfully."
            self.info = 'Information'
            self.check_console_log = "Check console log for details."
            self.error = "Error"
            self.build_interrupted = "Build process interrupted due to an error."
            self.build_complete_success = "Build process completed successfully!"
            self.kolbanidze_key_missing = "Kolbanidze PGP key not found or not trusted in pacman keyring. Attempting to add..."
            self.kolbanidze_key_add_fail = "Failed to add Kolbanidze PGP key."
            self.kolbanidze_key_ok = "Kolbanidze PGP key found and trusted."
            self.cloning = "Cloning/Updating repository:"
            self.clone_failed = "Failed to clone repository:"
            self.updating_offline_repo = "Updating offline package repository cache..."
            self.update_repo_failed = "Failed to update offline repository."
            self.creating_repo_db = "Creating offline repository database..."
            self.create_repo_db_failed = "Failed to create offline repository database."
            self.preparing_iso = "Preparing ISO build environment:"
            self.copying_offline_cache = "Copying offline repository cache to build environment..."
            self.copy_offline_cache_failed = "Failed to copy offline repository cache."
            self.configuring_pacman = "Configuring pacman.conf for build type:"
            self.configure_pacman_failed = "Failed to configure pacman.conf."
            self.collecting_py_packages = "Collecting Python packages for offline installation..."
            self.collect_py_fail = "Failed to collect Python packages."
            self.cleaning_dir = "Cleaning build directory:"
            self.clean_dir_ok = "Build directory cleaned:"
            self.clean_dir_fail_rm = "Failed to remove old build directory:"
            self.clean_dir_fail_mk = "Failed to create build directory:"
            self.success = "Success"
            self.command_failed_stdin = "Command failed due to stdin write error"
            # todo
            self.deps_success = 'Dependencies installed successfully'
            self.deps_err = 'Failed to install dependencies'
            self.deps_fnfe = 'Command not found during dependency installation. Is pacman or pip installed? Error:'
            self.exit = 'Exit'
            self.notification = "Notification"
            self.icon_not_found = 'Icon not found:'
            self.notify_gui_fail = 'Failed to create GUI notification'
            self.gui_error = 'GUI requested (-c not set), but customtkinter or Pillow is missing.'
            self.dir_not_found_at = 'directory not found at'
            self.attempting_to_create = 'Attempting to create'
            self.created_dir = 'Created directory'
            self.dir_fallback = 'Falling back to default directory'
            self.stopping_worker_thread = 'Stopping worker thread'
            self.scale_error = 'Scaling out of range'
            self.scale_invalid = 'Invalid scaling value selected'
            self.couldnt_load_image = 'Could not load image'
            self.checking_deps = 'Checking required system dependencies'
            self.deps_check_pass = 'System dependencies check passed'
            self.ping_fail = "Cannot check internet: 'ping' command not found"
            self.internet_check_error = 'Error checking internet connection'
            self.pacman_check_error = 'Failed to check pacman key'
            self.keyring_error = 'Keyring file does not exist'
            self.started = 'stated'
            self.failed_to_remove = 'Failed to remove existing directory for'
            self.at = 'at'
            self.exit_code = 'Exit code'
            self.offline_apps_update_success = 'Offline application sources updated successfully'
            self.offline_repo_fail = 'Failed to create offline repo directory'
            self.error_reading_offline_cache = 'Error reading offline cache directory'
            self.no_pkgs_found = 'No package files found in'
            self.offline_repo_update_success = 'Offline repository updated successfully'
            self.secux_installer_clone_failed = 'Failed to clone secux-installer into airootfs'
            self.offline_repo_miss = 'Offline repository source missing or incomplete.'
            self.py_collector_script_miss = 'Python collection script not found'
            self.pacman_config_not_found = 'Source pacman config not found'
            self.iso_not_found = 'Build failed: Expected ISO file not found at'
            self.failed_to_move = 'Failed to move'
            self.iso_build_success = 'ISO build successful'
            self.unknown_task = 'Unknown task type'
            self.error_reading_stream = 'Error reading stream'
            self.perm_denied = 'Permission denied executing command'
            self.terminating_hanging_process = 'Terminating hanging process'
            self.err_term = 'Error terminating process'
            self.skipping_bc_failed = 'Skipping function call due to previous error'
            self.worker_is_sleeping = 'Worker thread is not running. Cannot execute function.'
            self.rmtree_not_a_dir = 'Cannot rmtree: not a directory'
            self.failed_to_remove_dir = 'Failed to remove directory tree'
            self.failed_to_create_dir = 'Failed to create directory'
            self.cannot_remove_not_a_file = 'Cannot remove: not a file'
            self.failed_to_remove_file = 'Failed to remove file'
            self.failed_to_copy = 'Failed to copy'
            self.failed_to_chmod = 'Failed to chmod'
            self.failed_to_create_empty_file = 'Failed to create empty file'
            self.falling_back_to_cli = "[ERROR] GUI mode requested, but 'customtkinter' or 'Pillow' is not installed.\nInstall them using: pip install customtkinter Pillow\nOr use --install-all-dependencies flag.\nFalling back to CLI."
            self.unexpected_error_occurred = 'An unexpected error occurred'
            self.build_started = 'build'

        elif language == "ru":
            self.CURRENT_LANGUGAGE = "ru"
            self.arch_based = "Для сброки Secux Linux необходим Arch Linux или основанный на нем дистрибутив"
            self.not_installed_use = "не установлен. Для установки испльзуйте"
            self.missing_deps = 'При запуске были обнаружены отсутствующие зависимости. Для автоматической установки используйте флаг'
            self.root = 'Запускайте приложение только от суперпользователя'
            self.cli_on = 'Включен режим командной строки'
            self.releng_error = 'Директория releng не найдена. Создание образа Secux Linux невозможно'
            self.internet_error = "Для сборки Secux Linux необходимо стабильное подключеие к интернету"
            self.not_installed_deps = "Не установлены необходимые зависимости"
            self.offline_repo_autocreate = "Офлайн репозиторий будет автоматически создан"
            self.scaling_error = "Неверно указано мастабирование. Возврат к значению по умолчанию в 100%"
            self.scaling = "Масштабирование"
            self.workdir = "Рабочая папка"
            self.changedir = "Сменить папку"
            self.isoimagesfolder = "Папка для ISO образов"
            self.online_build = "Онлайн сборка"
            self.offline_build = "Офлайн сборка"
            self.online_label = "Минимальный ISO образ. Для установки\nсистемы потребуется подключение к интернету."
            self.offline_label = "ISO образ с всеми приложениями и \nпакетами, необходимыми для установки."
            self.update_apps = "Скачать/обновить приложения"
            self.offline_os = "Офлайн репозиторий содержит систему,\nвсе необходимые пакеты и зависимости\nдля установки Secux Linux."
            self.offline_repo = "Скачать/обновить офлайн репозиторий"
            self.build = "Собрать"
            self.building = "Пока можете откинуться на спинку стула.\nТехническая информация о процессе сборки:"
            self.failed_to_create_dir = "Не удалось создать каталог. Возврат к значениям по умолчанию. Ошибка:"
            self.empty_cli = 'Ошибка: Получен пустой список команд, пропуск.'
            self.executing_command = "Выполнение команды:"
            self.error_writing_to_stdin = "Ошибка записи в stdin:"
            self.stdin_failed = "Команда завершилась неудачно из-за ошибки stdin."
            self.error_reading_stdout = "Ошибка чтения из stdout:"
            self.stderr = "stderr"
            self.error_reading_stderr = "Ошибка чтения из stderr:"
            self.command_success = "Команда успешно завершена (Код:"
            self.command_failed = "Команда завершилась неудачно (Код:"
            self.command_not_found = "Ошибка: Команда не найдена:"
            self.unexpected_error = "Произошла непредвиденная ошибка во время выполнения команды:"
            self.executing_function = "Выполнение функции:"
            self.error_during_function_execution = "Ошибка во время выполнения функции:"
            self.return_value = "Возвращаемое значение:"
            self.couldnt_return_value = "(Не удалось представить возвращаемое значение:"
            self.function = "Функция"
            self.failed = "завершила свою работу с ошибкой."
            self.succeed = "завершила свою работу успешно."
            self.info = "Информация"
            self.check_console_log = 'Подробности смотрите в логе консоли'
            self.error = 'Ошибка'
            self.build_interrupted = "Процесс сборки прерван из-за ошибки."
            self.build_complete_success = "Процесс сборки успешно завершен!"
            self.kolbanidze_key_missing = "PGP ключ Kolbanidze не найден или не является доверенным в связке ключей pacman. Попытка добавить..."
            self.kolbanidze_key_add_fail = "Не удалось добавить PGP ключ Kolbanidze."
            self.kolbanidze_key_ok = "PGP ключ Kolbanidze найден и является доверенным."
            self.cloning = "Клонирование/Обновление репозитория:"
            self.clone_failed = "Не удалось клонировать репозиторий:"
            self.updating_offline_repo = "Обновление кеша офлайн репозитория пакетов..."
            self.update_repo_failed = "Не удалось обновить офлайн репозиторий."
            self.creating_repo_db = "Создание базы данных офлайн репозитория..."
            self.create_repo_db_failed = "Не удалось создать базу данных офлайн репозитория."
            self.preparing_iso = "Подготовка окружения для сборки ISO:"
            self.copying_offline_cache = "Копирование кеша офлайн репозитория в окружение сборки..."
            self.copy_offline_cache_failed = "Не удалось скопировать кеш офлайн репозитория."
            self.configuring_pacman = "Настройка pacman.conf для типа сборки:"
            self.configure_pacman_failed = "Не удалось настроить pacman.conf."
            self.collecting_py_packages = "Сбор Python пакетов для офлайн установки..."
            self.collect_py_fail = "Не удалось собрать Python пакеты."
            self.cleaning_dir = "Очистка папки сборки:"
            self.clean_dir_ok = "Папка сборки очищена:"
            self.clean_dir_fail_rm = "Не удалось удалить старую папку сборки:"
            self.clean_dir_fail_mk = "Не удалось создать папку сборки:"
            self.success = "Успех"
            self.command_failed_stdin = "Команда завершилась с ошибкой из-за ошибки записи в stdin"
            self.deps_success = 'Зависимости успешно установлены'
            # yo
            self.deps_err = 'Не удалось установить зависимости'
            self.deps_fnfe = 'Команда не найдена во время установки зависимости. Установлены ли pacman или pip? Ошибка:'
            self.exit = 'Выход'
            self.notification = "Уведомление"
            self.icon_not_found = 'Значок не найден:'
            self.notify_gui_fail = 'Не удалось создать уведомление GUI'
            self.gui_error = 'Запрошен GUI (-c не установлен), но customtkinter или Pillow отсутствуют.'
            self.dir_not_found_at = 'каталог не найден в'
            self.attempting_to_create = 'Попытка создания'
            self.created_dir = 'Создан каталог'
            self.dir_fallback = 'Возврат к каталогу по умолчанию'
            self.stopping_worker_thread = 'Остановка рабочего потока'
            self.scale_error = 'Масштабирование вне диапазона'
            self.scale_invalid = 'Выбрано недопустимое значение масштабирования'
            self.couldnt_load_image = 'Не удалось загрузить изображение'
            self.checking_deps = 'Проверка требуемых системных зависимостей'
            self.deps_check_pass = 'Проверка системных зависимостей пройдена'
            self.ping_fail = "Не удалось проверить интернет: команда 'ping' не найдена"
            self.internet_check_error = 'Ошибка проверки интернет-подключения'
            self.pacman_check_error = 'Не удалось проверить ключ pacman'
            self.keyring_error = 'Файл связки ключей не существует'
            self.started = 'запущена'
            self.failed_to_remove = 'Не удалось удалить существующий каталог для'
            self.at = 'в'
            self.exit_code = 'Код выхода'
            self.offline_apps_update_success = 'Исходные файлы автономного приложения успешно обновлены'
            self.offline_repo_fail = 'Не удалось создать каталог автономного репозитория'
            self.error_reading_offline_cache = 'Ошибка чтения каталога автономного кэша'
            self.no_pkgs_found = 'Файлы пакета не найдены в'
            self.offline_repo_update_success = 'Автономный репозиторий успешно обновлен'
            self.secux_installer_clone_failed = 'Не удалось клонировать secux-installer в airootfs'
            self.offline_repo_miss = 'Исходный код автономного репозитория отсутствует или неполный.'
            self.py_collector_script_miss = 'Скрипт сбора Python не найден'
            self.pacman_config_not_found = 'Исходная конфигурация pacman не найдена'
            self.iso_not_found = 'Сборка не удалась: ожидаемый файл ISO не найден по адресу'
            self.failed_to_move = 'Не удалось переместить'
            self.iso_build_success = 'Сборка ISO выполнена успешно'
            self.unknown_task = 'Неизвестный тип задачи'
            self.error_reading_stream = 'Ошибка чтения потока'
            self.perm_denied = 'Отказано в доступе при выполнении команды'
            self.terminating_hanging_process = 'Завершение зависшего процесса'
            self.err_term = 'Ошибка завершения процесса'
            self.skipping_bc_failed = 'Пропуск вызова функции из-за предыдущей ошибки'
            self.worker_is_sleeping = 'Рабочий поток не запущен. Невозможно выполнить функцию.'
            self.rmtree_not_a_dir = 'Невозможно rmtree: не каталог'
            self.failed_to_remove_dir = 'Не удалось удалить дерево каталогов'
            self.failed_to_create_dir = 'Не удалось создать каталог'
            self.cannot_remove_not_a_file = 'Не удалось удалить: не файл'
            self.failed_to_remove_file = 'Не удалось удалить файл'
            self.failed_to_copy = 'Не удалось скопировать'
            self.failed_to_chmod = 'Не удалось chmod'
            self.failed_to_create_empty_file = 'Не удалось создать пустой файл'
            self.falling_back_to_cli = "[ERROR] Запрошен режим GUI, но 'customtkinter' или 'Pillow' не установлены.\nУстановить их с помощью: pip install customtkinter Pillow\nИли используйте флаг --install-all-dependencies.\nОткат к CLI."
            self.unexpected_error_occurred = 'Произошла непредвиденная ошибка'
            self.build_started = 'сборка'
