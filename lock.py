import os
import getpass
import hashlib

# =========================
# HASH PASSWORD
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# CREATE FOLDER
# =========================
def create_folder():
    folder = input("Enter folder name: ")

    if not os.path.exists(folder):
        os.mkdir(folder)
        print(f"📁 Folder '{folder}' created successfully!")
    else:
        print("⚠️ Folder already exists!")

# =========================
# SAVE PASSWORD
# =========================
def save_password(folder, password):
    with open(f"{folder}_pass.txt", "w") as f:
        f.write(hash_password(password))

def verify_password(folder, password):
    try:
        with open(f"{folder}_pass.txt", "r") as f:
            stored = f.read()
        return stored == hash_password(password)
    except:
        return False

# =========================
# LOCK FOLDER
# =========================
def lock_folder():
    folder = input("Enter folder name to lock: ")

    if not os.path.exists(folder):
        print("❌ Folder does not exist!")
        return

    password = getpass.getpass("Set password: ")
    save_password(folder, password)

    locked_name = folder + "_LOCKED"
    os.rename(folder, locked_name)

    # Hide folder (Windows only)
    os.system(f'attrib +h "{locked_name}"')

    print(f"\n🔒 Folder '{locked_name}' is LOCKED")

# =========================
# UNLOCK FOLDER
# =========================
def unlock_folder():
    folder = input("Enter locked folder name: ")

    if not os.path.exists(folder):
        print("❌ Locked folder not found!")
        return

    original_name = folder.replace("_LOCKED", "")
    password = getpass.getpass("Enter password: ")

    if verify_password(original_name, password):
        # Unhide folder
        os.system(f'attrib -h "{folder}"')

        os.rename(folder, original_name)

        print(f"\n🔓 Folder '{original_name}' is UNLOCKED\n")

        # Show files
        files = os.listdir(original_name)
        if files:
            print("📂 Files inside folder:")
            for f in files:
                print(f" - {f}")
        else:
            print("📂 Folder is empty")

    else:
        print("❌ Wrong password!")

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
            print("Invalid choice!")

if __name__ == "__main__":
    main()
