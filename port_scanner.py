
import sys
import socket
import threading
import queue
import ipaddress
import time
from datetime import datetime
import json
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import logging
import psutil
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLineEdit, QPushButton, QProgressBar, QComboBox, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView, 
                            QStyleFactory, QMenuBar, QMenu, QStatusBar,
                            QDialog, QFormLayout, QSpinBox, QMessageBox, QCheckBox,
                            QTabWidget, QGroupBox, QColorDialog, QToolTip)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTranslator, QLocale
from PyQt6.QtGui import QIcon, QColor, QPalette, QAction, QKeySequence, QShortcut
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Attempt to import netifaces, but make it optional
try:
    import netifaces
    NETIFACES_AVAILABLE = True
except ImportError:
    NETIFACES_AVAILABLE = False
    logging.warning("netifaces module not available. Network interface selection disabled.")

# Setup logging
logging.basicConfig(filename='port_scanner.log', level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        'title': 'Advanced Network Port Scanner',
        'ip_label': 'IP Address/Range:',
        'port_label': 'Port Range:',
        'scan_button': 'Start Scan',
        'stop_button': 'Stop Scan',
        'pause_button': 'Pause Scan',
        'resume_button': 'Resume Scan',
        'clear_button': 'Clear Results',
        'theme_label': 'Theme:',
        'language_label': 'Language:',
        'results_label': 'Scan Results:',
        'history_label': 'Scan History:',
        'visualization_label': 'Port Distribution:',
        'settings_menu': 'Settings',
        'save_config': 'Save Configuration',
        'load_config': 'Load Configuration',
        'export_results': 'Export Results',
        'custom_theme': 'Custom Theme',
        'interface_label': 'Network Interface:',
        'scan_profile_label': 'Scan Profile:',
        'timeout_label': 'Timeout (ms):',
        'threads_label': 'Threads:',
        'ip': 'IP Address',
        'port': 'Port',
        'service': 'Service',
        'status': 'Status',
        'banner': 'Banner',
        'scanning': 'Scanning...',
        'paused': 'Scan Paused',
        'resumed': 'Scan Resumed',
        'completed': 'Scan Completed',
        'stopped': 'Scan Stopped',
        'error': 'Error',
        'invalid_ip': 'Invalid IP address or range (e.g., 192.168.1.1 or 192.168.1.0/24)',
        'invalid_port': 'Invalid port range (e.g., 1-65535 or 80,443,22)',
        'results_saved': 'Results saved successfully to {}',
        'config_saved': 'Configuration saved successfully',
        'config_loaded': 'Configuration loaded successfully',
        'about': 'About',
        'about_text': 'Advanced Network Port Scanner v2.0\nDeveloped with PyQt6\nSupports multiple themes, languages, and advanced features',
        'direction': 'ltr',
        'netifaces_warning': 'Network interface selection unavailable (install netifaces)'
    },
    'fa': {
        'title': 'اسکنر پیشرفته پورت شبکه',
        'ip_label': 'آدرس/محدوده IP:',
        'port_label': 'محدوده پورت:',
        'scan_button': 'شروع اسکن',
        'stop_button': 'توقف اسکن',
        'pause_button': 'مکث اسکن',
        'resume_button': 'ادامه اسکن',
        'clear_button': 'پاک کردن نتایج',
        'theme_label': 'تم:',
        'language_label': 'زبان:',
        'results_label': 'نتایج اسکن:',
        'history_label': 'تاریخچه اسکن:',
        'visualization_label': 'توزیع پورت‌ها:',
        'settings_menu': 'تنظیمات',
        'save_config': 'ذخیره تنظیمات',
        'load_config': 'بارگذاری تنظیمات',
        'export_results': 'خروجی نتایج',
        'custom_theme': 'تم سفارشی',
        'interface_label': 'رابط شبکه:',
        'scan_profile_label': 'پروفایل اسکن:',
        'timeout_label': 'تایم‌اوت (میلی‌ثانیه):',
        'threads_label': 'تعداد نخ‌ها:',
        'ip': 'آدرس IP',
        'port': 'پورت',
        'service': 'سرویس',
        'status': 'وضعیت',
        'banner': 'بنر',
        'scanning': 'در حال اسکن...',
        'paused': 'اسکن متوقف شده',
        'resumed': 'اسکن از سر گرفته شد',
        'completed': 'اسکن کامل شد',
        'stopped': 'اسکن متوقف شد',
        'error': 'خطا',
        'invalid_ip': 'آدرس یا محدوده IP نامعتبر است (مثال: 192.168.1.1 یا 192.168.1.0/24)',
        'invalid_port': 'محدوده پورت نامعتبر است (مثال: 1-65535 یا 80,443,22)',
        'results_saved': 'نتایج با موفقیت در {} ذخیره شد',
        'config_saved': 'تنظیمات با موفقیت ذخیره شد',
        'config_loaded': 'تنظیمات با موفقیت بارگذاری شد',
        'about': 'درباره',
        'about_text': 'اسکنر پیشرفته پورت شبکه نسخه 2.0\nتوسعه یافته با PyQt6\nپشتیبانی از چندین تم، زبان و ویژگی‌های پیشرفته',
        'direction': 'rtl',
        'netifaces_warning': 'انتخاب رابط شبکه در دسترس نیست (netifaces را نصب کنید)'
    },
    'zh': {
        'title': '高级网络端口扫描器',
        'ip_label': 'IP地址/范围：',
        'port_label': '端口范围：',
        'scan_button': '开始扫描',
        'stop_button': '停止扫描',
        'pause_button': '暂停扫描',
        'resume_button': '恢复扫描',
        'clear_button': '清除结果',
        'theme_label': '主题：',
        'language_label': '语言：',
        'results_label': '扫描结果：',
        'history_label': '扫描历史：',
        'visualization_label': '端口分布：',
        'settings_menu': '设置',
        'save_config': '保存配置',
        'load_config': '加载配置',
        'export_results': '导出结果',
        'custom_theme': '自定义主题',
        'interface_label': '网络接口：',
        'scan_profile_label': '扫描配置文件：',
        'timeout_label': '超时（毫秒）：',
        'threads_label': '线程数：',
        'ip': 'IP地址',
        'port': '端口',
        'service': '服务',
        'status': '状态',
        'banner': '横幅',
        'scanning': '正在扫描...',
        'paused': '扫描已暂停',
        'resumed': '扫描已恢复',
        'completed': '扫描完成',
        'stopped': '扫描已停止',
        'error': '错误',
        'invalid_ip': '无效的IP地址或范围（例如：192.168.1.1 或 192.168.1.0/24）',
        'invalid_port': '无效的端口范围（例如：1-65535 或 80,443,22）',
        'results_saved': '结果成功保存到 {}',
        'config_saved': '配置保存成功',
        'config_loaded': '配置加载成功',
        'about': '关于',
        'about_text': '高级网络端口扫描器 v2.0\n使用PyQt6开发\n支持多种主题、语言和高级功能',
        'direction': 'ltr',
        'netifaces_warning': '网络接口选择不可用（请安装netifaces）'
    }
}

