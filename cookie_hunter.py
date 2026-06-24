#!/usr/bin/env python3
"""
Cookie Hunter Advanced v2.4 – Foe
GUI for converting Netscape cookie .txt → custom formatted output:
- JSON (Cookie‑Editor) or Netscape (.txt)
- Filter by service (e.g., Outlook/Hotmail)
- Split by domain
- Split by computer: either by # Netscape headers or by folder
  (each folder = one computer)

Author: Foe
GitHub: https://github.com/FoeXploit
Telegram: https://t.me/Foe121
"""

import json, os, sys, random, string, threading, platform
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog,
    QTextEdit, QProgressBar, QVBoxLayout, QWidget, QCheckBox,
    QComboBox, QLineEdit, QButtonGroup, QRadioButton
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QFontDatabase


# ----------------------------------------------------------------------
# Internal RandString
# ----------------------------------------------------------------------
class RandString:
    def __init__(self, mode="uppercase", length=12):
        if mode == "uppercase":
            self.chars = string.ascii_uppercase
        elif mode == "lowercase":
            self.chars = string.ascii_lowercase
        elif mode == "digits":
            self.chars = string.digits
        else:
            self.chars = string.ascii_letters + string.digits
        self.length = length
    def __str__(self):
        return ''.join(random.choice(self.chars) for _ in range(self.length))
    def __repr__(self):
        return self.__str__()


# ----------------------------------------------------------------------
# Services and domain patterns
# ----------------------------------------------------------------------
SERVICE_DOMAINS = {
    "Outlook / Live / Hotmail": [
        "outlook.live.com", ".live.com", ".microsoft.com",
        "account.microsoft.com", "login.live.com", "login.microsoftonline.com",
        "outlook.office.com", ".hotmail.com", ".outlook.com",
        "www.microsoft.com",
    ],
    "Google": [
        ".google.com", ".google.se", "accounts.google.com", "mail.google.com",
    ],
    "Facebook": [
        ".facebook.com", ".fb.com", ".messenger.com",
    ],
}


def cookie_matches_domain(cookie_domain: str, patterns: list[str]) -> bool:
    domain = cookie_domain.lstrip(".")
    for pat in patterns:
        pat = pat.strip()
        if not pat:
            continue
        if pat.startswith("."):
            if domain == pat[1:] or domain.endswith(pat):
                return True
        else:
            if domain == pat:
                return True
    return False


# ----------------------------------------------------------------------
# Cookie parsing and serialization
# ----------------------------------------------------------------------
def parse_cookie_line(line: str) -> dict | None:
    parts = line.strip().split("\t")
    if len(parts) < 7:
        return None
    return {
        "domain": parts[0],
        "flag": parts[1],
        "path": parts[2],
        "secure": parts[3],
        "expiration": parts[4],
        "name": parts[5],
        "value": parts[6],
    }


def cookie_to_netscape(cookie: dict) -> str:
    return "\t".join([
        cookie["domain"], cookie["flag"], cookie["path"],
        cookie["secure"], cookie["expiration"], cookie["name"], cookie["value"],
    ])


def to_cookie_editor(cookie: dict) -> dict:
    ce = {
        "domain": cookie.get("domain", ""),
        "name": cookie.get("name", ""),
        "value": cookie.get("value", ""),
        "path": cookie.get("path", "/"),
        "secure": cookie.get("secure", "FALSE").upper() == "TRUE",
        "httpOnly": False,
        "sameSite": "unspecified",
        "storeId": "0",
        "hostOnly": False,
    }
    flag = cookie.get("flag", "TRUE").upper()
    ce["hostOnly"] = (flag != "TRUE")
    if cookie.get("domain", "").startswith("."):
        ce["hostOnly"] = False
    exp_raw = cookie.get("expiration", "0")
    try:
        exp_val = int(exp_raw) if exp_raw != "0" else 0
    except ValueError:
        exp_val = 0
    if exp_val > 0:
        ce["expirationDate"] = exp_val
        ce["session"] = False
    else:
        ce["session"] = True
        ce.pop("expirationDate", None)
    return ce


