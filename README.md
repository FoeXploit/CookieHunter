# 🍪 Cookie Hunter Advanced v2.4 – Foe Edition

**Cookie Hunter Advanced** is a smart GUI tool for processing and converting Netscape-format cookie logs (stealers: RedLine, Vidar, Raccoon, etc.).  
*Умный GUI‑инструмент для обработки и конвертации куки‑логов в формате Netscape (стилеры: RedLine, Vidar, Raccoon и др.).*

---

## 🇬🇧 ENGLISH

### 📖 Description

**Cookie Hunter Advanced** converts raw `.txt` cookie logs into two practical formats:

- **JSON (Cookie-Editor)** – ready to import into the browser extension.
- **Netscape (.txt)** – clean, filtered, and organised for direct use.

It provides service filtering (Outlook, Google, Facebook), per‑computer splitting, and per‑domain splitting to quickly isolate valuable accounts.

### 🔧 Key Features

- **Service Filtering** – built‑in domain patterns for:
  - Outlook / Live / Hotmail
  - Google
  - Facebook
  - *Custom domain list* (comma‑separated)
- **Per‑Computer Splitting** – three modes:
  1. Each subfolder = one computer (logs already sorted by victim)
  2. Split by `# Netscape HTTP Cookie File` headers inside a single `.txt`
  3. No split – all cookies merged into one output file
- **Per‑Domain Splitting** – creates a separate subfolder with one file per domain.
- **Recursive Search** – scans all `.txt` files in selected folder and subfolders.
- **Modern GUI** – dark theme, progress bar, real‑time log.
- **Batch Export** – all selected computers are processed in one run.

### 📥 Installation (Windows)

