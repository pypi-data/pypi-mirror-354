# LLM Anonymizer

A CLI tool to anonymize code using a local LLM before sending to Claude Code or other AI services.

## Prerequisites

### Install Ollama

1. **macOS/Linux:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Windows:**
   Download from [ollama.ai](https://ollama.ai/download)

3. **Start Ollama service:**
   ```bash
   ollama serve
   ```

4. **Install a model (in a new terminal):**
   ```bash
   # Install Llama 3.2 (recommended)
   ollama pull llama3.2
   
   # Or install other models
   ollama pull codellama
   ollama pull llama3.1
   ```

### Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd llm-anon
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Basic Usage

```bash
# Anonymize a single file and print to stdout
uv run python -m llm_anon.cli example.py

# Anonymize and save to file
uv run python -m llm_anon.cli example.py -o anonymized.py

# Process entire directory
uv run python -m llm_anon.cli src/ -r -o anonymized_output/
```

### Options

- `-o, --output PATH`: Output file or directory
- `-m, --model TEXT`: LLM model to use (default: llama3.2)
- `-t, --temperature FLOAT`: Temperature for generation (default: 0.1)
- `--preserve-comments`: Keep original comments
- `--preserve-strings`: Keep string literals unchanged
- `-r, --recursive`: Process directories recursively
- `-v, --verbose`: Show detailed progress
- `--validation-config PATH`: Path to validation config file with banned strings
- `--max-retries INTEGER`: Maximum retries for validation failures (default: 3)

### Examples

```bash
# Use different model with higher creativity
uv run python -m llm_anon.cli code.py -m codellama -t 0.3

# Preserve important strings and comments
uv run python -m llm_anon.cli api.py --preserve-strings --preserve-comments

# Process entire project with verbose output
uv run python -m llm_anon.cli ./src -r -v -o ./anonymized

# Use validation to ensure sensitive strings are removed
uv run python -m llm_anon.cli code.py --validation-config banned_strings.txt -v

# Process with custom retry limit for stubborn validations
uv run python -m llm_anon.cli sensitive_code.py --validation-config company_secrets.txt --max-retries 5
```

## Supported Languages

- Python (.py)
- JavaScript (.js, .jsx)
- TypeScript (.ts, .tsx)
- Java (.java)
- C/C++ (.c, .cpp, .cc, .cxx, .h, .hpp)
- Rust (.rs)
- Go (.go)

## Validation System

The tool includes a powerful validation system to ensure sensitive information is completely removed from anonymized code.

### Creating a Validation Config

Create a text file with banned strings (one per line):

```txt
# company_secrets.txt
# Company names and branding
MyCompany
mycompany.com

# API keys and credentials  
API_KEY_12345
secret_password_2024

# Contact information
support@mycompany.com
1-800-MYCOMPANY

# Product-specific terms
MyCompanyCustomer
MyCompanyLicenseManager
```

### How Validation Works

1. **Initial Anonymization**: LLM processes code normally
2. **String Detection**: Scans output for banned strings using word boundaries
3. **Re-prompting**: If banned strings found, sends explicit removal instructions
4. **Retry Logic**: Repeats up to `--max-retries` times until validation passes
5. **Failure Handling**: Reports specific banned strings if validation ultimately fails

### Validation Features

- **Case-sensitive matching** by default
- **Word boundary detection** prevents false positives
- **Progressive prompting** gets more explicit with each retry
- **Detailed error reporting** shows exactly which strings were found

## How It Works

1. **File Detection**: Automatically detects programming language from file extension
2. **LLM Processing**: Sends code to local Ollama model with anonymization prompt
3. **Validation** (if enabled): Checks output against banned strings and re-prompts if needed
4. **Smart Replacement**: Replaces variable names, function names, and identifiers while preserving:
   - Code structure and logic
   - Control flow
   - Data types
   - Import statements
   - Syntax and formatting

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama service
pkill ollama && ollama serve

# List available models
ollama list
```

### Model Not Found

```bash
# Pull the default model
ollama pull llama3.2

# Or specify a different model
uv run python -m llm_anon.cli code.py -m llama3.1
```

### Performance Tips

- Use smaller models for faster processing: `llama3.2:1b`
- Lower temperature (0.1) for more consistent results
- Process files individually for large codebases to avoid timeouts