# Common ports and their services
COMMON_PORTS = {
    20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
    80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 3389: 'RDP',
    3306: 'MySQL', 5432: 'PostgreSQL', 8080: 'HTTP-ALT', 8443: 'HTTPS-ALT'
}

# Scan profiles
SCAN_PROFILES = {
    'Common': '21,22,23,25,80,110,143,443,445,3389',
    'Web': '80,443,8080,8443',
    'Database': '3306,5432',
    'Full': '1-65535',
    'Quick': '21,22,80,443'
}

class ScanThread(QThread):
    scan_result = pyqtSignal(str, int, str, str, str)
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, ip_list, port_list, timeout, queue, interface=None):
        super().__init__()
        self.ip_list = ip_list
        self.port_list = port_list
        self.timeout = timeout / 1000.0
        self.queue = queue
        self.is_running = True
        self.is_paused = False
        self.interface = interface

    def get_service_banner(self, ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((ip, port))
            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner[:100] if banner else 'No banner'
        except:
            return 'No banner'

    def run(self):
        while self.is_running and not self.queue.empty():
            if self.is_paused:
                time.sleep(0.1)
                continue
            try:
                ip, port = self.queue.get()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(self.timeout)
                result = sock.connect_ex((str(ip), port))
                status = 'Open' if result == 0 else 'Closed'
                service = COMMON_PORTS.get(port, 'Unknown')
                banner = self.get_service_banner(str(ip), port) if status == 'Open' else ''
                if status == 'Open':
                    self.scan_result.emit(str(ip), port, service, status, banner)
                sock.close()
                self.progress.emit(1)
                self.queue.task_done()
            except Exception as e:
                self.error.emit(str(e))
                self.queue.task_done()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_running = False

class CustomThemeDialog(QDialog):
    def __init__(self, parent=None, language='en'):
        super().__init__(parent)
        self.setWindowTitle(TRANSLATIONS[language]['custom_theme'])
        self.language = language
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        
        self.window_color = QPushButton('Select Window Color')
        self.window_text_color = QPushButton('Select Window Text Color')
        self.base_color = QPushButton('Select Base Color')
        self.text_color = QPushButton('Select Text Color')
        
        self.window_color.clicked.connect(lambda: self.choose_color('window'))
        self.window_text_color.clicked.connect(lambda: self.choose_color('window_text'))
        self.base_color.clicked.connect(lambda: self.choose_color('base'))
        self.text_color.clicked.connect(lambda: self.choose_color('text'))
        
        layout.addRow('Window Color:', self.window_color)
        layout.addRow('Window Text Color:', self.window_text_color)
        layout.addRow('Base Color:', self.base_color)
        layout.addRow('Text Color:', self.text_color)
        
        buttons = QHBoxLayout()
        save_button = QPushButton(TRANSLATIONS[self.language]['save_config'])
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        
        layout.addRow(buttons)
        self.setLayout(layout)
        
        self.colors = {
            'window': QColor(30, 30, 30),
            'window_text': Qt.GlobalColor.white,
            'base': QColor(45, 45, 45),
            'text': Qt.GlobalColor.white
        }

    def choose_color(self, color_type):
        color = QColorDialog.getColor(self.colors[color_type], self)
        if color.isValid():
            self.colors[color_type] = color
            getattr(self, f'{color_type}_color').setStyleSheet(f'background-color: {color.name()}')

class SettingsDialog(QDialog):
    def __init__(self, parent=None, language='en'):
        super().__init__(parent)
        self.setWindowTitle(TRANSLATIONS[language]['title'])
        self.language = language
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()
        
        self.timeout_input = QSpinBox()
        self.timeout_input.setRange(100, 5000)
        self.timeout_input.setValue(1000)
        
        self.threads_input = QSpinBox()
        self.threads_input.setRange(1, max(1, psutil.cpu_count() * 2))
        self.threads_input.setValue(min(10, psutil.cpu_count()))
        
        self.interface_combo = QComboBox()
        if NETIFACES_AVAILABLE:
            interfaces = netifaces.interfaces()
            self.interface_combo.addItems(['Auto'] + interfaces)
        else:
            self.interface_combo.addItems(['Auto'])
            self.interface_combo.setEnabled(False)
            self.interface_combo.setToolTip(TRANSLATIONS[self.language]['netifaces_warning'])
        
        layout.addRow(TRANSLATIONS[self.language]['timeout_label'], self.timeout_input)
        layout.addRow(TRANSLATIONS[self.language]['threads_label'], self.threads_input)
        layout.addRow(TRANSLATIONS[self.language]['interface_label'], self.interface_combo)
        
        buttons = QHBoxLayout()
        save_button = QPushButton(TRANSLATIONS[self.language]['save_config'])
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)
        
        layout.addRow(buttons)
        self.setLayout(layout)

class PortDistributionCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.figure, self.ax = plt.subplots()
        super().__init__(self.figure)
        self.setParent(parent)
        self.ax.set_title(TRANSLATIONS['en']['visualization_label'])
        self.ax.set_xlabel('Port')
        self.ax.set_ylabel('Count')

    def update_plot(self, ports):
        self.ax.clear()
        if ports:
            self.ax.hist(ports, bins=50, color='blue', alpha=0.7)
        self.ax.set_title(TRANSLATIONS['en']['visualization_label'])
        self.ax.set_xlabel('Port')
        self.ax.set_ylabel('Count')
        self.draw()

class PortScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = 'en'
        self.theme = 'Windows'
        self.scan_threads = []
        self.task_queue = queue.Queue()
        self.total_tasks = 0
        self.completed_tasks = 0
        self.scan_history = []
        self.is_paused = False
        self.translator = QTranslator()
        self.open_ports = []
        self.init_ui()
        self.load_config()
        self.setup_shortcuts()
        self.setWindowIcon(QIcon('port_scanner.jpg'))

    def init_ui(self):
        self.setWindowTitle(TRANSLATIONS[self.language]['title'])
        self.setGeometry(100, 100, 1200, 800)
        
        # Menu Bar
        menubar = self.menuBar()
        settings_menu = menubar.addMenu(TRANSLATIONS[self.language]['settings_menu'])
        

        # Set favicon (same as window icon for consistency)
        self.setWindowIcon(QIcon('port_scanner.jpg'))

        save_action = QAction(TRANSLATIONS[self.language]['save_config'], self)
        save_action.setToolTip('Save current configuration')
        save_action.triggered.connect(self.save_config)
        load_action = QAction(TRANSLATIONS[self.language]['load_config'], self)
        load_action.setToolTip('Load saved configuration')
        load_action.triggered.connect(self.load_config)
        export_action = QAction(TRANSLATIONS[self.language]['export_results'], self)
        export_action.setToolTip('Export scan results')
        export_action.triggered.connect(self.export_results)
        custom_theme_action = QAction(TRANSLATIONS[self.language]['custom_theme'], self)
        custom_theme_action.setToolTip('Customize theme colors')
        custom_theme_action.triggered.connect(self.custom_theme)
        about_action = QAction(TRANSLATIONS[self.language]['about'], self)
        about_action.setToolTip('Show application information')
        about_action.triggered.connect(self.show_about)
        
        settings_menu.addAction(save_action)
        settings_menu.addAction(load_action)
        settings_menu.addAction(export_action)
        settings_menu.addAction(custom_theme_action)
        settings_menu.addAction(about_action)
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Scan Tab
        scan_widget = QWidget()
        scan_layout = QVBoxLayout(scan_widget)
        
        # Input section
        input_group = QGroupBox('Scan Parameters')
        input_layout = QHBoxLayout()
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('192.168.1.0/24 or 192.168.1.1')
        self.ip_input.textChanged.connect(self.validate_ip_input)
        self.ip_input.setToolTip(TRANSLATIONS[self.language]['invalid_ip'])
        input_layout.addWidget(QLabel(TRANSLATIONS[self.language]['ip_label']))
        input_layout.addWidget(self.ip_input)
        
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('1-65535 or 80,443,22')
        self.port_input.textChanged.connect(self.validate_port_input)
        self.port_input.setToolTip(TRANSLATIONS[self.language]['invalid_port'])
        input_layout.addWidget(QLabel(TRANSLATIONS[self.language]['port_label']))
        input_layout.addWidget(self.port_input)
        
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(['Custom'] + list(SCAN_PROFILES.keys()))
        self.profile_combo.currentTextChanged.connect(self.apply_scan_profile)
        input_layout.addWidget(QLabel(TRANSLATIONS[self.language]['scan_profile_label']))
        input_layout.addWidget(self.profile_combo)
        
        input_group.setLayout(input_layout)
        scan_layout.addWidget(input_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.scan_button = QPushButton(TRANSLATIONS[self.language]['scan_button'])
        self.scan_button.setToolTip('Start the port scan (Ctrl+S)')
        self.scan_button.clicked.connect(self.start_scan)
        self.pause_button = QPushButton(TRANSLATIONS[self.language]['pause_button'])
        self.pause_button.setToolTip('Pause the scan (Ctrl+P)')
        self.pause_button.clicked.connect(self.pause_scan)
        self.pause_button.setEnabled(False)
        self.resume_button = QPushButton(TRANSLATIONS[self.language]['resume_button'])
        self.resume_button.setToolTip('Resume the scan (Ctrl+R)')
        self.resume_button.clicked.connect(self.resume_scan)
        self.resume_button.setEnabled(False)
        self.stop_button = QPushButton(TRANSLATIONS[self.language]['stop_button'])
        self.stop_button.setToolTip('Stop the scan (Ctrl+T)')
        self.stop_button.clicked.connect(self.stop_scan)
        self.stop_button.setEnabled(False)
        self.clear_button = QPushButton(TRANSLATIONS[self.language]['clear_button'])
        self.clear_button.setToolTip('Clear results (Ctrl+C)')
        self.clear_button.clicked.connect(self.clear_results)
        
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.resume_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.clear_button)
        
        # Theme and Language selection
        settings_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Windows', 'Windows 11 Light', 'Windows 11 Dark', 'Red', 'Blue', 'Custom'])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        settings_layout.addWidget(QLabel(TRANSLATIONS[self.language]['theme_label']))
        settings_layout.addWidget(self.theme_combo)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(['English', 'فارسی', '中文'])
        self.language_combo.currentTextChanged.connect(self.change_language)
        settings_layout.addWidget(QLabel(TRANSLATIONS[self.language]['language_label']))
        settings_layout.addWidget(self.language_combo)
        
        scan_layout.addLayout(button_layout)
        scan_layout.addLayout(settings_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        scan_layout.addWidget(self.progress_bar)
        
        # Results table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels([
            TRANSLATIONS[self.language]['ip'],
            TRANSLATIONS[self.language]['port'],
            TRANSLATIONS[self.language]['service'],
            TRANSLATIONS[self.language]['status'],
            TRANSLATIONS[self.language]['banner']
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        scan_layout.addWidget(QLabel(TRANSLATIONS[self.language]['results_label']))
        scan_layout.addWidget(self.results_table)
        
        self.tabs.addTab(scan_widget, 'Scan')
        
        # History Tab
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(['Timestamp', 'IP Range', 'Ports'])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.itemDoubleClicked.connect(self.load_history_scan)
        history_layout.addWidget(QLabel(TRANSLATIONS[self.language]['history_label']))
        history_layout.addWidget(self.history_table)
        self.tabs.addTab(history_widget, 'History')
        
        # Visualization Tab
        visualization_widget = QWidget()
        visualization_layout = QVBoxLayout(visualization_widget)
        self.canvas = PortDistributionCanvas(self)
        visualization_layout.addWidget(QLabel(TRANSLATIONS[self.language]['visualization_label']))
        visualization_layout.addWidget(self.canvas)
        self.tabs.addTab(visualization_widget, 'Visualization')
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.update_ui_direction()

    def setup_shortcuts(self):
        QShortcut(QKeySequence('Ctrl+S'), self, self.start_scan)
        QShortcut(QKeySequence('Ctrl+P'), self, self.pause_scan)
        QShortcut(QKeySequence('Ctrl+R'), self, self.resume_scan)
        QShortcut(QKeySequence('Ctrl+T'), self, self.stop_scan)
        QShortcut(QKeySequence('Ctrl+C'), self, self.clear_results)

    def update_ui_direction(self):
        direction = TRANSLATIONS[self.language]['direction']
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft if direction == 'rtl' else Qt.LayoutDirection.LeftToRight)
        for widget in [self.ip_input, self.port_input, self.results_table, self.history_table]:
            widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft if direction == 'rtl' else Qt.LayoutDirection.LeftToRight)

    def change_theme(self, theme):
        self.theme = theme
        app = QApplication.instance()
        palette = QPalette()
        
        if theme == 'Windows':
            app.setStyle('Windows')
            palette = app.style().standardPalette()
        elif theme == 'Windows 11 Light':
            app.setStyle('Fusion')
            palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        elif theme == 'Windows 11 Dark':
            app.setStyle('Fusion')
            palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        elif theme == 'Red':
            app.setStyle('Fusion')
            palette.setColor(QPalette.ColorRole.Window, QColor(50, 0, 0))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(70, 0, 0))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        elif theme == 'Blue':
            app.setStyle('Fusion')
            palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 50))
            palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
            palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 70))
            palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        elif theme == 'Custom':
            dialog = CustomThemeDialog(self, self.language)
            if dialog.exec():
                palette.setColor(QPalette.ColorRole.Window, dialog.colors['window'])
                palette.setColor(QPalette.ColorRole.WindowText, dialog.colors['window_text'])
                palette.setColor(QPalette.ColorRole.Base, dialog.colors['base'])
                palette.setColor(QPalette.ColorRole.Text, dialog.colors['text'])
            else:
                self.theme_combo.setCurrentText('Windows')
                return
        
        app.setPalette(palette)

    def custom_theme(self):
        self.theme_combo.setCurrentText('Custom')
        self.change_theme('Custom')

    def change_language(self, language):
        if language == 'English':
            self.language = 'en'
        elif language == 'فارسی':
            self.language = 'fa'
        elif language == '中文':
            self.language = 'zh'
            
        self.update_ui_text()
        self.update_ui_direction()
        self.canvas.figure.axes[0].set_title(TRANSLATIONS[self.language]['visualization_label'])

    def update_ui_text(self):
        self.setWindowTitle(TRANSLATIONS[self.language]['title'])
        self.scan_button.setText(TRANSLATIONS[self.language]['scan_button'])
        self.pause_button.setText(TRANSLATIONS[self.language]['pause_button'])
        self.resume_button.setText(TRANSLATIONS[self.language]['resume_button'])
        self.stop_button.setText(TRANSLATIONS[self.language]['stop_button'])
        self.clear_button.setText(TRANSLATIONS[self.language]['clear_button'])
        self.results_table.setHorizontalHeaderLabels([
            TRANSLATIONS[self.language]['ip'],
            TRANSLATIONS[self.language]['port'],
            TRANSLATIONS[self.language]['service'],
            TRANSLATIONS[self.language]['status'],
            TRANSLATIONS[self.language]['banner']
        ])
        self.history_table.setHorizontalHeaderLabels(['Timestamp', 'IP Range', 'Ports'])
        self.tabs.setTabText(0, 'Scan')
        self.tabs.setTabText(1, 'History')
        self.tabs.setTabText(2, 'Visualization')
        
        menubar = self.menuBar()
        menubar.clear()
        settings_menu = menubar.addMenu(TRANSLATIONS[self.language]['settings_menu'])
        save_action = QAction(TRANSLATIONS[self.language]['save_config'], self)
        save_action.triggered.connect(self.save_config)
        load_action = QAction(TRANSLATIONS[self.language]['load_config'], self)
        load_action.triggered.connect(self.load_config)
        export_action = QAction(TRANSLATIONS[self.language]['export_results'], self)
        export_action.triggered.connect(self.export_results)
        custom_theme_action = QAction(TRANSLATIONS[self.language]['custom_theme'], self)
        custom_theme_action.triggered.connect(self.custom_theme)
        about_action = QAction(TRANSLATIONS[self.language]['about'], self)
        about_action.triggered.connect(self.show_about)
        
        settings_menu.addAction(save_action)
        settings_menu.addAction(load_action)
        settings_menu.addAction(export_action)
        settings_menu.addAction(custom_theme_action)
        settings_menu.addAction(about_action)

    def validate_ip_input(self):
        ip_input = self.ip_input.text()
        is_valid = bool(re.match(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2})?)$', ip_input))
        self.ip_input.setStyleSheet('' if is_valid else 'border: 1px solid red')

    def validate_port_input(self):
        port_input = self.port_input.text()
        is_valid = bool(re.match(r'^(\d{1,5}(?:-\d{1,5})?|\d{1,5}(?:,\d{1,5})*)$', port_input))
        self.port_input.setStyleSheet('' if is_valid else 'border: 1px solid red')

    def validate_ip(self, ip_input):
        try:
            if '/' in ip_input:
                network = ipaddress.ip_network(ip_input, strict=False)
                return [str(ip) for ip in network]
            else:
                ipaddress.ip_address(ip_input)
                return [ip_input]
        except ValueError:
            return None

    def validate_ports(self, port_input):
        try:
            if '-' in port_input:
                start, end = map(int, port_input.split('-'))
                if 1 <= start <= end <= 65535:
                    return list(range(start, end + 1))
            else:
                ports = [int(p) for p in port_input.split(',')]
                if all(1 <= p <= 65535 for p in ports):
                    return ports
            return None
        except ValueError:
            return None

    def apply_scan_profile(self, profile):
        if profile != 'Custom':
            self.port_input.setText(SCAN_PROFILES[profile])

    def start_scan(self):
        ip_input = self.ip_input.text()
        port_input = self.port_input.text()
        
        ip_list = self.validate_ip(ip_input)
        port_list = self.validate_ports(port_input)
        
        if not ip_list:
            QMessageBox.critical(self, TRANSLATIONS[self.language]['error'],
                               TRANSLATIONS[self.language]['invalid_ip'])
            return
        if not port_list:
            QMessageBox.critical(self, TRANSLATIONS[self.language]['error'],
                               TRANSLATIONS[self.language]['invalid_port'])
            return

        settings_dialog = SettingsDialog(self, self.language)
        if not settings_dialog.exec():
            return

        timeout = settings_dialog.timeout_input.value()
        threads = settings_dialog.threads_input.value()
        interface = settings_dialog.interface_combo.currentText() if settings_dialog.interface_combo.currentText() != 'Auto' and NETIFACES_AVAILABLE else None

        self.scan_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.results_table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.open_ports = []
        self.status_bar.showMessage(TRANSLATIONS[self.language]['scanning'])

        self.task_queue = queue.Queue()
        self.total_tasks = len(ip_list) * len(port_list)
        self.completed_tasks = 0
        
        for ip in ip_list:
            for port in port_list:
                self.task_queue.put((ip, port))

        self.scan_threads = []
        for _ in range(threads):
            thread = ScanThread(ip_list, port_list, timeout, self.task_queue, interface)
            thread.scan_result.connect(self.add_result)
            thread.progress.connect(self.update_progress)
            thread.finished.connect(self.thread_finished)
            thread.error.connect(self.show_error)
            self.scan_threads.append(thread)
            thread.start()

        # Save to history
        self.scan_history.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_range': ip_input,
            'ports': port_input
        })
        self.update_history_table()

    def add_result(self, ip, port, service, status, banner):
        if status == 'Open':
            self.open_ports.append(port)
            self.canvas.update_plot(self.open_ports)
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        self.results_table.setItem(row, 0, QTableWidgetItem(ip))
        self.results_table.setItem(row, 1, QTableWidgetItem(str(port)))
        self.results_table.setItem(row, 2, QTableWidgetItem(service))
        self.results_table.setItem(row, 3, QTableWidgetItem(status))
        self.results_table.setItem(row, 4, QTableWidgetItem(banner))
        logging.info(f"Scan result: IP={ip}, Port={port}, Service={service}, Status={status}, Banner={banner}")

    def update_progress(self):
        self.completed_tasks += 1
        progress = (self.completed_tasks / self.total_tasks) * 100
        self.progress_bar.setValue(int(progress))

    def thread_finished(self):
        if all(not thread.is_running for thread in self.scan_threads):
            self.scan_button.setEnabled(True)
            self.pause_button.setEnabled(False)
            self.resume_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status_bar.showMessage(TRANSLATIONS[self.language]['completed'])
            self.canvas.update_plot(self.open_ports)

    def show_error(self, error_msg):
        QMessageBox.critical(self, TRANSLATIONS[self.language]['error'], error_msg)
        logging.error(f"Error: {error_msg}")

    def pause_scan(self):
        self.is_paused = True
        for thread in self.scan_threads:
            thread.pause()
        self.scan_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(True)
        self.stop_button.setEnabled(True)
        self.status_bar.showMessage(TRANSLATIONS[self.language]['paused'])

    def resume_scan(self):
        self.is_paused = False
        for thread in self.scan_threads:
            thread.resume()
        self.scan_button.setEnabled(False)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_bar.showMessage(TRANSLATIONS[self.language]['resumed'])

    def stop_scan(self):
        for thread in self.scan_threads:
            thread.stop()
        self.scan_button.setEnabled(True)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.status_bar.showMessage(TRANSLATIONS[self.language]['stopped'])
        self.canvas.update_plot(self.open_ports)

    def clear_results(self):
        self.results_table.setRowCount(0)
        self.progress_bar.setValue(0)
        self.open_ports = []
        self.canvas.update_plot([])
        self.status_bar.showMessage('')

    def update_history_table(self):
        self.history_table.setRowCount(0)
        for scan in self.scan_history:
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            self.history_table.setItem(row, 0, QTableWidgetItem(scan['timestamp']))
            self.history_table.setItem(row, 1, QTableWidgetItem(scan['ip_range']))
            self.history_table.setItem(row, 2, QTableWidgetItem(scan['ports']))

    def load_history_scan(self, item):
        row = item.row()
        scan = self.scan_history[row]
        self.ip_input.setText(scan['ip_range'])
        self.port_input.setText(scan['ports'])
        self.tabs.setCurrentIndex(0)

    def save_config(self):
        config = {
            'ip': self.ip_input.text(),
            'ports': self.port_input.text(),
            'theme': self.theme_combo.currentText(),
            'language': self.language_combo.currentText()
        }
        try:
            with open('scanner_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)
            self.status_bar.showMessage(TRANSLATIONS[self.language]['config_saved'])
            logging.info("Configuration saved")
        except Exception as e:
            self.show_error(str(e))

    def load_config(self):
        try:
            if os.path.exists('scanner_config.json'):
                with open('scanner_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.ip_input.setText(config.get('ip', ''))
                self.port_input.setText(config.get('ports', ''))
                self.theme_combo.setCurrentText(config.get('theme', 'Windows'))
                self.language_combo.setCurrentText(config.get('language', 'English'))
                self.status_bar.showMessage(TRANSLATIONS[self.language]['config_loaded'])
                logging.info("Configuration loaded")
        except Exception as e:
            self.show_error(str(e))

    def export_results(self):
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            formats = ['CSV', 'JSON', 'XML']
            format_dialog = QDialog(self)
            format_layout = QVBoxLayout()
            format_combo = QComboBox()
            format_combo.addItems(formats)
            format_button = QPushButton('Export')
            format_layout.addWidget(QLabel('Select export format:'))
            format_layout.addWidget(format_combo)
            format_layout.addWidget(format_button)
            format_dialog.setLayout(format_layout)
            
            def export_selected():
                fmt = format_combo.currentText()
                filename = f'scan_results_{timestamp}.{fmt.lower()}'
                if fmt == 'CSV':
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('IP,Port,Service,Status,Banner\n')
                        for row in range(self.results_table.rowCount()):
                            items = [self.results_table.item(row, col).text() 
                                    for col in range(self.results_table.columnCount())]
                            f.write(','.join(items) + '\n')
                elif fmt == 'JSON':
                    results = []
                    for row in range(self.results_table.rowCount()):
                        results.append({
                            'ip': self.results_table.item(row, 0).text(),
                            'port': self.results_table.item(row, 1).text(),
                            'service': self.results_table.item(row, 2).text(),
                            'status': self.results_table.item(row, 3).text(),
                            'banner': self.results_table.item(row, 4).text()
                        })
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(results, f, ensure_ascii=False, indent=2)
                elif fmt == 'XML':
                    root = ET.Element('scan_results')
                    for row in range(self.results_table.rowCount()):
                        result = ET.SubElement(root, 'result')
                        ET.SubElement(result, 'ip').text = self.results_table.item(row, 0).text()
                        ET.SubElement(result, 'port').text = self.results_table.item(row, 1).text()
                        ET.SubElement(result, 'service').text = self.results_table.item(row, 2).text()
                        ET.SubElement(result, 'status').text = self.results_table.item(row, 3).text()
                        ET.SubElement(result, 'banner').text = self.results_table.item(row, 4).text()
                    tree = ET.ElementTree(root)
                    tree.write(filename, encoding='utf-8', xml_declaration=True)
                self.status_bar.showMessage(TRANSLATIONS[self.language]['results_saved'].format(filename))
                format_dialog.accept()
                logging.info(f"Results exported to {filename}")

            format_button.clicked.connect(export_selected)
            format_dialog.exec()
        except Exception as e:
            self.show_error(str(e))

    def show_about(self):
        QMessageBox.information(self, TRANSLATIONS[self.language]['about'],
                              TRANSLATIONS[self.language]['about_text'])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon('port_scanner.jpg'))  # Set application favicon
    scanner = PortScanner()
    scanner.show()
    sys.exit(app.exec())