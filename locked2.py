import os
import getpass
import hashlib
import re
import time

BASE_PATH = os.path.join(os.path.expanduser("~"), "Desktop")
AUTO_LOCK_TIME = 30

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# PASSWORD RULES
# =========================
def is_strong_password(password):
    if len(password) < 8:
        return False, "Min 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Need uppercase"
    if not re.search(r"[a-z]", password):
        return False, "Need lowercase"
    if not re.search(r"[0-9]", password):
        return False, "Need number"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Need special char"
    return True, "Strong"

# =========================
# CREATE FOLDER
# =========================
def create_folder():
    folder = input("Enter folder name: ")
    path = os.path.join(BASE_PATH, folder)

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"📁 Created at {path}")
    else:
        print("⚠️ Exists")

# =========================
# PASSWORD STORAGE
# =========================
def save_password(folder, pwd):
    with open(os.path.join(BASE_PATH, f"{folder}_pass.txt"), "w") as f:
        f.write(hash_password(pwd))

def verify_password(folder, pwd):
    try:
        with open(os.path.join(BASE_PATH, f"{folder}_pass.txt"), "r") as f:
            return f.read() == hash_password(pwd)
    except:
        return False

# =========================
# LOCK
# =========================
def perform_lock(folder):
    path = os.path.join(BASE_PATH, folder)
    locked = folder + "_LOCKED"
    locked_path = os.path.join(BASE_PATH, locked)

    if os.path.exists(path):
        os.rename(path, locked_path)
        os.system(f'attrib +h "{locked_path}"')
        print(f"\n🔒 '{locked}' LOCKED")

# =========================
# LOCK FOLDER
# =========================
def lock_folder():
    folder = input("Enter folder name: ")
    path = os.path.join(BASE_PATH, folder)

    if not os.path.exists(path):
        print("❌ Not found")
        return

    while True:
        pwd = getpass.getpass("Set password: ")
        valid, msg = is_strong_password(pwd)
        if valid:
            print("✅ Strong password")
            break
        else:
            print("❌", msg)

    save_password(folder, pwd)
    perform_lock(folder)

# =========================
# FILE MANAGER (AUTO LOAD)
# =========================
def manage_files(folder):
    path = os.path.join(BASE_PATH, folder)

    while True:
        print("\n--- File Manager ---")
        print("1. Create File")
        print("2. Edit File")
        print("3. View Files")
        print("4. Exit & Lock")

        ch = input("Choice: ")

        if ch == '1':
            name = input("File name: ")
            file_path = os.path.join(path, name)

            with open(file_path, "w") as f:
                f.write(input("Enter content: "))

            print("✅ Created")

        elif ch == '2':
            name = input("File name: ")
            file_path = os.path.join(path, name)

            if os.path.exists(file_path):
                with open(file_path, "a") as f:
                    f.write("\n" + input("Add content: "))
                print("✅ Updated")
            else:
                print("❌ Not found")

        elif ch == '3':
            files = os.listdir(path)
            print("\n📂 Files:")
            for f in files:
                print(" -", f)

        elif ch == '4':
            print("🔐 Exiting and locking...")
            perform_lock(folder)
            break

        else:
            print("Invalid")

# =========================
# UNLOCK (UPDATED 🔥)
# =========================
def unlock_folder():
    folder = input("Enter locked folder name: ")
    locked_path = os.path.join(BASE_PATH, folder)

    if not os.path.exists(locked_path):
        print("❌ Locked folder not found")
        return

    original = folder.replace("_LOCKED", "")
    original_path = os.path.join(BASE_PATH, original)

    pwd = getpass.getpass("Enter password: ")

    if verify_password(original, pwd):
        os.system(f'attrib -h "{locked_path}"')
        os.rename(locked_path, original_path)

        print(f"\n🔓 '{original}' UNLOCKED")

        # Open folder
        os.startfile(original_path)

        # 🔥 AUTO LOAD FILE MANAGER
        manage_files(original)

    else:
        print("❌ Wrong password")

# =========================
# MENU
# =========================
def main():
    while True:
        print("\n===== Secure Folder System =====")
        print("1. Create Folder")
        print("2. Lock Folder")
        print("3. Unlock Folder")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            create_folder()
        elif choice == '2':
            lock_folder()
        elif choice == '3':
            unlock_folder()
        elif choice == '4':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
