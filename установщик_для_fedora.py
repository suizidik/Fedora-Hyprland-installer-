#!/usr/bin/env python3
# fedora_software_installer.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import os
import sys

class FedoraSoftwareInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fedora Software Installer")
        self.root.geometry("800x750")
        self.root.resizable(True, True)

        # Переменные для языка
        self.language = tk.StringVar(value="ru")
        self.translations = {
            "ru": self.get_russian_text(),
            "en": self.get_english_text()
        }

        self.setup_ui()
        self.update_language()

    def get_russian_text(self):
        return {
            "title": "Установщик программ для Fedora",
            "select_software": "Выберите программы для установки:",
            "select_de": "Выберите окружение рабочего стола:",
            "install_btn": "Установить выбранное",
            "progress": "Идет установка...",
            "complete": "Установка завершена!",
            "error": "Ошибка",
            "help_title": "Справка",
            "required_tooltip": "Обязательная программа",
            "optional_tooltip": "Опциональная программа",
            "warning_text": "ПОЖАЛУЙСТА ПРОЧИТАЙТЕ ИНСТРУКЦИЮ ПО УСТАНОВКЕ В СПРАВКЕ",
            "help_text": """СПРАВКА ПО УСТАНОВЩИКУ:

⚠️ ВАЖНОЕ ПРЕДУПРЕЖДЕНИЕ:
Владельцы ноутбуков и жители городов с периодическим отключением света - внимание!
Автор не несёт ответственности за повреждение системы.

Для ноутбуков: убедитесь что ноутбук полностью заряжен!
Время установки длится от 1 до 2 часов!!!
Если вы не уверены в батарее - поставьте ноутбук на зарядку.

ОКРУЖЕНИЯ РАБОЧЕГО СТОЛА:

🖼️ Hyprland (Современный Wayland композитор)
- Очень настраиваемый, красивый, с анимациями
- МНОГО горячих клавиш - может быть сложно для новичков
- Рекомендуется опытным пользователям
- Не похож на Windows/MacOS

🎯 Горячие клавиши Hyprland:
Super + 1,2,3,4,5,6 - переключение рабочих столов
Super + C - открыть терминал
Super + F - открыть браузер
Super + V - открыть VS Code
Super + Q - закрыть окно
Super + D - запустить приложения (rofi)
Super + Enter - терминал
Super + T - плавающий режим
Super + Shift + Q - принудительно закрыть

🪟 KDE Plasma (Похож на Windows)
- Очень похож на Windows - легко для новичков
- Мощный и настраиваемый
- Много эффектов и настроек
- Идеален для перехода с Windows

🌀 GNOME (Современный и минималистичный)
- Чистый и простой интерфейс
- Похож на MacOS
- Хорошие жесты трекпада
- Стандарт для Fedora

⚡ XFCE (Легкий и быстрый)
- Малотребовательный к ресурсам
- Подходит для старых компьютеров
- Простой в использовании
- Стабильный и надежный

ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ:
- Пункт "ROG" в установщике Hyprland ТОЛЬКО для ноутбуков ASUS ROG!
  Если у вас не ROG ноутбук - НЕ ВКЛЮЧАЙТЕ эту опцию!

- После установки Hyprland появится программа-установщик
- Везде нажимайте Next пока не появится выбор способа установки
- ВЫБЕРИТЕ "ВСЕ ФАЙЛЫ" а не частичное в двух категориях
- Это последняя отметка перед началом установки

ОБЯЗАТЕЛЬНЫЕ ПРОГРАММЫ:
- RPM Fusion, Flatpak - необходимы для работы системы
- Драйвера NVIDIA - если у вас видеокарта NVIDIA
- Нельзя отключить

ПРОЦЕСС УСТАНОВКИ:
1. Выберите окружение (опционально)
2. Выберите нужные программы
3. Нажмите 'Установить выбранное'
4. Дождитесь завершения
5. Для Hyprland: следуйте инструкциям выше

В процессе установки может потребоваться ввод пароля."""
        }

    def get_english_text(self):
        return {
            "title": "Fedora Software Installer", 
            "select_software": "Select software to install:",
            "select_de": "Select desktop environment:",
            "install_btn": "Install Selected",
            "progress": "Installation in progress...",
            "complete": "Installation complete!",
            "error": "Error",
            "help_title": "Help",
            "required_tooltip": "Required program",
            "optional_tooltip": "Optional program",
            "warning_text": "PLEASE READ THE INSTALLATION INSTRUCTIONS IN HELP",
            "help_text": """INSTALLER HELP:

⚠️ IMPORTANT WARNING:
Laptop owners and residents of areas with periodic power outages - attention!
The author is not responsible for system damage.

For laptops: make sure the laptop is fully charged!
Installation time takes from 1 to 2 hours!!!
If you are unsure about the battery - plug in the laptop.

DESKTOP ENVIRONMENTS:

🖼️ Hyprland (Modern Wayland Compositor)
- Highly customizable, beautiful, with animations
- MANY hotkeys - can be difficult for beginners
- Recommended for experienced users
- Not similar to Windows/MacOS

🎯 Hyprland Hotkeys:
Super + 1,2,3,4,5,6 - switch workspaces
Super + C - open terminal
Super + F - open browser
Super + V - open VS Code
Super + Q - close window
Super + D - launch applications (rofi)
Super + Enter - terminal
Super + T - toggle floating
Super + Shift + Q - force close

🪟 KDE Plasma (Windows-like)
- Very similar to Windows - easy for beginners
- Powerful and customizable
- Many effects and settings
- Ideal for switching from Windows

🌀 GNOME (Modern and Minimalistic)
- Clean and simple interface
- Similar to MacOS
- Good trackpad gestures
- Default for Fedora

⚡ XFCE (Lightweight and Fast)
- Low resource requirements
- Suitable for old computers
- Easy to use
- Stable and reliable

IMPORTANT WARNINGS:
- "ROG" option in Hyprland installer ONLY for ASUS ROG laptops!
  If you don't have ROG laptop - DO NOT ENABLE this option!

- After Hyprland installation, an installer program will appear
- Click Next everywhere until installation method selection
- SELECT "ALL FILES" not partial in both categories
- This is the last mark before installation starts

REQUIRED PROGRAMS:
- RPM Fusion, Flatpak - essential for system operation
- NVIDIA drivers - if you have NVIDIA graphics card
- Cannot be disabled

INSTALLATION PROCESS:
1. Select environment (optional)
2. Select desired programs
3. Click 'Install Selected'
4. Wait for completion
5. For Hyprland: follow instructions above

Password may be required during installation."""
        }

    def setup_ui(self):
        # Верхняя панель с выбором языка
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill='x', padx=10, pady=5)

        # Кнопка помощи
        self.help_btn = ttk.Button(top_frame, text="?", width=2, command=self.show_help)
        self.help_btn.pack(side='left')

        # Выбор языка
        lang_frame = ttk.Frame(top_frame)
        lang_frame.pack(side='right')

        ttk.Label(lang_frame, text="Language:").pack(side='left', padx=5)
        ttk.Radiobutton(lang_frame, text="Русский", variable=self.language, 
                       value="ru", command=self.update_language).pack(side='left', padx=5)
        ttk.Radiobutton(lang_frame, text="English", variable=self.language,
                       value="en", command=self.update_language).pack(side='left', padx=5)

        # Предупреждающая надпись
        self.warning_label = tk.Label(self.root, text="", font=('Arial', 10), 
                                    fg='red', bg='lightyellow')
        self.warning_label.pack(fill='x', padx=10, pady=5)

        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Заголовок
        self.title_label = ttk.Label(main_frame, text="", font=('Arial', 12, 'bold'))
        self.title_label.pack(pady=(0, 10))

        # Фрейм для выбора окружения
        de_frame = ttk.LabelFrame(main_frame, text="")
        de_frame.pack(fill='x', pady=(0, 10))

        self.de_label = ttk.Label(de_frame, text="")
        self.de_label.pack(anchor='w', padx=5, pady=5)

        # Переменные для окружений
        self.de_vars = {
            "hyprland": tk.BooleanVar(),
            "gnome": tk.BooleanVar(),
            "kde": tk.BooleanVar(),
            "xfce": tk.BooleanVar()
        }

        de_inner_frame = ttk.Frame(de_frame)
        de_inner_frame.pack(fill='x', padx=10, pady=5)

        # Чекбоксы с описаниями
        ttk.Checkbutton(de_inner_frame, text="Hyprland (Modern Wayland)", 
                       variable=self.de_vars["hyprland"]).pack(anchor='w', padx=5, pady=2)
        ttk.Label(de_inner_frame, text="Много горячих клавиш, для опытных", 
                 font=('Arial', 8), foreground='gray').pack(anchor='w', padx=25)

        ttk.Checkbutton(de_inner_frame, text="KDE Plasma (Windows-like)", 
                       variable=self.de_vars["kde"]).pack(anchor='w', padx=5, pady=2)
        ttk.Label(de_inner_frame, text="Похож на Windows, для новичков", 
                 font=('Arial', 8), foreground='gray').pack(anchor='w', padx=25)

        ttk.Checkbutton(de_inner_frame, text="GNOME (Modern)", 
                       variable=self.de_vars["gnome"]).pack(anchor='w', padx=5, pady=2)
        ttk.Label(de_inner_frame, text="Минималистичный, похож на MacOS", 
                 font=('Arial', 8), foreground='gray').pack(anchor='w', padx=25)

        ttk.Checkbutton(de_inner_frame, text="XFCE (Lightweight)", 
                       variable=self.de_vars["xfce"]).pack(anchor='w', padx=5, pady=2)
        ttk.Label(de_inner_frame, text="Легкий и быстрый, для старых ПК", 
                 font=('Arial', 8), foreground='gray').pack(anchor='w', padx=25)

        # Фрейм для списка программ
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill='both', expand=True)

        # Создаем Treeview для красивого списка
        columns = ('selected', 'name', 'type')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='tree headings', height=18)

        # Настраиваем колонки
        self.tree.column('#0', width=0, stretch=False)
        self.tree.column('selected', width=80, anchor='center')
        self.tree.column('name', width=450, anchor='w')
        self.tree.column('type', width=150, anchor='w')

        # Заголовки
        self.tree.heading('selected', text='')
        self.tree.heading('name', text='')
        self.tree.heading('type', text='')

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Данные о программах
        self.software_list = [
            # === ОБЯЗАТЕЛЬНЫЕ СИСТЕМНЫЕ ===
            {"id": "rpmfusion_free", "name": "RPM Fusion Free", "required": True, "type": "repository", "dnf_cmd": ["dnf", "install", "-y", "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"]},
            {"id": "rpmfusion_nonfree", "name": "RPM Fusion Non-Free", "required": True, "type": "repository", "dnf_cmd": ["dnf", "install", "-y", "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"]},
            {"id": "flatpak", "name": "Flatpak", "required": True, "type": "package", "dnf_cmd": ["dnf", "install", "-y", "flatpak"]},
            {"id": "flathub", "name": "Flathub Repository", "required": True, "type": "repository", "dnf_cmd": ["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"]},

            # === ДРАЙВЕРА ===
            {"id": "nvidia_drivers", "name": "NVIDIA Drivers", "required": False, "type": "drivers", "dnf_cmd": ["dnf", "install", "-y", "akmod-nvidia", "xorg-x11-drv-nvidia-cuda"]},
            {"id": "media_codecs", "name": "Media Codecs", "required": False, "type": "package", "dnf_cmd": ["dnf", "groupupdate", "-y", "--with-optional", "Multimedia"]},

            # === БРАУЗЕРЫ ===
            {"id": "firefox", "name": "Firefox", "required": False, "type": "browser", "dnf_cmd": ["dnf", "install", "-y", "firefox"]},
            {"id": "chrome", "name": "Google Chrome", "required": False, "type": "browser", "dnf_cmd": ["dnf", "config-manager", "--set-enabled", "google-chrome"]},
            {"id": "chromium", "name": "Chromium", "required": False, "type": "browser", "dnf_cmd": ["dnf", "install", "-y", "chromium"]},
            {"id": "opera", "name": "Opera", "required": False, "type": "browser", "dnf_cmd": ["dnf", "config-manager", "--set-enabled", "opera"]},
            {"id": "brave", "name": "Brave Browser", "required": False, "type": "browser", "dnf_cmd": ["dnf", "install", "-y", "brave-browser"]},

            # === РАЗРАБОТКА ===
            {"id": "vscode", "name": "Visual Studio Code", "required": False, "type": "development", "dnf_cmd": ["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc", "&&", "sh", "-c", "echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo", "&&", "dnf", "install", "-y", "code"]},
            {"id": "git", "name": "Git", "required": False, "type": "development", "dnf_cmd": ["dnf", "install", "-y", "git"]},
            {"id": "python", "name": "Python Development", "required": False, "type": "development", "dnf_cmd": ["dnf", "install", "-y", "python3", "python3-devel", "python3-pip"]},

            # === МЕССЕНДЖЕРЫ ===
            {"id": "telegram", "name": "Telegram", "required": False, "type": "messenger", "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.telegram.desktop"]},
            {"id": "discord", "name": "Discord", "required": False, "type": "messenger", "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.discordapp.Discord"]},
            {"id": "signal", "name": "Signal", "required": False, "type": "messenger", "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.signal.Signal"]},

            # === МУЛЬТИМЕДИА ===
            {"id": "vlc", "name": "VLC Media Player", "required": False, "type": "media", "dnf_cmd": ["dnf", "install", "-y", "vlc"]},
            {"id": "spotify", "name": "Spotify", "required": False, "type": "media", "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.spotify.Client"]},
            {"id": "obs", "name": "OBS Studio", "required": False, "type": "media", "dnf_cmd": ["dnf", "install", "-y", "obs-studio"]},
            {"id": "gimp", "name": "GIMP", "required": False, "type": "graphics", "dnf_cmd": ["dnf", "install", "-y", "gimp"]},
            {"id": "kdenlive", "name": "Kdenlive", "required": False, "type": "media", "dnf_cmd": ["dnf", "install", "-y", "kdenlive"]},

            # === ОФИС ===
            {"id": "libreoffice", "name": "LibreOffice", "required": False, "type": "office", "dnf_cmd": ["dnf", "install", "-y", "libreoffice"]},

            # === СИСТЕМНЫЕ УТИЛИТЫ ===
            {"id": "wine", "name": "Wine", "required": False, "type": "compatibility", "dnf_cmd": ["dnf", "install", "-y", "wine"]},
            {"id": "steam", "name": "Steam", "required": False, "type": "games", "dnf_cmd": ["dnf", "install", "-y", "steam"]},
            {"id": "gparted", "name": "GParted", "required": False, "type": "system", "dnf_cmd": ["dnf", "install", "-y", "gparted"]},
            {"id": "htop", "name": "htop", "required": False, "type": "system", "dnf_cmd": ["dnf", "install", "-y", "htop"]},
            {"id": "neofetch", "name": "neofetch", "required": False, "type": "system", "dnf_cmd": ["dnf", "install", "-y", "neofetch"]},
        ]

        # Заполняем список программ
        self.populate_software_list()

        # Привязываем обработчик кликов
        self.tree.bind('<Button-1>', self.on_tree_click)

        # Кнопка установки
        self.install_btn = ttk.Button(main_frame, text="", command=self.start_installation)
        self.install_btn.pack(pady=10)

        # Прогресс бар
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')

        # Текстовое поле для логов
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10, state='disabled')
        self.log_text.pack(fill='both', expand=False, pady=5)

    def populate_software_list(self):
        """Заполняем список программ"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for software in self.software_list:
            status = "✓" if software.get('selected', software['required']) else "☐"
            tags = ('required',) if software['required'] else ('optional',)
            
            if software['required']:
                software['selected'] = True

            item = self.tree.insert('', 'end', values=(
                status, 
                software['name'],
                software['type']
            ), tags=tags)

            # Сохраняем ID программы в item
            self.tree.set(item, '#id', software['id'])

    def on_tree_click(self, event):
        """Обработчик кликов по дереву"""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if item and column == '#1':  # Колонка с галочкой
            software_id = self.tree.set(item, '#id')
            software = next((s for s in self.software_list if s['id'] == software_id), None)

            if software and not software['required']:
                # Переключаем состояние
                software['selected'] = not software.get('selected', False)
                status = "✓" if software['selected'] else "☐"
                self.tree.set(item, 'selected', status)

    def update_language(self):
        """Обновляем интерфейс при смене языка"""
        lang = self.language.get()
        texts = self.translations[lang]

        self.root.title(texts["title"])
        self.title_label.config(text=texts["select_software"])
        self.install_btn.config(text=texts["install_btn"])
        self.de_label.config(text=texts["select_de"])
        self.warning_label.config(text=texts["warning_text"])

        # Обновляем заголовки таблицы
        self.tree.heading('name', text='Program' if lang == 'en' else 'Программа')
        self.tree.heading('type', text='Type' if lang == 'en' else 'Тип')

        # Обновляем описания окружений
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Frame):
                        for desc_label in child.winfo_children():
                            if isinstance(desc_label, ttk.Label) and desc_label.cget('text'):
                                current_text = desc_label.cget('text')
                                # Обновляем описания на основе текущего текста
                                if "Много горячих клавиш" in current_text:
                                    desc_label.config(text="Many hotkeys, for experienced" if lang == "en" else "Много горячих клавиш, для опытных")
                                elif "Похож на Windows" in current_text:
                                    desc_label.config(text="Windows-like, for beginners" if lang == "en" else "Похож на Windows, для новичков")
                                elif "Минималистичный" in current_text:
                                    desc_label.config(text="Minimalistic, MacOS-like" if lang == "en" else "Минималистичный, похож на MacOS")
                                elif "Легкий и быстрый" in current_text:
                                    desc_label.config(text="Lightweight and fast, for old PCs" if lang == "en" else "Легкий и быстрый, для старых ПК")

    def show_help(self):
        """Показываем окно помощи"""
        lang = self.language.get()
        texts = self.translations[lang]

        help_window = tk.Toplevel(self.root)
        help_window.title(texts["help_title"])
        help_window.geometry("650x550")
        help_window.resizable(False, False)

        help_text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD)
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        help_text.insert('1.0',
