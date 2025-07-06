import os
import glob
import getpass
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

NOTES_DIR = "Encrypted Notes"

# Ensure the notes directory exists
os.makedirs(NOTES_DIR, exist_ok=True)

def cprint(text, color=None):
    if COLOR_ENABLED and color:
        print(getattr(Fore, color.upper(), "") + text + Style.RESET_ALL)
    else:
        print(text)

def generate_key(password):
    # Derive a Fernet key from the password (simple, not for production)
    import base64, hashlib
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_note(note, password):
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(note.encode())

def decrypt_note(token, password):
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(token).decode()

def save_note(note, password):
    encrypted = encrypt_note(note, password)
    filename = f"note_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(NOTES_DIR, filename)
    with open(filepath, 'wb') as f:
        f.write(encrypted)
    cprint(f"Note saved as {filename}!", 'green')

def list_notes():
    pattern = os.path.join(NOTES_DIR, "note_*.txt")
    files = sorted(glob.glob(pattern))
    if not files:
        cprint("No notes found.", 'yellow')
        return []
    cprint("\nNo.  Filename", 'cyan')
    for i, file in enumerate(files, 1):
        print(f"{i:<4} {os.path.basename(file)}")
    return files

def write_note():
    note = input("Note: ")
    password = getpass.getpass("Enter a password to encrypt this note: ")
    save_note(note, password)

def view_note():
    files = list_notes()
    if not files:
        return
    try:
        idx = int(input("\nEnter note number [1]: ") or "1") - 1
        if idx < 0 or idx >= len(files):
            cprint("Invalid selection.", 'red')
            return
    except ValueError:
        cprint("Invalid input.", 'red')
        return
    filename = files[idx]
    password = getpass.getpass("Enter the password to decrypt this note: ")
    with open(filename, 'rb') as f:
        encrypted = f.read()
    try:
        note = decrypt_note(encrypted, password)
        cprint(f"\n{os.path.basename(filename)}", 'yellow')
        cprint(note, 'green')
    except InvalidToken:
        cprint("Incorrect password or corrupted note.", 'red')

def main():
    while True:
        cprint("\n================= \U0001F512 Welcome to SecurePad =================", 'magenta')
        cprint("[1] Write a New Encrypted Note\n[2] View a Encrypted Note\n[3] Exit", 'magenta')
        choice = input("\nSelect an option [1/2/3]: ").strip()
        if choice == '1':
            write_note()
        elif choice == '2':
            view_note()
        elif choice == '3':
            cprint("Goodbye!", 'cyan')
            break
        else:
            cprint("Invalid option. Try again.", 'red')

if __name__ == "__main__":
    main() 