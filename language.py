class Locale:
    def __init__(self, language: str) -> None:
        if language == "en":
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


        elif language == "ru":
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
