# Gemini List Mapper

A robust, chunk-based, and cache-enabled Python library for mapping a list of strings to another list using Google's Gemini models. Designed for high-accuracy, large-scale tasks like batch translation, ensuring output consistency and resilience against API failures.

[![PyPI version](https://badge.fury.io/py/gemini-list-mapper.svg)](https://badge.fury.io/py/gemini-list-mapper)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Key Features

- **High-Precision Protocol**: Utilizes an "Individually Numbered Item Protocol" (`<item id="n">...</item>`) to force strict one-to-one mapping, virtually eliminating alignment errors.
- **File-Based Workflow**: Splits large tasks into smaller file-based chunks for maximum robustness.
- **Automatic Caching & Resumption**: Automatically caches results for each chunk. If the process is interrupted, it resumes exactly where it left off, saving time and API costs.
- **Targeted Rework**: Simply delete the output file for any chunk you're unsatisfied with, and the workflow will automatically re-process only that chunk.
- **Configuration-Driven**: Define all your tasks, models, and prompt templates in a clean, human-readable `config.yml` file.
- **Smart Initialization**: Automatically creates a default `config.yml` on first use, making setup effortless.
- **Progress Tracking**: Uses `tqdm` to provide clear, real-time progress bars for file processing.

## Installation

You can install the library directly from PyPI:

```bash
pip install gemini-list-mapper
```

This will also install all necessary dependencies, including `google-generativeai`, `PyYAML`, `numpy`, and `tqdm`.

## Quickstart

This library is designed to be used within a workflow script that manages file operations. An example workflow script is provided to handle large subtitle translation tasks.

### Step 1: Set Up Your Google API Key

First, ensure your Google AI API key is available as an environment variable:

```bash
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

### Step 2: Prepare Your Input File

Your input should be a JSON file containing a list of subtitles, like this:

**`my_subtitles.json`**:
```json
{
  "subtitles": [
    {
      "id": 1,
      "start_time": "00:00:01,000",
      "end_time": "00:00:03,000",
      "text": "你好世界"
    },
    {
      "id": 2,
      "start_time": "00:00:04,000",
      "end_time": "00:00:06,000",
      "text": "这是一个测试"
    }
  ]
}
```

### Step 3: Create and Run a Workflow Script

Create a Python script to manage the translation process. The library is designed to be called by a controller script like the one below.

**`run_my_translation.py`**:
```python
import os
from gemini_list_mapper import SubtitleWorkflowManager # Assuming you place the class in the library

# --- User Configuration ---
INPUT_FILE = 'my_subtitles.json'
TASK_NAME = 'translate_subtitles' # Must match a task in your config.yml
TARGET_LANG_CODE = 'en'
CHUNK_SIZE = 60 # How many subtitles per file chunk

# --- Execution ---
if __name__ == '__main__':
    # On first run, this will auto-generate a `config.yml` for you.
    # Feel free to inspect and customize it.
    manager = SubtitleWorkflowManager(
        input_file=INPUT_FILE,
        task_name=TASK_NAME,
        target_lang_code=TARGET_LANG_CODE,
        chunk_size=CHUNK_SIZE
    )
    
    # This single command handles everything:
    # splitting, translating (with caching), and combining.
    manager.run_all()
```
*(Note: The `SubtitleWorkflowManager` class is provided in the `examples` directory of the source repository as a best-practice implementation.)*

### Step 4: Run the Workflow

Execute your script from the terminal:

```bash
python run_my_translation.py
```

The script will create a `workflow_my_subtitles_en` directory containing three sub-folders:
- `1_source_chunks/`: The original file split into smaller, numbered chunks.
- `2_translated_chunks/`: The translated output for each corresponding source chunk.
- `3_final_output/`: The final, combined, translated JSON file.

### Step 5: Review and Rework (If Needed)

If you find a translation in `chunk_0005.json` is not satisfactory:
1.  **Delete the file**: `rm workflow_my_subtitles_en/2_translated_chunks/chunk_0005.json`
2.  **Re-run the script**: `python run_my_translation.py`

The workflow will notice the missing file, re-translate **only that chunk**, and then re-combine everything into the final output.

## Configuration (`config.yml`)

The library is controlled by a `config.yml` file, which is automatically created on first use. You can customize tasks, models, and prompts within this file.

Here is the default configuration, which uses a high-precision protocol for translation:

```yaml
# config.yml
tasks:
  translate_subtitles:
    model: 'gemini-1.5-flash-latest'
    prompt_template: |
      # ROLE:
      You are a high-precision, item-by-item translation engine.

      # PROTOCOL:
      1. You will receive a list of items, each tagged with a unique ID like `<item id="n">...</item>`.
      2. Your task is to translate the content inside each item tag from {source_lang} to {target_lang}.
      3. Your response MUST be a list of items with the EXACT SAME IDs, in the EXACT SAME order, using the same `<item id="n">...</item>` format.
      4. DO NOT merge, drop, or add any items.
      5. Only the translated text should be inside the tags.

      # DATA TO PROCESS:
      {list_items}

    default_variables:
      source_lang: 'Chinese'
      target_lang: 'English'
```

<!-- ## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/your_username/gemini-list-mapper/issues). -->

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.