1. **Install Python 3.9+** (tested up to 3.12).  
   Download from [python.org](https://python.org) and check **“Add Python to PATH”**.

2. **Clone the repository** or download the script and the `data` folder.  
   ```bash
   git clone https://github.com/FoeXploit/CookieHunter.git
   cd CookieHunter
   ```
   If you don’t use Git, simply download the ZIP from the repo and extract it.

3. **Install PyQt6**:
   ```bash
   pip install PyQt6
   ```
   (A virtual environment is recommended but not required.)

4. **Ensure the folder structure** looks like this:
   ```
   CookieHunter/
   ├── cookie_hunter.py        (main script)
   ├── data/
   │   ├── fonts/
   │   │   └── UbuntuMono-Regular.ttf
   │   └── icons/
   │       └── app.ico
   └── Result/                 (created automatically on first run)
   ```
   The `data` folder is optional – the GUI will still work, just with the default system font and no icon.

5. **Run the tool**:
   ```bash
   python cookie_hunter.py
   ```

### 🚀 How to Use

1. Launch the program – a dark window appears.
2. Choose **Output format**: JSON (Cookie‑Editor) or Netscape (.txt).
3. **Filter by service** (optional) – pick a pre‑defined service, *Custom* and enter your own domains, or *All cookies* for no filter.
4. **Computer split mode**:
   - *Each folder = a computer* – select a main folder that contains one subfolder per victim (each subfolder with their `.txt` files).
   - *Split by # Netscape headers* – select a folder with `.txt` files; the tool looks for `# Netscape HTTP Cookie File` lines to separate different computers.
   - *No split* – all cookies from all files are merged into one output.
5. Check **Recursive search** (enabled by default) and **Split by domain** (creates individual files per site).
6. Click **“SELECT FOLDER WITH LOG FILES”**.
7. Wait for processing – the progress bar shows the current progress. Output goes into the `Result/Result-[random]` folder.
8. Open the result folder and import the JSON files with the **Cookie‑Editor** extension or load the Netscape files into any cookie manager.

### 📁 Output Structure Example

If you choose *Each folder = a computer* and *Split by domain*, the output will look like:

```
Result/Result-[ABCDEFGHIJKL]/
├── Outlook-COMP1.json          (merged JSON for the first computer, Outlook cookies)
├── domain_split_COMP1/
│   ├── login.live.com.json
│   ├── account.microsoft.com.json
│   └── ...
├── Outlook-COMP2.json
├── domain_split_COMP2/
│   └── ...
```

Each file is ready to be imported via **Cookie‑Editor** → Import → select file.

### ⚠️ Notes

- **Windows only** – tested on Windows 10/11. Mac/Linux users may run into path issues (PRs welcome).
- The tool **does not** log, steal, or send any data anywhere. All processing happens locally.
- If you get an `IndexError` on start, it’s because the `data` folder is missing – it’s safe to ignore or just create an empty `data/` folder.

---

## 🇷🇺 РУССКИЙ

### 📖 Описание

**Cookie Hunter Advanced** позволяет превращать сырые `.txt`‑логи с куками в два удобных формата:

- **JSON (Cookie‑Editor)** – готов к импорту в расширение браузера.
- **Netscape (.txt)** – очищенный, отфильтрованный и разложенный по папкам.

Инструмент умеет фильтровать логи по сервисам (Outlook, Google, Facebook), разделять куки по доменам и даже разделять разные компьютеры (жертвы) – по папкам или по внутренним заголовкам `# Netscape HTTP Cookie File`.

### 🔧 Основные возможности

- **Фильтрация по сервисам** – встроенные шаблоны доменов для:
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

1. **Установите Python 3.9+** (проверено до 3.12).  
   Скачайте с [python.org](https://python.org), при установке отметьте **“Add Python to PATH”**.

2. **Скачайте скрипт и папку `data`** (клонируйте репозиторий или просто возьмите ZIP).  
   ```bash
   git clone https://github.com/FoeXploit/CookieHunter.git
   cd CookieHunter
   ```
   Если Git не используется, скачайте архив и распакуйте.

3. **Установите PyQt6**:
   ```bash
   pip install PyQt6
   ```
   (рекомендуется виртуальное окружение, но не обязательно)

4. **Проверьте структуру папок** – должно быть так:
   ```
   CookieHunter/
   ├── cookie_hunter.py
   ├── data/
   │   ├── fonts/
   │   │   └── UbuntuMono-Regular.ttf
   │   └── icons/
   │       └── app.ico
   └── Result/          (создастся автоматически при первом запуске)
   ```
   Папка `data` не обязательна – без неё GUI заработает, но со стандартным шрифтом и без иконки.

5. **Запуск**:
   ```bash
   python cookie_hunter.py
   ```

### 🚀 Как пользоваться

1. Откройте программу – появится тёмное окно.
2. Выберите **формат вывода**: JSON (Cookie‑Editor) или Netscape (.txt).
3. **Фильтр по сервису** (по желанию) – выберите предустановленный, либо *Custom* и введите свои домены через запятую, или *All cookies* чтобы не фильтровать.
4. **Режим разделения по компьютерам**:
   - *Каждая папка = компьютер* – выберите основную папку, внутри которой лежат подпапки с логами отдельных жертв.
   - *Разделение по заголовкам Netscape* – выберите папку с `.txt`, а инструмент сам найдёт `# Netscape HTTP Cookie File` и разделит разные машины.
   - *Без разделения* – все куки собираются в один файл.
5. Отметьте **Recursive search** (рекурсивный поиск, включён по умолчанию) и **Split by domain** (разбивка по доменам).
6. Нажмите **“SELECT FOLDER WITH LOG FILES”** (Выбрать папку с логами).
7. Дождитесь обработки – прогресс-бар покажет процесс. Весь результат появится в папке `Result/Result-[случайный код]`.
8. Откройте папку результата и импортируйте JSON через расширение **Cookie‑Editor** либо Netscape через любой менеджер кук.

### 📁 Пример выходной структуры

При выборе *Каждая папка = компьютер* и *Разделение по доменам* получится:

```
Result/Result-[ABCDEFGHIJKL]/
├── Outlook-COMP1.json
├── domain_split_COMP1/
│   ├── login.live.com.json
│   ├── account.microsoft.com.json
│   └── ...
├── Outlook-COMP2.json
├── domain_split_COMP2/
│   └── ...
```

Каждый файл можно сразу импортировать в **Cookie‑Editor** (Import → Select file).

### ⚠️ Важно

- **Только Windows** – тестировалось на Win 10/11. На Mac/Linux могут быть проблемы с путями (PR приветствуются).
- Инструмент **не отправляет** никаких данных в сеть. Всё работает строго локально.
- Ошибка `IndexError` при старте означает отсутствие папки `data` – её можно просто создать пустой, это не критично.

---

## 📢 Contacts & Updates

- **GitHub:** [https://github.com/FoeXploit](https://github.com/FoeXploit)
- **Telegram:** [https://t.me/Foe121](https://t.me/Foe121)

*По вопросам, багам или пожеланиям – пишите. / For bugs, questions, or suggestions – feel free to reach out.*
```
