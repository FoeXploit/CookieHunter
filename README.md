# 🍪 Cookie Hunter Advanced v2.4 – Foe Edition

**Cookie Hunter Advanced** – умный GUI‑инструмент для обработки и конвертации куки‑логов в формате Netscape (стилеры: RedLine, Vidar, Raccoon и др.)  
*Smart GUI tool for processing and converting Netscape-format cookie logs (stealers: RedLine, Vidar, Raccoon, etc.).*

---

## 🇷🇺 РУССКИЙ

### 📖 Описание

**Cookie Hunter Advanced** позволяет превращать сырые `.txt`‑логи с куками в два удобных формата:

- **JSON (Cookie‑Editor)** – готов к импорту в расширение браузера.
- **Netscape (.txt)** – очищенный, отфильтрованный и разложенный по папкам.

Инструмент фильтрует логи по сервисам (Outlook, Google, Facebook), разделяет куки по доменам и даже разделяет разные компьютеры (жертвы) – по папкам или по внутренним заголовкам `# Netscape HTTP Cookie File`.

### 🔧 Основные возможности

- **Фильтрация по сервисам** – встроенные шаблоны доменов:
  - Outlook / Live / Hotmail
  - Google
  - Facebook
  - *Свой список доменов* (через запятую)
- **Разделение по компьютерам** – три режима:
  1. Каждая папка = один компьютер (если логи уже разложены по жертвам)
  2. Разделение по заголовкам Netscape внутри одного `.txt` (когда стилер скидывает несколько профилей в один файл)
  3. Без разделения – все куки сливаются в один файл
- **Разделение по доменам** – создаёт отдельную папку с файлами для каждого домена.
- **Рекурсивный поиск** – сканирует все `.txt` внутри выбранной папки и подпапок.
- **Современный интерфейс** – тёмная тема, прогресс-бар, живой лог.
- **Пакетный экспорт** – все выбранные компьютеры обрабатываются за один запуск.

### 📥 Установка (Windows)

Код распространяется напрямую – клонировать репозиторий не требуется.

