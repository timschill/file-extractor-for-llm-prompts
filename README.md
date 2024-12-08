# Project to Prompt Converter

A Python utility that converts your project files into a format suitable for Large Language Model (LLM) prompts. It creates a single text file containing your project's directory structure and file contents, optimized for token efficiency.

## Features

- Generates a tree-like directory structure
- Processes files based on specified extensions
- Excludes common development directories/files (.git, **pycache**, etc.)
- Optimizes output for token efficiency by removing unnecessary whitespace
- Formats file contents with XML-style tags for clear structure

## Installation

1. Clone or download this script
2. Ensure you have Python 3.6 or higher installed
3. No additional dependencies required

## Usage

### Basic Usage

```bash
python main.py /path/to/your/project
```

This will create a `prompts.txt` file in your current directory with the default settings.

### Advanced Usage

```bash
python main.py /path/to/your/project \
    --extensions .py .js .tsx \
    --exclude .git __pycache__ build \
    --output custom_prompt.txt
```

### Command Line Arguments

- `directory`: Path to the project directory (required)
- `--extensions`: File extensions to include (default: .py .js .java .cpp .h .cs .rb)
- `--exclude`: Patterns to exclude (default: common development files/folders)
- `--output`: Output file name (default: prompts.txt)

### Default Exclusions

The script automatically excludes these common patterns:

- `.git`, `.gitignore`
- `__pycache__`, `*.pyc`, `*.pyo`, `*.pyd`
- `node_modules`
- `.env`, `.venv`, `venv`
- `.idea`, `.vscode`
- `.DS_Store`, `Thumbs.db`

## Output Format

The generated `prompts.txt` will have this structure:

```
Directory Structure:
├── src/
│   ├── main.py
│   ├── utils/
│   │   ├── helper.py

Files Content:
<src/main.py>
def main():
    print("Hello World")
</src/main.py>

<src/utils/helper.py>
def helper_function():
    return True
</src/utils/helper.py>
```

## Purpose

This tool is designed to help developers prepare their codebase for LLM prompts. It's particularly useful when you want to:

- Get AI assistance with your codebase
- Generate documentation
- Analyze project structure
- Share code context efficiently

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use and modify as needed.
