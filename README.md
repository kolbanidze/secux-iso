# Secux Linux Builder

В этом репозитории находятся исходники Secux Linux Builder, необходимого для сборки ISO образов Secux Linux. 

<p align="center">
    <img src="https://raw.githubusercontent.com/kolbanidze/secux-iso/refs/heads/main/welcome.png" width=384>
</p>

## Запуск

Для запуска сборщика: `python main.py`

После запуска установки оно перезапустится в режиме `worker`. Для получения root доступа используется pkexec.

### Техническая информация
*   Интерфейс написан на Python с использованием GTK 4 и Libadwaita.
*   Взаимодействие с диском и системой осуществляется через `subprocess` от root. 
*   Зависимости:
    *   `python-gobject`
    *   `libadwaita`
    *   `gtk4`
    *   `archiso`
    *   `rsync`
    *   `pacman-contrib`
    *   `pacman`
    * Дистирубтив на основе Arch Linux (например Secux Linux)