# ----------------------------------------------------------------------
# Collect cookies from a directory (all .txt files recursively)
# ----------------------------------------------------------------------
def gather_cookies_from_directory(dir_path: str) -> list[dict]:
    """Find all .txt files recursively in dir_path and return a list of cookies."""
    all_cookies = []
    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.lower().endswith(".txt"):
                full_path = os.path.join(root, f)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="replace") as fh:
                        for line in fh:
                            line = line.strip()
                            if not line or line.startswith("#"):
                                continue
                            c = parse_cookie_line(line)
                            if c:
                                all_cookies.append(c)
                except Exception:
                    continue
    return all_cookies


# ----------------------------------------------------------------------
# Worker logic (threaded)
# ----------------------------------------------------------------------
class ConverterWorker(QThread):
    progress_updated = pyqtSignal(int)
    log_message = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, input_folder, output_folder, recursive=True,
                 split_by_domain=True, filter_patterns=None, split_computers="headers",
                 output_format="json"):
        """
        split_computers: "headers" -> split by # Netscape headers in the same file
                         "folders" -> each subfolder inside input_folder is a computer
                         "none"    -> all cookies combined into one output file
        """
        super().__init__()
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.recursive = recursive
        self.split_by_domain = split_by_domain
        self.filter_patterns = filter_patterns
        self.split_computers = split_computers
        self.output_format = output_format

    def run(self):
        try:
            os.makedirs(self.output_folder, exist_ok=True)
            self.log_message.emit(f"[+] Output format: {'Netscape (.txt)' if self.output_format == 'netscape' else 'JSON (Cookie‑Editor)'}")
            if self.filter_patterns:
                self.log_message.emit(f"[+] Filtering for domains: {', '.join(self.filter_patterns)}")
            if self.split_by_domain:
                self.log_message.emit("[+] Splitting by domain")

            # ------------------------------------------------------------------
            # 1) Fetch data based on split_computers
            # ------------------------------------------------------------------
            if self.split_computers == "folders":
                # Each subfolder is a computer
                items = os.listdir(self.input_folder)
                subdirs = [os.path.join(self.input_folder, d) for d in items
                           if os.path.isdir(os.path.join(self.input_folder, d))]
                subdirs.sort()
                computers = []
                for sub in subdirs:
                    cookies = gather_cookies_from_directory(sub)
                    if cookies:
                        comp_name = os.path.basename(sub)
                        short_name = comp_name[:40].strip()
                        computers.append((short_name, cookies))
                self.log_message.emit(f"[+] Found {len(computers)} folder computers.")
                total_items = len(computers)
                process_func = self._process_computer_list

            elif self.split_computers == "headers":
                # Collect .txt files and split by Netscape headers
                txt_files = self._collect_txt_files()
                if not txt_files:
                    self.log_message.emit("[!] No .txt files found.")
                    self.finished.emit("")
                    return
                computers = []
                for tf in txt_files:
                    try:
                        with open(tf, "r", encoding="utf-8", errors="replace") as f:
                            raw = f.read()
                        sections = self._split_by_headers(raw)
                        for idx, (_, lines) in enumerate(sections):
                            cookies = [parse_cookie_line(l) for l in lines if parse_cookie_line(l)]
                            if cookies:
                                computers.append((f"{os.path.basename(tf)}-s{idx+1}", cookies))
                    except Exception as e:
                        self.log_message.emit(f"[-] Error in {os.path.basename(tf)}: {e}")
                self.log_message.emit(f"[+] Found {len(computers)} header computers.")
                total_items = len(computers)
                process_func = self._process_computer_list

            else:  # "none" – all cookies in a single output
                cookies = gather_cookies_from_directory(self.input_folder)
                if not cookies:
                    self.log_message.emit("[!] No cookies found.")
                    self.finished.emit("")
                    return
                computers = [("All-Cookies", cookies)]
                total_items = 1
                process_func = self._process_computer_list

            # ------------------------------------------------------------------
            # 2) Process each computer
            # ------------------------------------------------------------------
            for idx, (comp_name, comp_cookies) in enumerate(computers, start=1):
                # Filter
                if self.filter_patterns:
                    filtered = [c for c in comp_cookies if cookie_matches_domain(c["domain"], self.filter_patterns)]
                else:
                    filtered = comp_cookies
                if not filtered:
                    self.log_message.emit(f"[-] {comp_name}: no matching cookies.")
                    continue

                # Prefix
                if self.filter_patterns:
                    prefix = self.filter_patterns[0].replace(".", "").replace("/", "_")[:30]
                else:
                    prefix = "All"

                # Sanitize computer name for filename
                safe_comp = "".join(c if c.isalnum() or c in "._-" else "_" for c in comp_name)
                if len(safe_comp) > 50:
                    safe_comp = safe_comp[:50]

                # JSON export
                if self.output_format == "json":
                    json_path = os.path.join(self.output_folder, f"{prefix}-{safe_comp}.json")
                    with open(json_path, "w", encoding="utf-8") as jf:
                        json.dump(filtered, jf, indent=4, ensure_ascii=False)

                    if self.split_by_domain:
                        domain_dir = os.path.join(self.output_folder, f"domain_split_{safe_comp}")
                        os.makedirs(domain_dir, exist_ok=True)
                        domain_map = defaultdict(list)
                        for c in filtered:
                            dom = c.get("domain", "unknown").lstrip(".")
                            domain_map[dom].append(to_cookie_editor(c))
                        for domain, c_list in domain_map.items():
                            safe_dom = "".join(c if c.isalnum() or c in "._-" else "_" for c in domain)
                            with open(os.path.join(domain_dir, f"{safe_dom}.json"), "w", encoding="utf-8") as df:
                                json.dump(c_list, df, indent=2, ensure_ascii=False)

                # Netscape export
                else:
                    txt_path = os.path.join(self.output_folder, f"{prefix}-{safe_comp}.txt")
                    with open(txt_path, "w", encoding="utf-8") as tf:
                        tf.write("# Netscape HTTP Cookie File\n")
                        tf.write(f"# Computer: {comp_name}\n\n")
                        for c in filtered:
                            tf.write(cookie_to_netscape(c) + "\n")

                    if self.split_by_domain:
                        domain_dir = os.path.join(self.output_folder, f"domain_split_{safe_comp}")
                        os.makedirs(domain_dir, exist_ok=True)
                        domain_map = defaultdict(list)
                        for c in filtered:
                            dom = c.get("domain", "unknown").lstrip(".")
                            domain_map[dom].append(cookie_to_netscape(c))
                        for domain, lines_list in domain_map.items():
                            safe_dom = "".join(c if c.isalnum() or c in "._-" else "_" for c in domain)
                            with open(os.path.join(domain_dir, f"{safe_dom}.txt"), "w", encoding="utf-8") as df:
                                df.write("# Netscape HTTP Cookie File\n\n")
                                df.write("\n".join(lines_list) + "\n")

                # Progress
                progress = int((idx / total_items) * 100)
                self.progress_updated.emit(progress)

            self.log_message.emit(f"[+] Done! Exported {len(computers)} computer(s).")
            self.finished.emit(self.output_folder)

        except Exception as e:
            self.log_message.emit(f"[!] Critical error: {e}")
            self.finished.emit("")

    def _collect_txt_files(self):
        txt_files = []
        if self.recursive:
            for root, _, files in os.walk(self.input_folder):
                for f in files:
                    if f.lower().endswith(".txt"):
                        txt_files.append(os.path.join(root, f))
        else:
            for f in os.listdir(self.input_folder):
                full = os.path.join(self.input_folder, f)
                if os.path.isfile(full) and f.lower().endswith(".txt"):
                    txt_files.append(full)
        return txt_files

    def _split_by_headers(self, text: str):
        """Return list of (header, [cookie_lines]) for each Netscape section."""
        sections = []
        current_lines = []
        for line in text.splitlines():
            if line.startswith("# Netscape HTTP Cookie File"):
                if current_lines:
                    sections.append(("", current_lines))
                    current_lines = []
            elif line.startswith("#") or not line.strip():
                continue
            else:
                current_lines.append(line)
        if current_lines:
            sections.append(("", current_lines))
        return sections

    def _process_computer_list(self, computers):
        # This method is not directly used; logic is inline in run()
        pass