1. **Установите Python 3.9+** (проверено до 3.12).  
   Скачайте с [python.org](https://python.org), при установке отметьте **“Add Python to PATH”**.

2. **Установите PyQt6**:
   ```bash
   pip install PyQt6
(Рекомендуется виртуальное окружение, но не обязательно.)

Сохраните скрипт – скопируйте код из файла cookie_hunter.py (приложен в репозитории или в теле поста) и сохраните его на своём компьютере как cookie_hunter.py.

Опционально: ресурсные файлы – если хотите использовать кастомный шрифт и иконку, создайте рядом со скриптом папки:

text
data/
├── fonts/
│   └── UbuntuMono-Regular.ttf
└── icons/
    └── app.ico
Если папка data отсутствует, инструмент заработает и без неё – со стандартным системным шрифтом и без иконки окна.

Запуск:

bash
python cookie_hunter.py
При первом запуске автоматически создастся папка Result для вывода.

🚀 Как пользоваться
Откройте программу – появится тёмное окно.

Выберите формат вывода: JSON (Cookie‑Editor) или Netscape (.txt).

Фильтр по сервису (по желанию) – выберите предустановленный, Custom (введите свои домены через запятую) или All cookies чтобы не фильтровать.

Режим разделения по компьютерам:

Каждая папка = компьютер – выберите основную папку, внутри которой лежат подпапки с логами отдельных жертв.

Разделение по заголовкам Netscape – выберите папку с .txt; инструмент сам найдёт строки # Netscape HTTP Cookie File и разделит разные машины.

Без разделения – все куки собираются в один файл.

Отметьте Recursive search (рекурсивный поиск, включён по умолчанию) и Split by domain (разбивка по доменам).

Нажмите “VÄLJ MAPP MED LOGGFILER” (Выбрать папку с логами).

Дождитесь обработки – прогресс-бар покажет процесс. Результат появится в папке Result/Result-[случайный код].

Откройте папку результата и импортируйте JSON через расширение Cookie‑Editor (Import → Select file) либо Netscape через любой менеджер кук.

📁 Пример выходной структуры
При выборе Каждая папка = компьютер и Разделение по доменам:

text
Result/Result-[ABCDEFGHIJKL]/
├── Outlook-COMP1.json
├── domain_split_COMP1/
│   ├── login.live.com.json
│   ├── account.microsoft.com.json
│   └── ...
├── Outlook-COMP2.json
├── domain_split_COMP2/
│   └── ...
⚠️ Важно
Только Windows – тестировалось на Win 10/11.

Инструмент не отправляет никаких данных в сеть, всё работает локально.

Ошибка IndexError при старте означает отсутствие папки data – создайте пустую папку data/ или просто игнорируйте.

🇬🇧 ENGLISH
📖 Description
Cookie Hunter Advanced converts raw Netscape-format cookie logs into two practical formats:

JSON (Cookie‑Editor) – ready to import into the browser extension.

Netscape (.txt) – clean, filtered, and organised for direct use.

It provides service filtering (Outlook, Google, Facebook), per‑computer splitting, and per‑domain splitting to quickly isolate valuable accounts.

🔧 Key Features
Service Filtering – built‑in domain patterns for:

Outlook / Live / Hotmail

Google

Facebook

Custom domain list (comma‑separated)

Per‑Computer Splitting – three modes:

Each subfolder = one computer (logs already sorted by victim)
Split by # Netscape HTTP Cookie File headers inside a single .txt
No split – all cookies merged into one output file
Per‑Domain Splitting – creates a separate subfolder with one file per domain.

Recursive Search – scans all .txt files in selected folder and subfolders.

Modern GUI – dark theme, progress bar, real‑time log.

Batch Export – all selected computers are processed in one run.

📥 Installation (Windows)
The code is shared directly – no repository cloning required.

Install Python 3.9+ (tested up to 3.12).
Download from python.org and check “Add Python to PATH”.

Install PyQt6:

bash
pip install PyQt6
(A virtual environment is recommended but not required.)

Save the script – copy the code from cookie_hunter.py (included in the repository or the post) and save it as cookie_hunter.py on your computer.

Optional: resource files – for a custom font and icon, create these folders next to the script:

text
data/
├── fonts/
│   └── UbuntuMono-Regular.ttf
└── icons/
    └── app.ico
If the data folder is missing, the GUI will still work with the default system font and no window icon.

Run the tool:

bash
python cookie_hunter.py
A Result folder will be created automatically on first run.

🚀 How to Use
Launch the program – a dark window appears.

Choose Output format: JSON (Cookie‑Editor) or Netscape (.txt).

Filter by service (optional) – pick a pre‑defined service, Custom (enter your own domains), or All cookies for no filter.

Computer split mode:

Each folder = a computer – select a main folder that contains one subfolder per victim.

Split by # Netscape headers – select a folder with .txt files; the tool splits by # Netscape HTTP Cookie File lines.

No split – all cookies are merged into one output file.

Check Recursive search (enabled by default) and Split by domain.

Click “VÄLJ MAPP MED LOGGFILER” (Select folder with log files).

Wait for processing – the progress bar shows the current progress. Output will be inside Result/Result-[random].

Open the result folder and import JSON files via Cookie‑Editor (Import → Select file), or load Netscape files into any cookie manager.

📁 Output Structure Example
Choosing Each folder = a computer and Split by domain results in:

text
Result/Result-[ABCDEFGHIJKL]/
├── Outlook-COMP1.json
├── domain_split_COMP1/
│   ├── login.live.com.json
│   ├── account.microsoft.com.json
│   └── ...
├── Outlook-COMP2.json
├── domain_split_COMP2/
│   └── ...
Each file is ready to be imported via Cookie‑Editor.

⚠️ Notes
Windows only – tested on Windows 10/11.

The tool does not send any data anywhere. All processing is local.

If you get an IndexError on start, the data folder is missing – create an empty data/ folder or ignore the error.

📢 Contacts & Updates
GitHub: https://github.com/FoeXploit

Telegram: https://t.me/Foe121

По вопросам, багам или пожеланиям – пишите. / For bugs, questions, or suggestions – feel free to reach out.
