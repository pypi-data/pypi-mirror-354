import os
import platform
import subprocess
import multiprocessing
from tqdm import tqdm
import pikepdf
from pikepdf import PasswordError

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import tkinter as tk
    from tkinter import filedialog

    def win_choose_files():
        tk.Tk().withdraw()
        pdfs = filedialog.askopenfilenames(
            title="Select PDFs", filetypes=[("PDF files", "*.pdf")]
        )
        wordlist = filedialog.askopenfilename(
            title="Select Password List", filetypes=[("Text files", "*.txt")]
        )
        out_dir = filedialog.askdirectory(title="Select Output Folder")
        return list(pdfs), wordlist, out_dir


def zenity_file_selection(title, multiple=False):
    try:
        cmd = ["zenity", "--file-selection", f"--title={title}"]
        if multiple:
            cmd += ["--multiple", "--separator=|"]
        result = subprocess.check_output(cmd, text=True).strip()
        return result.split("|") if multiple else result
    except subprocess.CalledProcessError:
        return None


def zenity_folder_selection(title):
    try:
        result = subprocess.check_output(
            ["zenity", "--file-selection", "--directory", f"--title={title}"],
            text=True
        ).strip()
        return result
    except subprocess.CalledProcessError:
        return None


def linux_choose_files():
    pdfs = zenity_file_selection("Select PDFs", multiple=True)
    if not pdfs:
        return [], None, None
    wordlist = zenity_file_selection("Select Password List")
    if not wordlist:
        return [], None, None
    out_dir = zenity_folder_selection("Select Output Folder")
    return pdfs, wordlist, out_dir


def choose_files():
    return win_choose_files() if IS_WINDOWS else linux_choose_files()


def load_passwords(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []


def unlock_pdf(path, passwords, queue, out_dir):
    try:
        with pikepdf.open(path) as pdf:
            queue.put((path, "Unprotected"))
            return
    except PasswordError:
        pass
    except Exception as e:
        queue.put((path, f"Error: {e}"))
        return

    for pw in tqdm(passwords, desc=os.path.basename(path), leave=False):
        try:
            with pikepdf.open(path, password=pw) as pdf:
                name = os.path.splitext(os.path.basename(path))[0] + "_unlocked.pdf"
                pdf.save(os.path.join(out_dir, name))
                queue.put((path, pw))
                return
        except PasswordError:
            continue
        except Exception as e:
            queue.put((path, f"Error: {e}"))
            return

    queue.put((path, None))