# ----------------------------------------------------------------------
# Graphical interface
# ----------------------------------------------------------------------
class CookieConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cookie Hunter Advanced v2.4 | Foe")
        self.setFixedSize(900, 780)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self._load_resources()
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(8)

        # Title
        self.title_lbl = QLabel("Cookie Hunter – Per‑Folder Computer Detection")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if hasattr(self, 'custom_font'):
            self.title_lbl.setFont(QFont(self.custom_font, 20))
        else:
            self.title_lbl.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.title_lbl)

        # Subtitle with Foe's contact info
        self.sub_lbl = QLabel("GitHub: https://github.com/FoeXploit | Telegram: https://t.me/Foe121")
        self.sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_lbl.setStyleSheet("color: #2973B2; font-size: 14px;")
        layout.addWidget(self.sub_lbl)

        # --- Output format ---
        self.format_label = QLabel("Output format:")
        self.format_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
        layout.addWidget(self.format_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["JSON (Cookie‑Editor)", "Netscape (.txt)"])
        self.format_combo.setStyleSheet("font-size: 14px; padding: 4px;")
        layout.addWidget(self.format_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Service selection ---
        self.service_label = QLabel("Filter by service:")
        self.service_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.service_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.service_combo = QComboBox()
        self.service_combo.addItems(list(SERVICE_DOMAINS.keys()) + ["All cookies (no filter)", "Custom"])
        self.service_combo.setStyleSheet("font-size: 14px; padding: 4px;")
        self.service_combo.currentTextChanged.connect(self._on_service_changed)
        layout.addWidget(self.service_combo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.custom_domains_edit = QLineEdit()
        self.custom_domains_edit.setPlaceholderText("Custom domains, comma-separated")
        self.custom_domains_edit.setStyleSheet("font-size: 14px; padding: 4px;")
        self.custom_domains_edit.setVisible(False)
        layout.addWidget(self.custom_domains_edit, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Computer splitting ---
        self.comp_group_label = QLabel("Computer splitting:")
        self.comp_group_label.setStyleSheet("font-size: 16px; margin-top: 10px;")
        layout.addWidget(self.comp_group_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.comp_group = QButtonGroup(self)

        self.radio_none = QRadioButton("No split (all in one file)")
        self.radio_none.setStyleSheet("font-size: 15px;")
        self.comp_group.addButton(self.radio_none)

        self.radio_headers = QRadioButton("Split by # Netscape headers")
        self.radio_headers.setStyleSheet("font-size: 15px; color: #ffab40;")
        self.comp_group.addButton(self.radio_headers)

        self.radio_folders = QRadioButton("Each folder = one computer")
        self.radio_folders.setStyleSheet("font-size: 15px; color: #4fc3f7;")
        self.comp_group.addButton(self.radio_folders)

        # Default selection
        self.radio_folders.setChecked(True)

        for radio in [self.radio_none, self.radio_headers, self.radio_folders]:
            layout.addWidget(radio, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Other checkboxes ---
        self.recursive_cb = QCheckBox("Recursive search (header mode)")
        self.recursive_cb.setChecked(True)
        self.recursive_cb.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.recursive_cb, alignment=Qt.AlignmentFlag.AlignCenter)

        self.split_cb = QCheckBox("Split by domain")
        self.split_cb.setChecked(True)
        self.split_cb.setStyleSheet("font-size: 16px; color: #81c784;")
        layout.addWidget(self.split_cb, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Button ---
        self.select_btn = QPushButton("SELECT FOLDER WITH LOG FILES")
        self.select_btn.setStyleSheet(
            "background-color: #2e7d32; color: white; font-size: 18px; padding: 8px; border-radius: 5px;"
        )
        self.select_btn.clicked.connect(self._select_folder)
        layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Log and progress
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setStyleSheet("background-color: #333; font-size: 14px;")
        layout.addWidget(self.log_area)

        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setStyleSheet(
            "QProgressBar { border: 1px solid #555; background: #333; }"
            "QProgressBar::chunk { background-color: #4caf50; }"
        )
        layout.addWidget(self.progress)

        self.worker = None

    def _load_resources(self):
        try:
            font_path = os.path.join("data", "fonts", "UbuntuMono-Regular.ttf")
            if os.path.exists(font_path):
                font_id = QFontDatabase.addApplicationFont(font_path)
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                    self.custom_font = families[0]
        except Exception:
            pass
        try:
            icon_path = os.path.join("data", "icons", "app.ico")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass

    def _on_service_changed(self, text):
        self.custom_domains_edit.setVisible(text == "Custom")

    def _get_filter_patterns(self):
        service = self.service_combo.currentText()
        if service == "All cookies (no filter)":
            return None
        elif service == "Custom":
            raw = self.custom_domains_edit.text().strip()
            if not raw:
                return None
            return [d.strip() for d in raw.split(",") if d.strip()]
        else:
            return SERVICE_DOMAINS.get(service, None)

    def _select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select folder with log files")
        if not folder:
            self.log_area.append("[!] No folder selected.")
            return

        rand_str = str(RandString("uppercase", 12))
        output = os.path.join("Result", f"Result - [{rand_str}]")

        self.progress.setValue(0)
        self.select_btn.setEnabled(False)
        self.log_area.clear()
        self.log_area.append(f"[+] Selected folder: {folder}")
        self.log_area.append(f"[+] Output: {output}")

        # Determine split mode
        if self.radio_none.isChecked():
            split_mode = "none"
        elif self.radio_headers.isChecked():
            split_mode = "headers"
        else:
            split_mode = "folders"

        recursive = self.recursive_cb.isChecked()
        split_domain = self.split_cb.isChecked()
        filter_patterns = self._get_filter_patterns()
        out_fmt = "json" if self.format_combo.currentText().startswith("JSON") else "netscape"

        self.worker = ConverterWorker(folder, output, recursive, split_domain,
                                       filter_patterns, split_mode, out_fmt)
        self.worker.log_message.connect(self._on_log)
        self.worker.progress_updated.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.start()

    def _on_log(self, message):
        self.log_area.append(message)

    def _on_progress(self, value):
        self.progress.setValue(value)

    def _on_finished(self, output_folder):
        self.select_btn.setEnabled(True)
        if output_folder:
            self.log_area.append(f"[+] Finished! Open the result folder: {output_folder}")
        else:
            self.log_area.append("[!] Conversion failed or no files found.")


# ----------------------------------------------------------------------
# Start
# ----------------------------------------------------------------------
def main():
    if platform.system() != "Windows":
        print("This tool is only tested on Windows. Exiting.")
        sys.exit(0)

    app = QApplication(sys.argv)
    window = CookieConverterGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except IndexError:
        with open("error.log", "w", encoding="utf-8") as err:
            err.write(
                "Missing 'data' folder. Place it next to the script.\n"
                "data/\n  fonts/\n  icons/\n"
            )
        print("Error: 'data' folder missing. See error.log")
    except Exception as e:
        print(f"Unhandled error: {e}")
