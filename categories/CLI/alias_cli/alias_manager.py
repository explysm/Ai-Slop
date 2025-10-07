#!/usr/bin/env python3

import os
import re
import sys

# Constants
CONFIG_FILES = {
    'bash': '.bashrc',
    'zsh': '.zshrc',
}
ALIAS_SECTION_START = '# START ALIAS MANAGER'
ALIAS_SECTION_END = '# END ALIAS MANAGER'

def get_shell_config_path():
    """Detects the user's shell and returns the path to the config file."""
    shell = os.environ.get('SHELL', '')
    if 'zsh' in shell:
        return os.path.expanduser(f"~/{CONFIG_FILES['zsh']}")
    # Default to bash
    return os.path.expanduser(f"~/{CONFIG_FILES['bash']}")

def read_config_file(config_path):
    """Reads the content of the configuration file."""
    if not os.path.exists(config_path):
        return ""
    with open(config_path, 'r') as f:
        return f.read()

def write_config_file(config_path, content):
    """Writes content to the configuration file."""
    with open(config_path, 'w') as f:
        f.write(content)

def get_managed_aliases(content):
    """Extracts aliases from the managed section of the config file."""
    managed_section = re.search(f'{ALIAS_SECTION_START}(.*?){ALIAS_SECTION_END}', content, re.DOTALL)
    if not managed_section:
        return {}
    
    aliases = {}
    for line in managed_section.group(1).strip().split('\n'):
        if line.startswith('alias '):
            match = re.match(r"alias (.*?)=(.*)", line)
            if match:
                aliases[match.group(1)] = match.group(2)
    return aliases

def get_managed_paths(content):
    """Extracts paths from the managed section of the config file."""
    managed_section = re.search(f'{ALIAS_SECTION_START}(.*?){ALIAS_SECTION_END}', content, re.DOTALL)
    if not managed_section:
        return []

    paths = []
    for line in managed_section.group(1).strip().split('\n'):
        if line.startswith('export PATH='):
            match = re.search(r"export PATH=(?:(?:\$PATH):)?(.*)", line)
            if match:
                paths.extend(filter(None, match.group(1).split(':')))
    return paths


def view_aliases(config_path):
    """Displays the current aliases."""
    content = read_config_file(config_path)
    aliases = get_managed_aliases(content)
    paths = get_managed_paths(content)

    print("\n--- Aliases ---")
    if aliases:
        for name, value in aliases.items():
            print(f"{name}: {value}")
    else:
        print("No aliases found.")
        
    print("\n--- Paths ---")
    if paths:
        for path in paths:
            print(path)
    else:
        print("No paths found.")


def add_alias(config_path):
    """Adds a new alias."""
    name = input("Enter alias name: ")
    command = input("Enter command (in quotes): ")

    content = read_config_file(config_path)
    new_alias = f"alias {name}={command}"

    if ALIAS_SECTION_START in content:
        content = content.replace(ALIAS_SECTION_END, f"{new_alias}\n{ALIAS_SECTION_END}")
    else:
        content += f"\n{ALIAS_SECTION_START}\n{new_alias}\n{ALIAS_SECTION_END}\n"
        
    write_config_file(config_path, content)
    print(f"Alias '{name}' added. Please restart your shell or run 'source {config_path}' to apply changes.")

def remove_alias(config_path):
    """Removes an existing alias."""
    name = input("Enter alias name to remove: ")
    
    content = read_config_file(config_path)
    aliases = get_managed_aliases(content)

    if name not in aliases:
        print(f"Alias '{name}' not found.")
        return

    # This is a simplified removal. A more robust solution would be to
    # parse and rewrite the managed section.
    new_content = []
    in_managed_section = False
    for line in content.splitlines():
        if line.strip() == ALIAS_SECTION_START:
            in_managed_section = True
        elif line.strip() == ALIAS_SECTION_END:
            in_managed_section = False

        if in_managed_section and line.startswith(f"alias {name}="):
            continue
        new_content.append(line)

    write_config_file(config_path, "\n".join(new_content))
    print(f"Alias '{name}' removed. Please restart your shell or run 'source {config_path}' to apply changes.")


def add_path(config_path):
    """Adds a new path to the PATH."""
    path = input("Enter path to add: ")
    
    content = read_config_file(config_path)
    new_path_export = f"export PATH={path}:$PATH"

    if ALIAS_SECTION_START in content:
        content = content.replace(ALIAS_SECTION_END, f"{new_path_export}\n{ALIAS_SECTION_END}")
    else:
        content += f"\n{ALIAS_SECTION_START}\n{new_path_export}\n{ALIAS_SECTION_END}\n"

    write_config_file(config_path, content)
    print(f"Path '{path}' added. Please restart your shell or run 'source {config_path}' to apply changes.")


def import_existing_aliases_and_paths(config_path):
    """Imports existing aliases and paths into the managed section."""
    content = read_config_file(config_path)
    managed_aliases = get_managed_aliases(content)
    managed_paths = get_managed_paths(content)

    new_aliases = []
    new_paths = []

    for line in content.splitlines():
        if line.startswith('alias '):
            match = re.match(r"alias (.*?)=(.*)", line)
            if match:
                name = match.group(1)
                if name not in managed_aliases:
                    new_aliases.append(line)
        elif line.startswith('export PATH='):
            match = re.search(r"export PATH=(?:(?:\$PATH):)?(.*)", line)
            if match:
                paths_in_line = filter(None, match.group(1).split(':'))
                for path in paths_in_line:
                    if path not in managed_paths:
                        new_paths.append(line)
                        break

    if not new_aliases and not new_paths:
        return

    print("Found existing aliases and/or paths. Importing them into the managed section.")

    if ALIAS_SECTION_START in content:
        new_content = ""
        if new_aliases:
            new_content += "\n" + "\n".join(new_aliases)
        if new_paths:
            new_content += "\n" + "\n".join(new_paths)
        content = content.replace(ALIAS_SECTION_END, f"{new_content}\n{ALIAS_SECTION_END}")
    else:
        content += f"\n{ALIAS_SECTION_START}\n"
        if new_aliases:
            content += "\n".join(new_aliases) + "\n"
        if new_paths:
            content += "\n".join(new_paths) + "\n"
        content += f"{ALIAS_SECTION_END}\n"

    write_config_file(config_path, content)
    print("Import complete. Please restart your shell or run 'source {config_path}' to apply changes.")


def main():
    """Main function."""
    config_path = get_shell_config_path()
    print(f"Reading from: {config_path}")
    
    if not os.path.exists(config_path):
        create_file = input(f"Configuration file not found at {config_path}. Create it? (y/n): ")
        if create_file.lower() != 'y':
            sys.exit("Aborting.")
        write_config_file(config_path, "")

    import_existing_aliases_and_paths(config_path)

    while True:
        print("\n--- Alias Manager ---")
        print("1. View aliases and paths")
        print("2. Add alias")
        print("3. Remove alias")
        print("4. Add path")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            view_aliases(config_path)
        elif choice == '2':
            add_alias(config_path)
        elif choice == '3':
            remove_alias(config_path)
        elif choice == '4':
            add_path(config_path)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()