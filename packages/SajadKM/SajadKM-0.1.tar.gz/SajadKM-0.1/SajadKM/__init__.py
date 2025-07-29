import os, sys, shutil
def copy_local_file(filepath, destination_dir):
    filename = os.path.basename(filepath)
    dest_path = os.path.join(destination_dir, filename)
    if not os.path.exists(filepath):
        print(f"[!] {filepath}")
        return
    os.makedirs(destination_dir, exist_ok=True)
    shutil.copy2(filepath, dest_path)
    print(f"[+] {dest_path}")
def main():
    if len(sys.argv) == 1:
        local_file = 'SajadKM.cpython-311.so'
        filename = os.path.basename(local_file)
        dest_folder = 'lib/python3.11/lib-dynload/' if filename.endswith('.so') else 'lib/python3.11/lib-dynload/'
        copy_local_file(local_file, os.path.join(sys.prefix, dest_folder))
if __name__ == "__main__":
    main()