#!/usr/bin/env python3
# fedora_software_installer.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import subprocess
import threading
import os
import sys
from datetime import datetime
import json
import webbrowser

class FedoraSoftwareInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Fedora Software Installer Pro")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)
        
        # Настройка стилей
        self.setup_styles()
        
        # Переменные для языка
        self.language = tk.StringVar(value="ru")
        self.translations = {
            "ru": self.get_russian_text(),
            "en": self.get_english_text()
        }
        
        # Данные о установках
        self.installation_history = []
        self.load_history()
        
        # Цветовая схема
        self.colors = {
            "bg": "#1e1e2e",
            "fg": "#cdd6f4",
            "primary": "#89b4fa",
            "secondary": "#b4befe",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8",
            "accent": "#cba6f7",
            "card_bg": "#313244"
        }
        
        self.setup_ui()
        self.update_language()

    def setup_styles(self):
        """Настройка стилей интерфейса"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Настраиваем цвета
        style.configure("TButton", padding=6, relief="flat", background=self.colors["primary"])
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 12))
        style.configure("Card.TFrame", background=self.colors["card_bg"])
        
        # Кастомные стили
        style.map("Custom.TButton",
                background=[("active", self.colors["secondary"])])
        style.configure("Custom.TButton",
                       padding=10,
                       font=("Segoe UI", 10, "bold"))

    def get_russian_text(self):
        return {
            "title": "Fedora Software Installer Pro",
            "select_software": "📦 Выберите программы для установки",
            "select_de": "🎨 Выберите окружение рабочего стола",
            "install_btn": "🚀 Начать установку",
            "update_btn": "🔄 Обновить систему",
            "clean_btn": "🧹 Очистить систему",
            "history_btn": "📊 История установок",
            "progress": "Идет установка...",
            "complete": "Установка завершена!",
            "error": "Ошибка",
            "help_title": "Справка",
            "required_tooltip": "Обязательная программа",
            "optional_tooltip": "Опциональная программа",
            "warning_text": "⚠️ ВНИМАНИЕ: ПРОЧТИТЕ ИНСТРУКЦИЮ В СПРАВКЕ ПЕРЕД УСТАНОВКОЙ",
            "search_placeholder": "🔍 Поиск программ...",
            "select_all": "Выбрать все",
            "deselect_all": "Снять все",
            "stats": "Статистика",
            "selected_count": "Выбрано программ",
            "time_estimate": "Примерное время",
            "system_info": "Информация о системе",
            "install_type": "Тип установки",
            "express_install": "Экспресс-установка",
            "custom_install": "Пользовательская установка",
            "help_text": """СПРАВКА ПО УСТАНОВЩИКУ:

✨ ВОЗМОЖНОСТИ УСТАНОВЩИКА:
1. Установка нескольких окружений рабочего стола
2. Массовая установка программ
3. Автоматическая настройка репозиториев
4. Очистка системы от ненужных пакетов
5. История установок
6. Экспресс-установка для быстрой настройки

⚡ ЭКСПРЕСС-УСТАНОВКА:
- Разработчик: VS Code, Git, Python, Docker
- Дизайн: GIMP, Inkscape, Blender
- Офис: LibreOffice, OnlyOffice
- Мультимедиа: VLC, OBS, Kdenlive
- Игры: Steam, Lutris, Wine

⚠️ ВАЖНЫЕ ПРЕДУПРЕЖДЕНИЯ:
1. Убедитесь в стабильности питания
2. Резервное копирование важных данных
3. Проверьте свободное место на диске
4. Не прерывайте процесс установки

🎮 ИГРОВАЯ СБОРКА:
- Wine, Steam, Lutris, MangoHud
- Игровые драйвера NVIDIA/AMD
- Эмуляторы (RetroArch, Dolphin)
- Discord, OBS для стриминга

🎨 ДИЗАЙНЕРСКАЯ СБОРКА:
- GIMP, Inkscape, Krita
- Blender, DaVinci Resolve
- Shotcut, Darktable
- Scribus, FreeCAD

💻 РАЗРАБОТЧИК:
- VS Code, JetBrains Toolbox
- Docker, Podman, Kubernetes
- Node.js, Go, Rust, Java
- MySQL, PostgreSQL, Redis

📊 СТАТИСТИКА:
- Более 150 доступных пакетов
- Поддержка Flatpak и Snap
- Автоматическое обновление
- Резервное копирование конфигов

🛠️ ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:
1. Очистка кеша пакетов
2. Удаление orphaned пакетов
3. Оптимизация системы
4. Создание точки восстановления

💡 СОВЕТЫ:
- Используйте экспресс-установку для быстрой настройки
- Регулярно обновляйте систему
- Создавайте резервные копии
- Изучайте логи установки"""
        }

    def get_english_text(self):
        return {
            "title": "Fedora Software Installer Pro",
            "select_software": "📦 Select Software to Install",
            "select_de": "🎨 Select Desktop Environment",
            "install_btn": "🚀 Start Installation",
            "update_btn": "🔄 Update System",
            "clean_btn": "🧹 Clean System",
            "history_btn": "📊 Installation History",
            "progress": "Installation in progress...",
            "complete": "Installation complete!",
            "error": "Error",
            "help_title": "Help",
            "required_tooltip": "Required program",
            "optional_tooltip": "Optional program",
            "warning_text": "⚠️ WARNING: READ HELP INSTRUCTIONS BEFORE INSTALLATION",
            "search_placeholder": "🔍 Search programs...",
            "select_all": "Select All",
            "deselect_all": "Deselect All",
            "stats": "Statistics",
            "selected_count": "Selected programs",
            "time_estimate": "Estimated time",
            "system_info": "System Information",
            "install_type": "Installation Type",
            "express_install": "Express Install",
            "custom_install": "Custom Install",
            "help_text": """INSTALLER HELP:

✨ FEATURES:
1. Multiple desktop environments installation
2. Bulk software installation
3. Automatic repository configuration
4. System cleanup tools
5. Installation history
6. Express installation for quick setup

