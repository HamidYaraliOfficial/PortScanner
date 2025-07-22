# Advanced Network Port Scanner

## English

### Overview
The **Advanced Network Port Scanner** is a powerful, user-friendly tool built with PyQt6 for scanning network ports. It supports scanning IP addresses or ranges, customizable port ranges, and provides detailed results including service detection and banner grabbing. The application features a multilingual interface (English, Persian, Chinese), multiple themes, scan history, and port distribution visualization.

### Features
- **IP and Port Range Scanning**: Scan single IPs or CIDR ranges (e.g., 192.168.1.0/24) and specify port ranges or individual ports.
- **Service Detection**: Identifies common services (e.g., HTTP, FTP, SSH) for open ports.
- **Banner Grabbing**: Retrieves service banners for open ports.
- **Multithreading**: Configurable thread count for faster scanning.
- **Network Interface Selection**: Optional support for selecting network interfaces (requires `netifaces`).
- **Multilingual Support**: Interface available in English, Persian, and Chinese with RTL/LTR layout adjustments.
- **Theming**: Built-in themes (Windows, Windows 11 Light/Dark, Red, Blue, Custom) with customizable colors.
- **Scan History**: Stores previous scans for quick access and re-running.
- **Visualization**: Displays port distribution using Matplotlib.
- **Export Results**: Save scan results in CSV, JSON, or XML formats.
- **Configuration Management**: Save and load scan configurations.
- **Logging**: Detailed logging of scan activities and errors.

