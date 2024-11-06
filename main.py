import os
import re
from pathlib import Path
import argparse

# Default exclusion patterns
DEFAULT_EXCLUDES = {
    ".git",
    ".gitignore",
    "__pycache__",
    "node_modules",
    ".env",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".DS_Store",
    "Thumbs.db",
}


def should_exclude(path, exclude_patterns):
    """Check if path should be excluded based on patterns."""
    path_str = str(path)
    name = path.name

    for pattern in exclude_patterns:
        # Handle glob patterns (*.ext)
        if pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        # Handle direct matches
        elif pattern in path_str or name == pattern:
            return True
    return False


def get_directory_tree(root_path, exclude_patterns, indent=""):
    """Generate a tree-like directory structure, excluding specified patterns."""
    tree = []
    root = Path(root_path)

    def add_to_tree(path, prefix=""):
        if should_exclude(path, exclude_patterns):
            return

        if path.is_file():
            tree.append(prefix + "├── " + path.name)
        elif path.is_dir():
            tree.append(prefix + "├── " + path.name + "/")
            # Sort directories first, then files
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            for item in items:
                add_to_tree(item, prefix + "│   ")

    add_to_tree(root)
    return "\n".join(tree)


def clean_content(content):
    """Clean file content to minimize tokens while preserving meaning."""
    # Remove empty lines
    content = re.sub(r"\n\s*\n", "\n", content)
    # Remove trailing whitespace
    content = re.sub(r"[ \t]+$", "", content, flags=re.MULTILINE)
    # Collapse multiple spaces
    content = re.sub(r" +", " ", content)
    return content.strip()


def process_directory(
    directory, extensions, exclude_patterns, output_file="prompts.txt"
):
    """Process directory and create formatted output file."""
    directory = Path(directory)

    # Generate directory tree
    tree = get_directory_tree(directory, exclude_patterns)

    # Collect and process files
    files_content = []

    # Convert extensions to set for faster lookup
    extensions_set = set(ext.lower() for ext in extensions)

    for file_path in directory.rglob("*"):
        # Skip excluded paths
        if should_exclude(file_path, exclude_patterns):
            continue

        if file_path.is_file():
            # Check if file extension matches
            if file_path.suffix.lower() in extensions_set:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Clean content
                    cleaned_content = clean_content(content)

                    # Get relative path from input directory
                    relative_path = file_path.relative_to(directory)

                    # Add to files content list
                    files_content.append(
                        f"<{relative_path}>\n{cleaned_content}\n</{relative_path}>"
                    )
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Write output file
    with open(output_file, "w", encoding="utf-8") as f:
        # Write directory tree
        f.write("Directory Structure:\n")
        f.write(tree)
        f.write("\n\nFiles Content:\n")

        # Write files content
        f.write("\n\n".join(files_content))


def main():
    parser = argparse.ArgumentParser(
        description="Convert project files to a prompt-friendly format"
    )
    parser.add_argument("directory", help="Directory to process")
    parser.add_argument(
        "--extensions",
        nargs="+",
        default=[".py", ".js", ".java", ".cpp", ".h", ".cs", ".rb"],
        help="File extensions to include (e.g., .py .js .java)",
    )
    parser.add_argument("--output", default="prompts.txt", help="Output file name")
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=list(DEFAULT_EXCLUDES),
        help="Patterns to exclude (e.g., .git __pycache__ *.pyc)",
    )

    args = parser.parse_args()

    # Ensure extensions start with dot
    extensions = [ext if ext.startswith(".") else f".{ext}" for ext in args.extensions]

    process_directory(args.directory, extensions, set(args.exclude), args.output)
    print(f"Processing complete. Output written to {args.output}")


if __name__ == "__main__":
    main()
