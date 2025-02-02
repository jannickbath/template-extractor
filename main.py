import os
import zipfile
import subprocess
import shutil
import re
import sys
from pathlib import Path
from PyInquirer import prompt
from rich import print as rprint
from rich.markdown import Markdown

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

def enhanced_parse_env(env_path, archive_dir):
    env_vars = {}

    # Determine the type of resolver
    if os.path.exists(os.path.join(archive_dir, 'env_resolver.js')):
        resolver_type = 'js'
        resolver_path = os.path.join(archive_dir, 'env_resolver.js')
    else:
        resolver_type = 'sh'
        resolver_path = os.path.join(archive_dir, 'env_resolver.sh')

    resolver_exists = os.path.exists(resolver_path)

    with open(env_path, 'r') as file:
        for line in file.readlines():
            key, value = line.strip().split('=', 1)
            
            # Check if value appears to be a function call
            if re.match(r"\w+\(\)", value) and resolver_exists:
                function_name = value[:-2]
                
                try:
                    if resolver_type == 'js':
                        result = subprocess.check_output(
                            ['node', '-e', f'const {{ {function_name} }} = require("{resolver_path}"); console.log({function_name}())'],
                            text=True, stderr=subprocess.PIPE
                        ).strip()
                    else:
                        result = subprocess.check_output(
                            ['bash', '-c', f'source {resolver_path}; {function_name}'],
                            text=True, stderr=subprocess.PIPE
                        ).strip()
                    
                    options = []
                    if result and result not in ["0", "null", "None", ""]:
                        options.extend(result.split('\n'))
                    options.append("Create new")
                    
                    questions = [{
                        'type': 'list',
                        'name': 'selection',
                        'message': f'Select a value for {key}',
                        'choices': options
                    }]
                    
                    answer = prompt(questions)
                    if answer['selection'] == "Create new":
                        env_vars[key] = input(f"Provide a value for {key}: ")
                    else:
                        env_vars[key] = answer['selection']
                except subprocess.CalledProcessError:
                    env_vars[key] = input(f"Function {function_name} not found or error occurred. Provide a value for {key}: ")
            else:
                env_vars[key] = value.strip()

            # Existing logic for empty values
            if not env_vars[key]:
                env_vars[key] = input(f"Provide a value for {key}: ")

    return env_vars

def replace_placeholders_in_file(file_path, env_vars):
    with open(file_path, 'r') as file:
        content = file.read()
        for key, value in env_vars.items():
            content = re.sub(r'\{' + re.escape(key) + r'\}', value, content)
    with open(file_path, 'w') as file:
        file.write(content)

def get_helper_path():
    if getattr(sys, 'frozen', False):
        # The application is bundled with PyInstaller
        base_path = sys._MEIPASS
    else:
        # The application is run from a script
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, 'helper.js')

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

        # Copy the helper.js file into the archive directory
        shutil.copy(get_helper_path(), ARCHIVE_DIR)
        
        env_vars = enhanced_parse_env(os.path.join(ARCHIVE_DIR, '.env'), ARCHIVE_DIR)
        inject_env_values(ARCHIVE_DIR, env_vars)
        
        # Check which build file exists and execute accordingly
        if os.path.exists(f'{ARCHIVE_DIR}/build.js'):
            exit_code = subprocess.call(['node', f'{ARCHIVE_DIR}/build.js'])
        elif os.path.exists(f'{ARCHIVE_DIR}/build.sh'):
            exit_code = subprocess.call(['sh', f'{ARCHIVE_DIR}/build.sh'])
        else:
            rprint("[red]Error:[/red] No valid build script (build.js or build.sh) found in the archive.")
            return False
        
        shutil.rmtree(ARCHIVE_DIR)
        
        return exit_code == 0

def modern_select_from_list(items, message):
    questions = [
        {
            'type': 'list',
            'name': 'selected_item',
            'message': message,
            'choices': items
        }
    ]

    answers = prompt(questions)
    return answers['selected_item']

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

        while True:
            selected_archive = modern_select_from_list(archives, "Select a .zip archive:")

            with zipfile.ZipFile(os.path.join(directory, selected_archive), 'r') as zip_ref:
                if 'README.md' in zip_ref.namelist():
                    with zip_ref.open('README.md') as readme:
                        markdown_content = readme.read().decode('utf-8')
                        rprint(Markdown(markdown_content))
                        print("\n", "-"*50, "\n")

            confirm_question = [{
                'type': 'confirm',
                'name': 'proceed',
                'message': 'Do you want to proceed with this archive?',
                'default': True
            }]
            confirmation = prompt(confirm_question)
            if confirmation['proceed']:
                break
        
        success = extract_and_run_build_with_temp_archive(os.path.join(directory, selected_archive), directory)
        if success:
            print("\033[92mBuild process finished successfully!\033[0m")
        else:
            print("\033[91mBuild process encountered an error!\033[0m")
    
    except KeyboardInterrupt:
        print("\n\033[93mGoodbye!\033[0m")

if __name__ == "__main__":
    main()