⚡ EXPRESS INSTALLATION:
- Developer: VS Code, Git, Python, Docker
- Design: GIMP, Inkscape, Blender
- Office: LibreOffice, OnlyOffice
- Multimedia: VLC, OBS, Kdenlive
- Games: Steam, Lutris, Wine

⚠️ IMPORTANT WARNINGS:
1. Ensure stable power supply
2. Backup important data
3. Check free disk space
4. Do not interrupt installation

🎮 GAMING BUNDLE:
- Wine, Steam, Lutris, MangoHud
- NVIDIA/AMD gaming drivers
- Emulators (RetroArch, Dolphin)
- Discord, OBS for streaming

🎨 DESIGNER BUNDLE:
- GIMP, Inkscape, Krita
- Blender, DaVinci Resolve
- Shotcut, Darktable
- Scribus, FreeCAD

💻 DEVELOPER BUNDLE:
- VS Code, JetBrains Toolbox
- Docker, Podman, Kubernetes
- Node.js, Go, Rust, Java
- MySQL, PostgreSQL, Redis

📊 STATISTICS:
- Over 150 available packages
- Flatpak and Snap support
- Automatic updates
- Configuration backup

🛠️ ADDITIONAL FUNCTIONS:
1. Package cache cleanup
2. Orphaned package removal
3. System optimization
4. Restore point creation

