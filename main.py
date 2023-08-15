import os
import zipfile
import subprocess
import shutil
import re
from pathlib import Path

CONFIG_FILE = 'config.txt'

def save_directory(directory):
    with open(CONFIG_FILE, 'w') as f:
        f.write(directory)

def load_directory():
    if not Path(CONFIG_FILE).exists():
        return None
    with open(CONFIG_FILE, 'r') as f:
        return f.read().strip()

def list_archives(directory):
    return [f for f in os.listdir(directory) if f.endswith('.zip')]

def enhanced_parse_env(env_path):
    env_vars = {}
    
    with open(env_path, 'r') as file:
        for line in file.readlines():
            # Split only at the first '=' to handle cases where value might be an empty string
            key, value = line.strip().split('=', 1)
            env_vars[key] = value.strip()
    
    # Check for keys with empty values and prompt the user for input
    for key, value in env_vars.items():
        if not value:
            env_vars[key] = input(f"Provide a value for {key}: ")

    return env_vars


def replace_placeholders_in_file(file_path, env_vars):
    with open(file_path, 'r') as file:
        content = file.read()
        for key, value in env_vars.items():
            content = re.sub(r'\{' + re.escape(key) + r'\}', value, content)
    with open(file_path, 'w') as file:
        file.write(content)

def inject_env_values(temp_dir, env_vars):
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file != ".env":
                replace_placeholders_in_file(os.path.join(root, file), env_vars)

def extract_and_run_build_with_temp_archive(zip_file, directory):
    ARCHIVE_DIR = './archive'
    
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        if os.path.exists(ARCHIVE_DIR):
            shutil.rmtree(ARCHIVE_DIR)
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        zip_ref.extractall(ARCHIVE_DIR)
        
        env_vars = enhanced_parse_env(os.path.join(ARCHIVE_DIR, '.env'))
        inject_env_values(ARCHIVE_DIR, env_vars)
        
        exit_code = subprocess.call(['sh', f'{ARCHIVE_DIR}/build.sh'])
        shutil.rmtree(ARCHIVE_DIR)
        
        return exit_code == 0

def select_from_list(items, message):
    print(message)
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(items):
                return items[choice-1]
            else:
                print("\033[91mInvalid choice. Please select a number from the list.\033[0m")
        except ValueError:
            print("\033[91mPlease enter a valid number.\033[0m")

def main():
    try:
        directory = load_directory()
        if not directory:
            directory = input('Specify the directory where .zip archives are saved: ')
            save_directory(directory)
        
        archives = list_archives(directory)
        if not archives:
            print("No .zip archives found in the specified directory.")
            return
        
        selected_archive = select_from_list(archives, "Select a .zip archive:")

        with zipfile.ZipFile(os.path.join(directory, selected_archive), 'r') as zip_ref:
            if 'README' in zip_ref.namelist():
                with zip_ref.open('README') as readme:
                    print("\nDescription:\n", readme.read().decode('utf-8'))
                    print("\n", "-"*50, "\n")
        
        success = extract_and_run_build_with_temp_archive(os.path.join(directory, selected_archive), directory)
        if success:
            print("\033[92mBuild process finished successfully!\033[0m")
        else:
            print("\033[91mBuild process encountered an error!\033[0m")
    
    except KeyboardInterrupt:
        print("\n\033[93mGoodbye!\033[0m")

if __name__ == "__main__":
    main()
