import multiprocessing
import os
from .core import choose_files, load_passwords, unlock_pdf

def main():
    print("Decryptify - PDF Access Recovery\nVersion: v3.0\nRepo: https://github.com/d4niis44hir/Decryptify")
    input("Press ENTER to begin...")

    pdfs, wordlist_path, out_dir = choose_files()
    if not pdfs or not wordlist_path or not out_dir:
        print("Missing input. Exiting.")
        return

    passwords = load_passwords(wordlist_path)
    if not passwords:
        print("Empty or invalid password list.")
        return

    manager = multiprocessing.Manager()
    queue = manager.Queue()
    jobs = []

    for pdf in pdfs:
        p = multiprocessing.Process(
            target=unlock_pdf, args=(pdf, passwords, queue, out_dir)
        )
        p.start()
        jobs.append(p)

    for p in jobs:
        p.join()

    print("\nResults:")
    while not queue.empty():
        path, result = queue.get()
        name = os.path.basename(path)
        if result == "Unprotected":
            print(f"{name}: Not password protected.")
        elif result:
            print(f"{name}: Password -> {result}")
        else:
            print(f"{name}: No match found.")

    input("Done. Press ENTER to exit.")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