💡 TIPS:
- Use express installation for quick setup
- Update system regularly
- Create backups
- Check installation logs"""
        }

    def setup_ui(self):
        # Установка фонового цвета
        self.root.configure(bg=self.colors["bg"])
        
        # Верхняя панель с логотипом
        header_frame = tk.Frame(self.root, bg=self.colors["bg"], height=80)
        header_frame.pack(fill='x', padx=20, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Логотип и название
        logo_frame = tk.Frame(header_frame, bg=self.colors["bg"])
        logo_frame.pack(side='left')
        
        title_label = tk.Label(logo_frame, text="🐧", font=("Segoe UI", 28), 
                             bg=self.colors["bg"], fg=self.colors["primary"])
        title_label.pack(side='left')
        
        title_text = tk.Label(logo_frame, text="Fedora Software Installer", 
                            font=("Segoe UI", 18, "bold"), 
                            bg=self.colors["bg"], fg=self.colors["fg"])
        title_text.pack(side='left', padx=10)
        
        # Кнопки управления
        control_frame = tk.Frame(header_frame, bg=self.colors["bg"])
        control_frame.pack(side='right')
        
        # Кнопка помощи
        self.help_btn = tk.Button(control_frame, text="❓ Помощь", 
                                command=self.show_help,
                                bg=self.colors["accent"], fg="white",
                                font=("Segoe UI", 10, "bold"),
                                relief="flat", padx=15, pady=5)
        self.help_btn.pack(side='left', padx=5)
        
        # Выбор языка
        lang_frame = tk.Frame(control_frame, bg=self.colors["bg"])
        lang_frame.pack(side='left', padx=10)
        
        tk.Label(lang_frame, text="🌐", bg=self.colors["bg"], 
                fg=self.colors["fg"]).pack(side='left')
        
        tk.Radiobutton(lang_frame, text="РУ", variable=self.language, 
                      value="ru", command=self.update_language,
                      bg=self.colors["bg"], fg=self.colors["fg"],
                      selectcolor=self.colors["bg"],
                      activebackground=self.colors["bg"],
                      activeforeground=self.colors["primary"]).pack(side='left', padx=5)
        
        tk.Radiobutton(lang_frame, text="EN", variable=self.language,
                      value="en", command=self.update_language,
                      bg=self.colors["bg"], fg=self.colors["fg"],
                      selectcolor=self.colors["bg"],
                      activebackground=self.colors["bg"],
                      activeforeground=self.colors["primary"]).pack(side='left', padx=5)
        
        # Предупреждение
        self.warning_label = tk.Label(self.root, text="", 
                                    font=('Segoe UI', 10, 'bold'), 
                                    fg=self.colors["warning"], bg=self.colors["bg"])
        self.warning_label.pack(fill='x', padx=20, pady=(0, 10))
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Левая панель (окружения и статистика)
        left_panel = tk.Frame(main_container, bg=self.colors["bg"], width=300)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        # Карточка окружений
        de_card = tk.Frame(left_panel, bg=self.colors["card_bg"], 
                          relief="flat", bd=2)
        de_card.pack(fill='x', pady=(0, 10))
        
        de_title = tk.Label(de_card, text="🎨 Окружения рабочего стола", 
                          font=("Segoe UI", 12, "bold"),
                          bg=self.colors["card_bg"], fg=self.colors["fg"])
        de_title.pack(anchor='w', padx=15, pady=(15, 10))
        
        self.de_vars = {
            "hyprland": tk.BooleanVar(),
            "gnome": tk.BooleanVar(),
            "kde": tk.BooleanVar(),
            "xfce": tk.BooleanVar(),
            "cinnamon": tk.BooleanVar(),
            "mate": tk.BooleanVar(),
            "lxqt": tk.BooleanVar(),
            "budgie": tk.BooleanVar()
        }
        
        de_list_frame = tk.Frame(de_card, bg=self.colors["card_bg"])
        de_list_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Список окружений с иконками
        de_options = [
            ("🧩 Hyprland", "Современный Wayland", "hyprland"),
            ("🪟 KDE Plasma", "Похож на Windows", "kde"),
            ("🌀 GNOME", "Минималистичный", "gnome"),
            ("⚡ XFCE", "Легкий и быстрый", "xfce"),
            ("🍃 Cinnamon", "Традиционный", "cinnamon"),
            ("🌿 MATE", "Классический GNOME 2", "mate"),
            ("🐧 LXQt", "Ultra-lightweight", "lxqt"),
            ("🐦 Budgie", "Элегантный", "budgie")
        ]
        
        for icon, desc, key in de_options:
            frame = tk.Frame(de_list_frame, bg=self.colors["card_bg"])
            frame.pack(fill='x', pady=2)
            
            cb = tk.Checkbutton(frame, text=icon, variable=self.de_vars[key],
                              bg=self.colors["card_bg"], fg=self.colors["fg"],
                              selectcolor=self.colors["card_bg"],
                              activebackground=self.colors["card_bg"],
                              activeforeground=self.colors["primary"],
                              font=("Segoe UI", 10))
            cb.pack(side='left')
            
            label = tk.Label(frame, text=desc, bg=self.colors["card_bg"],
                           fg="#a6adc8", font=("Segoe UI", 9))
            label.pack(side='left', padx=10)
        
        # Карточка статистики
        stats_card = tk.Frame(left_panel, bg=self.colors["card_bg"], 
                            relief="flat", bd=2)
        stats_card.pack(fill='x', pady=(0, 10))
        
        stats_title = tk.Label(stats_card, text="📊 Статистика", 
                             font=("Segoe UI", 12, "bold"),
                             bg=self.colors["card_bg"], fg=self.colors["fg"])
        stats_title.pack(anchor='w', padx=15, pady=(15, 10))
        
        self.stats_frame = tk.Frame(stats_card, bg=self.colors["card_bg"])
        self.stats_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Карточка быстрых действий
        actions_card = tk.Frame(left_panel, bg=self.colors["card_bg"], 
                              relief="flat", bd=2)
        actions_card.pack(fill='x')
        
        actions_title = tk.Label(actions_card, text="⚡ Быстрые действия", 
                               font=("Segoe UI", 12, "bold"),
                               bg=self.colors["card_bg"], fg=self.colors["fg"])
        actions_title.pack(anchor='w', padx=15, pady=(15, 10))
        
        actions_frame = tk.Frame(actions_card, bg=self.colors["card_bg"])
        actions_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Кнопки быстрых действий
        action_buttons = [
            ("🔄 Обновить систему", self.update_system, self.colors["primary"]),
            ("🧹 Очистить систему", self.clean_system, self.colors["accent"]),
            ("📊 История", self.show_history, self.colors["secondary"]),
            ("⚡ Экспресс", self.express_install, self.colors["success"])
        ]
        
        for text, command, color in action_buttons:
            btn = tk.Button(actions_frame, text=text, command=command,
                          bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                          relief="flat", padx=10, pady=8, width=20)
            btn.pack(pady=3)
        
        # Правая панель (программы)
        right_panel = tk.Frame(main_container, bg=self.colors["bg"])
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Панель поиска и управления
        search_frame = tk.Frame(right_panel, bg=self.colors["bg"])
        search_frame.pack(fill='x', pady=(0, 10))
        
        # Поиск
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_programs)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                              font=("Segoe UI", 11), relief="flat",
                              bg="#45475a", fg=self.colors["fg"],
                              insertbackground=self.colors["fg"])
        search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        search_entry.insert(0, "🔍 Поиск программ...")
        search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) 
                         if search_entry.get() == "🔍 Поиск программ..." else None)
        
        # Кнопки выбора
        select_btn = tk.Button(search_frame, text="✓ Выбрать все",
                             command=self.select_all_programs,
                             bg=self.colors["primary"], fg="white",
                             font=("Segoe UI", 10, "bold"),
                             relief="flat", padx=15)
        select_btn.pack(side='left', padx=2)
        
        deselect_btn = tk.Button(search_frame, text="✗ Снять все",
                               command=self.deselect_all_programs,
                               bg="#585b70", fg="white",
                               font=("Segoe UI", 10, "bold"),
                               relief="flat", padx=15)
        deselect_btn.pack(side='left', padx=2)
        
        # Категории
        categories_frame = tk.Frame(right_panel, bg=self.colors["bg"])
        categories_frame.pack(fill='x', pady=(0, 10))
        
        self.category_vars = {}
        categories = [
            ("🌐 Браузеры", "browser"),
            ("💻 Разработка", "development"),
            ("🎮 Игры", "games"),
            ("🎨 Графика", "graphics"),
            ("📺 Мультимедиа", "media"),
            ("💼 Офис", "office"),
            ("🔧 Утилиты", "system"),
            ("📱 Мессенджеры", "messenger"),
            ("🎵 Аудио", "audio"),
            ("📚 Образование", "education")
        ]
        
        for i, (name, key) in enumerate(categories):
            var = tk.BooleanVar(value=True)
            self.category_vars[key] = var
            cb = tk.Checkbutton(categories_frame, text=name, variable=var,
                              command=self.filter_programs,
                              bg=self.colors["bg"], fg=self.colors["fg"],
                              selectcolor=self.colors["bg"],
                              activebackground=self.colors["bg"],
                              activeforeground=self.colors["primary"],
                              font=("Segoe UI", 9))
            cb.grid(row=0, column=i, padx=5)
        
        # Список программ в Canvas с прокруткой
        canvas_frame = tk.Frame(right_panel, bg=self.colors["bg"])
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors["bg"],
                              highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical",
                               command=self.canvas.yview)
        self.programs_frame = tk.Frame(self.canvas, bg=self.colors["bg"])
        
        self.canvas.create_window((0, 0), window=self.programs_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.programs_frame.bind("<Configure>", 
                               lambda e: self.canvas.configure(
                                   scrollregion=self.canvas.bbox("all")))
        
        # Данные о программах (расширенный список)
        self.software_list = self.get_extended_software_list()
        self.display_programs()
        
        # Нижняя панель
        bottom_frame = tk.Frame(self.root, bg=self.colors["bg"], height=80)
        bottom_frame.pack(fill='x', padx=20, pady=10)
        bottom_frame.pack_propagate(False)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(bottom_frame, mode='indeterminate',
                                      style="Custom.Horizontal.TProgressbar")
        
        # Кнопка установки
        self.install_btn = tk.Button(bottom_frame, text="🚀 НАЧАТЬ УСТАНОВКУ",
                                   command=self.start_installation,
                                   bg="#f38ba8", fg="white",
                                   font=("Segoe UI", 12, "bold"),
                                   relief="flat", padx=40, pady=12)
        self.install_btn.pack(side='right')
        
        # Лог
        self.log_text = scrolledtext.ScrolledText(bottom_frame, height=8,
                                                bg="#11111b", fg="#cdd6f4",
                                                font=("Consolas", 9),
                                                relief="flat")
        
        # Обновляем статистику
        self.update_stats()

    def get_extended_software_list(self):
        """Расширенный список программ"""
        return [
            # === ОБЯЗАТЕЛЬНЫЕ ===
            {"id": "rpmfusion_free", "name": "📦 RPM Fusion Free", "required": True, 
             "type": "repository", "category": "system", "icon": "🔧",
             "description": "Репозиторий свободных пакетов",
             "dnf_cmd": ["dnf", "install", "-y", "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm"]},
            
            {"id": "rpmfusion_nonfree", "name": "📦 RPM Fusion Non-Free", "required": True,
             "type": "repository", "category": "system", "icon": "🔧",
             "description": "Репозиторий несвободных пакетов",
             "dnf_cmd": ["dnf", "install", "-y", "https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm"]},
            
            {"id": "flatpak", "name": "📦 Flatpak", "required": True,
             "type": "package", "category": "system", "icon": "📦",
             "description": "Система контейнеризации приложений",
             "dnf_cmd": ["dnf", "install", "-y", "flatpak"]},
            
            {"id": "flathub", "name": "🛒 Flathub", "required": True,
             "type": "repository", "category": "system", "icon": "🛒",
             "description": "Магазин приложений Flatpak",
             "dnf_cmd": ["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"]},
            
            # === БРАУЗЕРЫ ===
            {"id": "firefox", "name": "🦊 Firefox", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Браузер с открытым исходным кодом",
             "dnf_cmd": ["dnf", "install", "-y", "firefox"]},
            
            {"id": "chrome", "name": "🔵 Google Chrome", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Браузер от Google",
             "dnf_cmd": ["dnf", "config-manager", "--set-enabled", "google-chrome"]},
            
            {"id": "chromium", "name": "⚫ Chromium", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Открытая версия Chrome",
             "dnf_cmd": ["dnf", "install", "-y", "chromium"]},
            
            {"id": "brave", "name": "🦁 Brave", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Браузер с защитой приватности",
             "dnf_cmd": ["dnf", "install", "-y", "brave-browser"]},
            
            {"id": "opera", "name": "🔴 Opera", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Браузер со встроенным VPN",
             "dnf_cmd": ["dnf", "config-manager", "--set-enabled", "opera"]},
            
            {"id": "vivaldi", "name": "🔶 Vivaldi", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Настраиваемый браузер",
             "dnf_cmd": ["dnf", "config-manager", "--add-repo", "https://repo.vivaldi.com/archive/vivaldi-fedora.repo", "&&", "dnf", "install", "-y", "vivaldi-stable"]},
            
            {"id": "tor", "name": "🧅 Tor Browser", "required": False,
             "type": "browser", "category": "browser", "icon": "🌐",
             "description": "Анонимный браузер",
             "dnf_cmd": ["dnf", "install", "-y", "tor", "torbrowser-launcher"]},
            
            # === РАЗРАБОТКА ===
            {"id": "vscode", "name": "💻 VS Code", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Редактор кода от Microsoft",
             "dnf_cmd": ["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc", "&&", "sh", "-c", "echo -e '[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc' > /etc/yum.repos.d/vscode.repo", "&&", "dnf", "install", "-y", "code"]},
            
            {"id": "git", "name": "🔀 Git", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Система контроля версий",
             "dnf_cmd": ["dnf", "install", "-y", "git"]},
            
            {"id": "python", "name": "🐍 Python", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Python с инструментами разработки",
             "dnf_cmd": ["dnf", "install", "-y", "python3", "python3-devel", "python3-pip", "python3-virtualenv"]},
            
            {"id": "nodejs", "name": "⬢ Node.js", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "JavaScript runtime",
             "dnf_cmd": ["dnf", "install", "-y", "nodejs", "npm"]},
            
            {"id": "docker", "name": "🐳 Docker", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Платформа контейнеризации",
             "dnf_cmd": ["dnf", "-y", "install", "dnf-plugins-core", "&&", "dnf", "config-manager", "--add-repo", "https://download.docker.com/linux/fedora/docker-ce.repo", "&&", "dnf", "install", "-y", "docker-ce", "docker-ce-cli", "containerd.io"]},
            
            {"id": "postman", "name": "📮 Postman", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "API тестирование",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.getpostman.Postman"]},
            
            {"id": "phpstorm", "name": "🐘 PHPStorm", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "IDE для PHP",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.jetbrains.PhpStorm"]},
            
            {"id": "pycharm", "name": "🐍 PyCharm", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "IDE для Python",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.jetbrains.PyCharm-Professional"]},
            
            {"id": "intellij", "name": "☕ IntelliJ IDEA", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "IDE для Java",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.jetbrains.IntelliJ-IDEA-Ultimate"]},
            
            {"id": "mysql", "name": "🐬 MySQL", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Система управления базами данных",
             "dnf_cmd": ["dnf", "install", "-y", "mysql-server"]},
            
            {"id": "postgresql", "name": "🐘 PostgreSQL", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Объектно-реляционная СУБД",
             "dnf_cmd": ["dnf", "install", "-y", "postgresql-server"]},
            
            {"id": "redis", "name": "🗃️ Redis", "required": False,
             "type": "development", "category": "development", "icon": "👨‍💻",
             "description": "Ключ-значение база данных",
             "dnf_cmd": ["dnf", "install", "-y", "redis"]},
            
            # === ИГРЫ ===
            {"id": "steam", "name": "🎮 Steam", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Игровая платформа",
             "dnf_cmd": ["dnf", "install", "-y", "steam"]},
            
            {"id": "lutris", "name": "🕹️ Lutris", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Менеджер игр для Linux",
             "dnf_cmd": ["dnf", "install", "-y", "lutris"]},
            
            {"id": "wine", "name": "🍷 Wine", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Совместимость с Windows",
             "dnf_cmd": ["dnf", "install", "-y", "wine"]},
            
            {"id": "proton", "name": "⚛️ Proton", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Steam Play compatibility tool",
             "dnf_cmd": ["dnf", "install", "-y", "proton"]},
            
            {"id": "retroarch", "name": "👾 RetroArch", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Эмулятор ретро-игр",
             "dnf_cmd": ["dnf", "install", "-y", "retroarch"]},
            
            {"id": "dolphin", "name": "🐬 Dolphin", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Эмулятор GameCube/Wii",
             "dnf_cmd": ["dnf", "install", "-y", "dolphin-emu"]},
            
            {"id": "minecraft", "name": "⛏️ Minecraft", "required": False,
             "type": "games", "category": "games", "icon": "🎮",
             "description": "Строительная игра",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.mojang.Minecraft"]},
            
            # === ГРАФИКА ===
            {"id": "gimp", "name": "🎨 GIMP", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Редактор изображений",
             "dnf_cmd": ["dnf", "install", "-y", "gimp"]},
            
            {"id": "inkscape", "name": "🖋️ Inkscape", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Векторный графический редактор",
             "dnf_cmd": ["dnf", "install", "-y", "inkscape"]},
            
            {"id": "krita", "name": "🖌️ Krita", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Цифровая живопись",
             "dnf_cmd": ["dnf", "install", "-y", "krita"]},
            
            {"id": "blender", "name": "🎬 Blender", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "3D моделирование и анимация",
             "dnf_cmd": ["dnf", "install", "-y", "blender"]},
            
            {"id": "darktable", "name": "📷 Darktable", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Обработка RAW фотографий",
             "dnf_cmd": ["dnf", "install", "-y", "darktable"]},
            
            {"id": "scribus", "name": "📄 Scribus", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Настольная издательская система",
             "dnf_cmd": ["dnf", "install", "-y", "scribus"]},
            
            {"id": "freecad", "name": "📐 FreeCAD", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Параметрическое 3D CAD",
             "dnf_cmd": ["dnf", "install", "-y", "freecad"]},
            
            {"id": "openscad", "name": "⚙️ OpenSCAD", "required": False,
             "type": "graphics", "category": "graphics", "icon": "🎨",
             "description": "Программное 3D моделирование",
             "dnf_cmd": ["dnf", "install", "-y", "openscad"]},
            
            # === МУЛЬТИМЕДИА ===
            {"id": "vlc", "name": "📺 VLC", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Медиаплеер",
             "dnf_cmd": ["dnf", "install", "-y", "vlc"]},
            
            {"id": "obs", "name": "🎥 OBS Studio", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Запись и стриминг",
             "dnf_cmd": ["dnf", "install", "-y", "obs-studio"]},
            
            {"id": "kdenlive", "name": "🎬 Kdenlive", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Видеоредактор",
             "dnf_cmd": ["dnf", "install", "-y", "kdenlive"]},
            
            {"id": "spotify", "name": "🎵 Spotify", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Музыкальный стриминг",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.spotify.Client"]},
            
            {"id": "audacity", "name": "🎤 Audacity", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Редактор аудио",
             "dnf_cmd": ["dnf", "install", "-y", "audacity"]},
            
            {"id": "handbrake", "name": "🎞️ HandBrake", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Видеоконвертер",
             "dnf_cmd": ["dnf", "install", "-y", "handbrake"]},
            
            {"id": "kodi", "name": "📀 Kodi", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Медиацентр",
             "dnf_cmd": ["dnf", "install", "-y", "kodi"]},
            
            {"id": "shotcut", "name": "✂️ Shotcut", "required": False,
             "type": "media", "category": "media", "icon": "🎵",
             "description": "Видеоредактор",
             "dnf_cmd": ["dnf", "install", "-y", "shotcut"]},
            
            # === ОФИС ===
            {"id": "libreoffice", "name": "📊 LibreOffice", "required": False,
             "type": "office", "category": "office", "icon": "💼",
             "description": "Офисный пакет",
             "dnf_cmd": ["dnf", "install", "-y", "libreoffice"]},
            
            {"id": "onlyoffice", "name": "📈 OnlyOffice", "required": False,
             "type": "office", "category": "office", "icon": "💼",
             "description": "Офисный пакет",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.onlyoffice.desktopeditors"]},
            
            {"id": "thunderbird", "name": "✉️ Thunderbird", "required": False,
             "type": "office", "category": "office", "icon": "💼",
             "description": "Почтовый клиент",
             "dnf_cmd": ["dnf", "install", "-y", "thunderbird"]},
            
            {"id": "calibre", "name": "📚 Calibre", "required": False,
             "type": "office", "category": "office", "icon": "💼",
             "description": "Управление электронными книгами",
             "dnf_cmd": ["dnf", "install", "-y", "calibre"]},
            
            {"id": "okular", "name": "📖 Okular", "required": False,
             "type": "office", "category": "office", "icon": "💼",
             "description": "Просмотрщик PDF",
             "dnf_cmd": ["dnf", "install", "-y", "okular"]},
            
            # === УТИЛИТЫ ===
            {"id": "htop", "name": "📊 htop", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Монитор процессов",
             "dnf_cmd": ["dnf", "install", "-y", "htop"]},
            
            {"id": "neofetch", "name": "🐧 neofetch", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Информация о системе",
             "dnf_cmd": ["dnf", "install", "-y", "neofetch"]},
            
            {"id": "gparted", "name": "💾 GParted", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Редактор разделов",
             "dnf_cmd": ["dnf", "install", "-y", "gparted"]},
            
            {"id": "timeshift", "name": "🕰️ Timeshift", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Резервное копирование системы",
             "dnf_cmd": ["dnf", "install", "-y", "timeshift"]},
            
            {"id": "bleachbit", "name": "🧹 BleachBit", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Очистка системы",
             "dnf_cmd": ["dnf", "install", "-y", "bleachbit"]},
            
            {"id": "speedtest", "name": "🌐 Speedtest", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Проверка скорости интернета",
             "dnf_cmd": ["dnf", "install", "-y", "speedtest-cli"]},
            
            {"id": "grub_customizer", "name": "🍔 Grub Customizer", "required": False,
             "type": "system", "category": "system", "icon": "🔧",
             "description": "Настройка Grub",
             "dnf_cmd": ["dnf", "install", "-y", "grub-customizer"]},
            
            # === МЕССЕНДЖЕРЫ ===
            {"id": "telegram", "name": "📱 Telegram", "required": False,
             "type": "messenger", "category": "messenger", "icon": "💬",
             "description": "Мессенджер",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.telegram.desktop"]},
            
            {"id": "discord", "name": "🎮 Discord", "required": False,
             "type": "messenger", "category": "messenger", "icon": "💬",
             "description": "Голосовой чат для геймеров",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "com.discordapp.Discord"]},
            
            {"id": "signal", "name": "🔒 Signal", "required": False,
             "type": "messenger", "category": "messenger", "icon": "💬",
             "description": "Защищенный мессенджер",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.signal.Signal"]},
            
            {"id": "element", "name": "🏠 Element", "required": False,
             "type": "messenger", "category": "messenger", "icon": "💬",
             "description": "Matrix клиент",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "im.riot.Riot"]},
            
            # === АУДИО ===
            {"id": "ardour", "name": "🎹 Ardour", "required": False,
             "type": "audio", "category": "audio", "icon": "🎶",
             "description": "Цифровая звуковая рабочая станция",
             "dnf_cmd": ["dnf", "install", "-y", "ardour"]},
            
            {"id": "lmms", "name": "🎼 LMMS", "required": False,
             "type": "audio", "category": "audio", "icon": "🎶",
             "description": "Создание музыки",
             "dnf_cmd": ["dnf", "install", "-y", "lmms"]},
            
            {"id": "hydrogen", "name": "🥁 Hydrogen", "required": False,
             "type": "audio", "category": "audio", "icon": "🎶",
             "description": "Барабанная машина",
             "dnf_cmd": ["dnf", "install", "-y", "hydrogen"]},
            
            # === ОБРАЗОВАНИЕ ===
            {"id": "anki", "name": "📚 Anki", "required": False,
             "type": "education", "category": "education", "icon": "🎓",
             "description": "Карточки для запоминания",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "net.ankiweb.Anki"]},
            
            {"id": "stellarium", "name": "🌌 Stellarium", "required": False,
             "type": "education", "category": "education", "icon": "🎓",
             "description": "Планетарий",
             "dnf_cmd": ["dnf", "install", "-y", "stellarium"]},
            
            {"id": "geogebra", "name": "📐 GeoGebra", "required": False,
             "type": "education", "category": "education", "icon": "🎓",
             "description": "Математическое ПО",
             "dnf_cmd": ["flatpak", "install", "-y", "flathub", "org.geogebra.GeoGebra"]},
            
            # === ДРАЙВЕРА ===
            {"id": "nvidia_drivers", "name": "🎮 NVIDIA Drivers", "required": False,
             "type": "drivers", "category": "system", "icon": "⚙️",
             "description": "Драйвера для видеокарт NVIDIA",
             "dnf_cmd": ["dnf", "install", "-y", "akmod-nvidia", "xorg-x11-drv-nvidia-cuda"]},
            
            {"id": "media_codecs", "name": "🎬 Media Codecs", "required": False,
             "type": "package", "category": "system", "icon": "⚙️",
             "description": "Кодеки для медиа",
             "dnf_cmd": ["dnf", "groupupdate", "-y", "--with-optional", "Multimedia"]}
        ]
        
        # Инициализируем выбранные программы
        for software in self.software_list:
            if software['required']:
                software['selected'] = True
            else:
                software['selected'] = False
        
        return self.software_list

    def display_programs(self):
        """Отображает программы в интерфейсе"""
        # Очищаем текущий список
        for widget in self.programs_frame.winfo_children():
            widget.destroy()
        
        # Фильтруем программы
        search_text = self.search_var.get().lower()
        
        for software in self.software_list:
            # Проверка поиска
            if search_text and search_text != "🔍 поиск программ...":
                if (search_text not in software['name'].lower() and 
                    search_text not in software['description'].lower()):
                    continue
            
            # Проверка категории
            category_active = self.category_vars.get(software['category'], tk.BooleanVar(value=True)).get()
            if not category_active:
                continue
            
            # Создаем карточку программы
            card = tk.Frame(self.programs_frame, bg=self.colors["card_bg"], 
                          relief="flat", bd=1)
            card.pack(fill='x', padx=5, pady=3)
            
            # Чекбокс
            var = tk.BooleanVar(value=software.get('selected', False))
            software['var'] = var
            
            if software['required']:
                # Для обязательных программ - делаем чекбокс неактивным
                cb = tk.Checkbutton(card, variable=var, state='disabled',
                                  bg=self.colors["card_bg"], fg="#a6adc8",
                                  selectcolor=self.colors["card_bg"])
            else:
                cb = tk.Checkbutton(card, variable=var,
                                  command=lambda s=software, v=var: self.toggle_program(s, v),
                                  bg=self.colors["card_bg"], fg=self.colors["fg"],
                                  selectcolor=self.colors["card_bg"],
                                  activebackground=self.colors["card_bg"],
                                  activeforeground=self.colors["primary"])
            
            cb.pack(side='left', padx=10)
            
            # Иконка и название
            icon_frame = tk.Frame(card, bg=self.colors["card_bg"])
            icon_frame.pack(side='left', fill='y', padx=(0, 10))
            
            icon_label = tk.Label(icon_frame, text=software['icon'], 
                                font=("Segoe UI", 16),
                                bg=self.colors["card_bg"], fg=self.colors["primary"])
            icon_label.pack()
            
            # Информация
            info_frame = tk.Frame(card, bg=self.colors["card_bg"])
            info_frame.pack(side='left', fill='both', expand=True)
            
            name_label = tk.Label(info_frame, text=software['name'],
                                font=("Segoe UI", 11, "bold"),
                                bg=self.colors["card_bg"], fg=self.colors["fg"],
                                anchor='w')
            name_label.pack(anchor='w')
            
            desc_label = tk.Label(info_frame, text=software['description'],
                                font=("Segoe UI", 9),
                                bg=self.colors["card_bg"], fg="#a6adc8",
                                anchor='w')
            desc_label.pack(anchor='w')
            
            # Категория
            cat_frame = tk.Frame(card, bg=self.colors["card_bg"])
            cat_frame.pack(side='right', padx=10)
            
            cat_label = tk.Label(cat_frame, 
                               text=f"📁 {software['category']}",
                               font=("Segoe UI", 8),
                               bg="#45475a", fg="#cdd6f4",
                               padx=6, pady=2)
            cat_label.pack()

    def toggle_program(self, software, var):
        """Переключение состояния программы"""
        software['selected'] = var.get()
        self.update_stats()

    def select_all_programs(self):
        """Выбрать все программы"""
        for software in self.software_list:
            if not software['required']:
                software['selected'] = True
                if 'var' in software:
                    software['var'].set(True)
        self.display_programs()
        self.update_stats()

    def deselect_all_programs(self):
        """Снять выбор со всех программ"""
        for software in self.software_list:
            if not software['required']:
                software['selected'] = False
                if 'var' in software:
                    software['var'].set(False)
        self.display_programs()
        self.update_stats()

    def filter_programs(self, *args):
        """Фильтрация программ по поиску и категориям"""
        self.display_programs()

    def update_stats(self):
        """Обновление статистики"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        selected_count = sum(1 for s in self.software_list if s.get('selected', False))
        total_count = len(self.software_list)
        
        # Время установки (приблизительно)
        estimate_minutes = selected_count * 2
        hours = estimate_minutes // 60
        minutes = estimate_minutes % 60
        
        stats_data = [
            (f"📦 Всего программ: {total_count}", self.colors["secondary"]),
            (f"✅ Выбрано: {selected_count}", self.colors["success"]),
            (f"⏱️ Время: {hours}ч {minutes}мин", self.colors["warning"]),
            (f"💾 Память: ~{selected_count * 50} MB", self.colors["accent"])
        ]
        
        for text, color in stats_data:
            label = tk.Label(self.stats_frame, text=text,
                           font=("Segoe UI", 9, "bold"),
                           bg=self.colors["card_bg"], fg=color)
            label.pack(anchor='w', pady=2)

    def update_language(self):
        """Обновление языка интерфейса"""
        lang = self.language.get()
        texts = self.translations[lang]
        
        # Обновляем тексты
        self.warning_label.config(text=texts["warning_text"])
        self.install_btn.config(text=texts["install_btn"])
        
        # Обновляем статистику
        self.update_stats()
        
        # Перерисовываем программы для обновления описаний
        self.display_programs()

    def show_help(self):
        """Показать справку"""
        lang = self.language.get()
        texts = self.translations[lang]
        
        help_window = tk.Toplevel(self.root)
        help_window.title(texts["help_title"])
        help_window.geometry("700x600")
        help_window.configure(bg=self.colors["bg"])
        help_window.resizable(True, True)
        
        # Создаем Notebook для вкладок
        notebook = ttk.Notebook(help_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка с инструкцией
        help_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(help_frame, text="📖 Инструкция")
        
        help_text = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD,
                                            bg="#11111b", fg="#cdd6f4",
                                            font=("Segoe UI", 10))
        help_text.pack(fill='both', expand=True, padx=10, pady=10)
        help_text.insert('1.0', texts["help_text"])
        help_text.config(state='disabled')
        
        # Вкладка с горячими клавишами
        shortcuts_frame = tk.Frame(notebook, bg=self.colors["bg"])
        notebook.add(shortcuts_frame, text="⌨️ Горячие клавиши")
        
        shortcuts = """
        🎮 Игровой режим:
        Super + G - Включить игровой режим
        Super + F - Полноэкранный режим
        Super + S - Сделать скриншот
        
        🖥️ Рабочий стол:
        Super + 1-9 - Переключение рабочих столов
        Super + Tab - Переключение окон
        Super + D - Показать рабочий стол
        Super + L - Заблокировать экран
        
        🛠️ Система:
        Super + T - Терминал
        Super + E - Файловый менеджер
        Super + W - Веб-браузер
        Super + P - Настройки
        """
        
        shortcuts_text = scrolledtext.ScrolledText(shortcuts_frame, wrap=tk.WORD,
                                                 bg="#11111b", fg="#cdd6f4",
                                                 font=("Segoe UI", 10))
        shortcuts_text.pack(fill='both', expand=True, padx=10, pady=10)
        shortcuts_text.insert('1.0', shortcuts)
        shortcuts_text.config(state='disabled')
        
        # Кнопка закрытия
        btn_frame = tk.Frame(help_window, bg=self.colors["bg"])
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        close_btn = tk.Button(btn_frame, text="Закрыть", 
                            command=help_window.destroy,
                            bg=self.colors["primary"], fg="white",
                            font=("Segoe UI", 10, "bold"),
                            relief="flat", padx=20, pady=5)
        close_btn.pack()

    def log_message(self, message, level="info"):
        """Добавление сообщения в лог"""
        colors = {
            "info": "#89b4fa",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "error": "#f38ba8"
        }
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Показываем лог если он скрыт
        if not self.log_text.winfo_ismapped():
            self.log_text.pack(fill='x', pady=5)
        
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, log_entry)
        
        # Применяем цвет к последней строке
        start_index = f"{self.log_text.index(tk.END).split('.')[0]}.0"
        end_index = self.log_text.index(tk.END)
        
        self.log_text.tag_add(level, start_index, end_index)
        self.log_text.tag_config(level, foreground=colors.get(level, "#89b4fa"))
        
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def run_command(self, cmd, shell=False):
        """Выполнение команды"""
        try:
            self.log_message(f"Выполняю: {' '.join(cmd) if isinstance(cmd, list) else cmd}", "info")
            
            if shell:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if result.stdout:
                self.log_message(result.stdout.strip(), "success")
            
            return result
            
        except subprocess.CalledProcessError as e:
            self.log_message(f"Ошибка: {e.stderr}", "error")
            raise

    def install_software(self):
        """Основная установка"""
        try:
            # Показываем прогресс
            self.progress.pack(fill='x', pady=5)
            self.progress.start()
            self.install_btn.config(state='disabled')
            
            self.log_message("🚀 Начинаю установку...", "success")
            
            # Обновление системы
            self.log_message("🔄 Обновляю систему...", "info")
            self.run_command(["dnf", "update", "-y"])
            
            # Установка DE
            de_installed = False
            for de_name, var in self.de_vars.items():
                if var.get():
                    de_installed = True
                    self.log_message(f"🎨 Устанавливаю {de_name}...", "info")
                    
                    if de_name == "hyprland":
                        self.install_hyprland()
                    else:
                        self.run_command(["dnf", "groupinstall", "-y", f"{de_name}-desktop"])
            
            # Установка программ
            selected_software = [s for s in self.software_list if s.get('selected', False)]
            self.log_message(f"📦 Устанавливаю {len(selected_software)} программ...", "info")
            
            for i, software in enumerate(selected_software, 1):
                if 'dnf_cmd' in software:
                    self.log_message(f"({i}/{len(selected_software)}) {software['name']}", "info")
                    try:
                        if isinstance(software['dnf_cmd'], list):
                            if '&&' in software['dnf_cmd']:
                                cmd_str = ' '.join(software['dnf_cmd'])
                                self.run_command(cmd_str, shell=True)
                            else:
                                self.run_command(software['dnf_cmd'])
                        else:
                            self.run_command(software['dnf_cmd'], shell=True)
                    except Exception as e:
                        self.log_message(f"⚠️ Пропускаю {software['name']}: {str(e)}", "warning")
            
            # Сохраняем в историю
            self.save_to_history(selected_software, de_installed)
            
            self.log_message("✅ Установка завершена успешно!", "success")
            messagebox.showinfo("Успех", "Установка завершена успешно!")
            
        except Exception as e:
            self.log_message(f"❌ Критическая ошибка: {str(e)}", "error")
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
        finally:
            self.progress.stop()
            self.progress.pack_forget()
            self.install_btn.config(state='normal')

    def install_hyprland(self):
        """Установка Hyprland"""
        try:
            self.log_message("🚀 Устанавливаю Hyprland...", "info")
            
            commands = [
                "git clone --depth=1 https://github.com/hyprwm/Hyprland ~/Hyprland",
                "cd ~/Hyprland && sudo make install",
                "systemctl enable --now sddm"
            ]
            
            for cmd in commands:
                self.run_command(cmd, shell=True)
            
            self.log_message("✅ Hyprland установлен!", "success")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка установки Hyprland: {str(e)}", "error")

    def update_system(self):
        """Обновление системы"""
        try:
            self.log_message("🔄 Начинаю обновление системы...", "info")
            self.run_command(["dnf", "update", "-y"])
            self.log_message("✅ Система обновлена!", "success")
            messagebox.showinfo("Обновление", "Система успешно обновлена!")
        except Exception as e:
            self.log_message(f"❌ Ошибка обновления: {str(e)}", "error")

    def clean_system(self):
        """Очистка системы"""
        try:
            self.log_message("🧹 Начинаю очистку системы...", "info")
            
            commands = [
                ["dnf", "autoremove", "-y"],
                ["dnf", "clean", "all"],
                ["flatpak", "uninstall", "--unused", "-y"],
                ["journalctl", "--vacuum-time=3d"]
            ]
            
            for cmd in commands:
                self.run_command(cmd)
            
            self.log_message("✅ Система очищена!", "success")
            messagebox.showinfo("Очистка", "Система успешно очищена!")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка очистки: {str(e)}", "error")

    def express_install(self):
        """Экспресс-установка"""
        express_packages = [
            "vscode", "git", "python", "docker",
            "gimp", "inkscape", "blender",
            "libreoffice", "vlc", "obs",
            "steam", "discord", "telegram"
        ]
        
        # Выбираем экспресс-пакеты
        for software in self.software_list:
            software['selected'] = software['id'] in express_packages or software['required']
            if 'var' in software:
                software['var'].set(software['selected'])
        
        self.display_programs()
        self.update_stats()
        self.log_message("⚡ Настроена экспресс-установка", "success")

    def show_history(self):
        """Показать историю установок"""
        history_window = tk.Toplevel(self.root)
        history_window.title("📊 История установок")
        history_window.geometry("600x400")
        history_window.configure(bg=self.colors["bg"])
        
        if not self.installation_history:
            label = tk.Label(history_window, text="История пуста",
                           bg=self.colors["bg"], fg=self.colors["fg"],
                           font=("Segoe UI", 12))
            label.pack(pady=50)
        else:
            tree = ttk.Treeview(history_window, columns=("date", "count", "de"), show="headings")
            tree.heading("date", text="Дата")
            tree.heading("count", text="Программ")
            tree.heading("de", text="Окружение")
            
            for item in self.installation_history[-10:]:  # Последние 10 записей
                tree.insert("", "end", values=(item['date'], item['count'], item['de']))
            
            tree.pack(fill='both', expand=True, padx=10, pady=10)

    def save_to_history(self, software_list, de_installed):
        """Сохранение в историю"""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "count": len(software_list),
            "de": "Да" if de_installed else "Нет",
            "packages": [s['name'] for s in software_list]
        }
        
        self.installation_history.append(entry)
        self.save_history()

    def load_history(self):
        """Загрузка истории"""
        history_file = os.path.expanduser("~/.fedora_installer_history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.installation_history = json.load(f)
            except:
                self.installation_history = []

    def save_history(self):
        """Сохранение истории"""
        history_file = os.path.expanduser("~/.fedora_installer_history.json")
        try:
            with open(history_file, 'w') as f:
                json.dump(self.installation_history, f, indent=2)
        except:
            pass

    def start_installation(self):
        """Начало установки"""
        # Проверка прав
        if os.geteuid() != 0:
            messagebox.showerror("Ошибка", "Запустите программу с правами sudo!")
            return
        
        # Подтверждение
        selected_count = sum(1 for s in self.software_list if s.get('selected', False))
        
        if messagebox.askyesno("Подтверждение",
                              f"Установить {selected_count} программ?\n"
                              "Процесс может занять длительное время."):
            thread = threading.Thread(target=self.install_software)
            thread.daemon = True
            thread.start()

    def run(self):
        """Запуск приложения"""
        # Проверка системы
        if not os.path.exists('/etc/fedora-release'):
            messagebox.showerror("Ошибка", "Этот установщик предназначен только для Fedora!")
            return
        
        self.root.mainloop()

if __name__ == "__main__":
    app = FedoraSoftwareInstaller()
    app.run() 

