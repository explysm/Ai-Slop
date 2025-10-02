
import os
import argparse

# ANSI escape codes for colors
COLOR_BLUE = '\033[94m'
COLOR_GREEN = '\033[92m'
COLOR_END = '\033[0m'

def tree_cli(startpath, folders_only=False, depth=0, prefix=''):
    if depth == 0:
        print(f"{COLOR_BLUE}{os.path.basename(startpath)}{COLOR_END}")

    contents = sorted(os.listdir(startpath))
    # Separate directories and files for consistent listing
    dirs = [c for c in contents if os.path.isdir(os.path.join(startpath, c))]
    files = [c for c in contents if os.path.isfile(os.path.join(startpath, c))]

    # Combine, prioritizing directories
    sorted_contents = dirs + files

    for i, item in enumerate(sorted_contents):
        path = os.path.join(startpath, item)
        is_last = (i == len(sorted_contents) - 1)
        
        if os.path.isdir(path):
            print(f"{prefix}{"└── " if is_last else "├── "}{COLOR_BLUE}{item}{COLOR_END}")
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_cli(path, folders_only, depth + 1, new_prefix)
        elif not folders_only:
            print(f"{prefix}{"└── " if is_last else "├── "}{COLOR_GREEN}{item}{COLOR_END}")

def main():
    parser = argparse.ArgumentParser(description="Generate a tree-like directory listing.")
    parser.add_argument('path', nargs='?', default='.', help="The starting directory (default: current directory)")
    parser.add_argument('--folders', action='store_true', help="Only show folders")
    
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory '{args.path}' not found.")
        return

    tree_cli(args.path, folders_only=args.folders)

if __name__ == "__main__":
    main()