### Requirements
- Python 3.7+
- PyQt6
- psutil
- matplotlib
- netifaces (optional, for network interface selection)
- A favicon image named `port_scanner.jpg` in the project directory

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/HamidYaraliOfficial/PortScanner.git
   cd PortScanner
   ```
2. Install dependencies:
   ```bash
   pip install pyqt6 psutil matplotlib netifaces
   ```
3. Ensure `port_scanner.jpg` is in the project directory for the favicon.
4. Run the application:
   ```bash
   python port_scanner.py
   ```

### Usage
1. **Input IP and Ports**:
   - Enter an IP address or range (e.g., `192.168.1.1` or `192.168.1.0/24`).
   - Specify ports (e.g., `80,443` or `1-65535`) or select a scan profile (e.g., Common, Web, Database).
2. **Configure Settings**:
   - Adjust timeout, thread count, and network interface (if `netifaces` is installed) in the settings dialog.
3. **Start Scan**:
   - Click "Start Scan" or use `Ctrl+S` to begin scanning.
   - Pause (`Ctrl+P`), resume (`Ctrl+R`), or stop (`Ctrl+T`) the scan as needed.
4. **View Results**:
   - Results appear in the table with IP, port, service, status, and banner.
   - View scan history in the "History" tab or port distribution in the "Visualization" tab.
5. **Export and Configure**:
   - Export results via the "Export Results" menu (`CSV`, `JSON`, `XML`).
   - Save/load configurations or customize themes via the "Settings" menu.

### Screenshots
*(Add screenshots of the application here for better documentation)*

### Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.

### License
This project is licensed under the MIT License.

---

## فارسی

### بررسی اجمالی
**اسکنر پیشرفته پورت شبکه** یک ابزار قدرتمند و کاربرپسند است که با استفاده از PyQt6 برای اسکن پورت‌های شبکه توسعه یافته است. این ابزار از اسکن آدرس‌های IP یا محدوده‌ها، محدوده‌های پورت قابل تنظیم و ارائه نتایج دقیق شامل شناسایی سرویس و دریافت بنر پشتیبانی می‌کند. برنامه دارای رابط کاربری چندزبانه (انگلیسی، فارسی، چینی)، تم‌های متعدد، تاریخچه اسکن و تجسم توزیع پورت‌ها است.

### ویژگی‌ها
- **اسکن IP و محدوده پورت**: اسکن آدرس‌های IP تکی یا محدوده‌های CIDR (مانند 192.168.1.0/24) و تعیین محدوده پورت یا پورت‌های خاص.
- **شناسایی سرویس**: شناسایی سرویس‌های رایج (مانند HTTP، FTP، SSH) برای پورت‌های باز.
- **دریافت بنر**: دریافت بنر سرویس برای پورت‌های باز.
- **چندنخی**: تعداد نخ‌های قابل تنظیم برای اسکن سریع‌تر.
- **انتخاب رابط شبکه**: پشتیبانی اختیاری برای انتخاب رابط‌های شبکه (نیازمند `netifaces`).
- **پشتیبانی چندزبانه**: رابط کاربری به زبان‌های انگلیسی، فارسی و چینی با تنظیمات چیدمان راست‌به‌چپ/چپ‌به‌راست.
- **تم‌ها**: تم‌های داخلی (ویندوز، ویندوز 11 روشن/تیره، قرمز، آبی، سفارشی) با رنگ‌های قابل تنظیم.
- **تاریخچه اسکن**: ذخیره اسکن‌های قبلی برای دسترسی سریع و اجرای مجدد.
- **تجسم**: نمایش توزیع پورت‌ها با استفاده از Matplotlib.
- **خروجی نتایج**: ذخیره نتایج اسکن در فرمت‌های CSV، JSON یا XML.
- **مدیریت تنظیمات**: ذخیره و بارگذاری تنظیمات اسکن.
- **لاگ‌گیری**: ثبت دقیق فعالیت‌ها و خطاهای اسکن.

### پیش‌نیازها
- Python 3.7+
- PyQt6
- psutil
- matplotlib
- netifaces (اختیاری، برای انتخاب رابط شبکه)
- تصویر favicon با نام `port_scanner.jpg` در پوشه پروژه

### نصب
1. کلون کردن مخزن:
   ```bash
   git clone https://github.com/HamidYaraliOfficial/PortScanner.git
   cd PortScanner
   ```
2. نصب وابستگی‌ها:
   ```bash
   pip install pyqt6 psutil matplotlib netifaces
   ```
3. اطمینان حاصل کنید که فایل `port_scanner.jpg` در پوشه پروژه برای favicon موجود است.
4. اجرای برنامه:
   ```bash
   python port_scanner.py
   ```

### استفاده
1. **وارد کردن IP و پورت‌ها**:
   - آدرس IP یا محدوده (مانند `192.168.1.1` یا `192.168.1.0/24`) را وارد کنید.
   - پورت‌ها را مشخص کنید (مانند `80,443` یا `1-65535`) یا یک پروفایل اسکن (مانند Common، Web، Database) انتخاب کنید.
2. **پیکربندی تنظیمات**:
   - در پنجره تنظیمات، زمان‌بندی، تعداد نخ‌ها و رابط شبکه (در صورت نصب `netifaces`) را تنظیم کنید.
3. **شروع اسکن**:
   - روی «شروع اسکن» کلیک کنید یا از `Ctrl+S` استفاده کنید.
   - اسکن را با `Ctrl+P` متوقف کنید، با `Ctrl+R` ادامه دهید یا با `Ctrl+T` متوقف کنید.
4. **مشاهده نتایج**:
   - نتایج در جدول با IP، پورت، سرویس، وضعیت و بنر نمایش داده می‌شود.
   - تاریخچه اسکن را در تب «تاریخچه» یا توزیع پورت‌ها را در تب «تجسم» مشاهده کنید.
5. **خروجی و تنظیمات**:
   - نتایج را از طریق منوی «خروجی نتایج» به فرمت‌های `CSV`، `JSON` یا `XML` ذخیره کنید.
   - تنظیمات را ذخیره/بارگذاری کنید یا تم‌ها را از طریق منوی «تنظیمات» سفارشی کنید.

### تصاویر
*(تصاویر برنامه را برای مستندسازی بهتر اینجا اضافه کنید)*

### مشارکت
مشارکت‌ها مورد استقبال قرار می‌گیرند! لطفاً درخواست کشیدن (pull request) ارسال کنید یا برای پیشنهادات یا گزارش خطاها، مسئله‌ای (issue) باز کنید.

### مجوز
این پروژه تحت مجوز MIT منتشر شده است.

---

## 中文

### 概述
**高级网络端口扫描器** 是一个功能强大、用户友好的工具，使用 PyQt6 开发，用于扫描网络端口。它支持扫描单个 IP 或范围、可自定义的端口范围，并提供包括服务检测和横幅抓取的详细结果。应用程序具有多语言界面（英语、波斯语、汉语），支持多种主题、扫描历史记录和端口分布可视化。

### 功能
- **IP 和端口范围扫描**：扫描单个 IP 或 CIDR 范围（如 192.168.1.0/24），并指定端口范围或单个端口。
- **服务检测**：识别开放端口的常见服务（如 HTTP、FTP、SSH）。
- **横幅抓取**：获取开放端口的服务横幅。
- **多线程**：可配置线程数以加快扫描速度。
- **网络接口选择**：支持选择网络接口（需要 `netifaces`）。
- **多语言支持**：支持英语、波斯语和汉语界面，自动调整 RTL/LTR 布局。
- **主题**：内置主题（Windows、Windows 11 亮/暗、红色、蓝色、自定义），支持自定义颜色。
- **扫描历史**：保存之前的扫描记录以便快速访问和重新运行。
- **可视化**：使用 Matplotlib 显示端口分布。
- **导出结果**：以 CSV、JSON 或 XML 格式保存扫描结果。
- **配置管理**：保存和加载扫描配置。
- **日志记录**：详细记录扫描活动和错误。

### 依赖项
- Python 3.7+
- PyQt6
- psutil
- matplotlib
- netifaces（可选，用于网络接口选择）
- 项目目录中名为 `port_scanner.jpg` 的 favicon 图片

### 安装
1. 克隆仓库：
   ```bash
   git clone https://github.com/HamidYaraliOfficial/PortScanner.git
   cd PortScanner
   ```
2. 安装依赖项：
   ```bash
   pip install pyqt6 psutil matplotlib netifaces
   ```
3. 确保项目目录中存在 `port_scanner.jpg` 文件作为 favicon。
4. 运行应用程序：
   ```bash
   python port_scanner.py
   ```

### 使用方法
1. **输入 IP 和端口**：
   - 输入 IP 地址或范围（如 `192.168.1.1` 或 `192.168.1.0/24`）。
   - 指定端口（如 `80,443` 或 `1-65535`）或选择扫描配置文件（如 Common、Web、Database）。
2. **配置设置**：
   - 在设置对话框中调整超时、线程数和网络接口（需安装 `netifaces`）。
3. **开始扫描**：
   - 点击“开始扫描”或使用 `Ctrl+S` 开始扫描。
   - 使用 `Ctrl+P` 暂停，`Ctrl+R` 恢复，或 `Ctrl+T` 停止扫描。
4. **查看结果**：
   - 结果显示在表格中，包括 IP、端口、服务、状态和横幅。
   - 在“历史”选项卡中查看扫描历史，或在“可视化”选项卡中查看端口分布。
5. **导出和配置**：
   - 通过“导出结果”菜单将结果保存为 `CSV`、`JSON` 或 `XML` 格式。
   - 通过“设置”菜单保存/加载配置或自定义主题。

### 截图
*(在此处添加应用程序截图以完善文档)*

### 贡献
欢迎贡献！请提交拉取请求或开启问题以提供建议或报告错误。

### 许可证
本项目采用 MIT 许可证。