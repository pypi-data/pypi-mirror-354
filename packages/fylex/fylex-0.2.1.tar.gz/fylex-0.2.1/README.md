

# fylex

**Smart, Safe & Customizable File Operations Toolkit**


`fylex` is a Python-powered CLI utility and library that enables **high-performance file copying and moving** with content-aware logic, parallel execution, and advanced filtering. Built for developers, sysadmins, and data engineers who need **reliable and configurable file operations** across platforms.

##

##  Key Highlights

*  **Hash-Based File Comparison** — skip identical files using `xxhash`
*  **Multithreaded Copying** — speed up transfers using `ThreadPoolExecutor`
*  **Advanced Filtering** — include/exclude via glob, regex, or filenames
*  **Robust Conflict Handling** — resolve duplicates by size, time, rename, etc.
*  **Interactive + Dry-Run Modes** — test your actions before committing
*  **Logging & Summary Files** — track operations with optional logs
*  **Preserves Metadata** — timestamps and permissions retained

##

## Why `fylex`?

Most tools either **blindly copy everything** or **require complex scripting** to filter and verify safely. `fylex` offers a smarter alternative:


| Criteria                           | `fylex`                                   | `rsync`                       | `shutil` / `distutils`  | `robocopy` (Windows)       | Other Python libs (e.g. `send2trash`, `dirsync`) |
| ---------------------------------- | ------------------------------------------------------ | ----------------------------- | ----------------------- | -------------------------- | ------------------------------------------------ |
| **Hash-based change detection**    | ✅ Uses `xxhash` to skip identical files efficiently    |  Optional via checksum      | ❌ Metadata only         | ❌ File size/time only      |  Varies per lib                                |
| **Multi-threaded copy**            | ✅ `ThreadPoolExecutor`-based parallelism               | ❌ Mostly single-threaded      | ❌ Single-threaded       | ✅ Parallelization possible | ❌ Usually sequential                             |
| **Regex + Glob + Name filtering**  | ✅ Supports all three (rare combo)                      |  Basic include/exclude      | ❌ Minimal support       |  Mask-based filtering    |  Usually only glob                             |
| **Conflict resolution strategies** | ✅ `skip`, `replace`, `rename`, `larger`, `newer`, etc. |  `--update`, overwrite-only | ❌ Must handle manually  |  Some file age support   | ❌ Very limited logic                             |
| **Smart move**                     | ✅ Adds verified delete after copy                      | ❌ Requires manual delete      | ❌ No move-and-check     | ❌ Overwrites or fails      | ❌ Not built-in                                   |
| **Interactive prompts**            | ✅ Asks on conflict (optional)                          | ❌ No CLI interactivity        | ❌ No interactivity      | ❌ Batch/script-oriented    | ❌ Rare                                           |
| **Dry-run mode**                   | ✅ Simulates full operation                             | ✅ `--dry-run`                 | ❌ Not available         | ✅ `/L` option              |  Sometimes                                     |
| **Preserves metadata**             | ✅ Via `shutil.copy2()`                                 | ✅ Preserves most metadata     |  Partial (copy2 only) | ✅ Full metadata support    |  Limited                                       |
| **Logging and Summary**            | ✅ Optional logs and summary file                       |  Logs via stdout            | ❌ No logs               | ✅ Built-in logs            | ❌ Rare                                           |
| **CLI + API support**              | ✅ Both available                                       | ❌ CLI-only                    |  Python-only          | ✅ CLI only                 |  API only                                      |
| **Cross-platform**                 | ✅ Full (Linux, macOS, Windows)                         | ✅ Mostly                      | ✅ Yes                   | ❌ Windows-only             |  Varies                                        |
| **Extensibility / Modularity**     | ✅ Modular design, easy to plug in new behaviors        | ❌ Hard to extend              | ✅ For basic scripting   | ❌ Not scriptable           |  Sometimes messy                               |
| **Active UI feedback (UX)**        | ✅ Supports verbose/dry-run interactions                | ❌ Silent unless verbose       | ❌ No feedback           |  Some progress reports   | ❌ Often silent                                   |

##

## Positioning Strategy for `fylex`

| Target Audience              | How `fylex` Fits Them                                                |
| ---------------------------- | -------------------------------------------------------------------- |
| **Developers / Engineers**   | Precise control via regex/glob/API, great for devops/data copying    |
| **Data Analysts**            | Safe bulk copy/move of large datasets, with dry-run + summary        |
| **Researchers / Archivists** | Reliable deduplication & backup tool for sensitive files             |
| **Open Source Users**        | A modern `rsync` alternative with user-friendly interface            |
| **Sysadmins / Automators**   | CLI + script combo makes it usable in crons or custom Python scripts |


##

## CLI Usage

### Syntax

```bash
fylex copy SRC DEST [options]
fylex move SRC DEST [options]
```

### Options (shared between `copy` and `move`)

| Option                | Description                                                        |
| --------------------- | ------------------------------------------------------------------ |
| `--match-glob`        | Include only files matching this glob pattern (`*.txt`, etc.)      |
| `--match-regex`       | Include files matching this regular expression                     |
| `--match-names`       | Include only listed filenames (space-separated)                    |
| `--exclude-glob`      | Exclude files by glob pattern                                      |
| `--exclude-regex`     | Exclude files by regex                                             |
| `--exclude-names`     | Exclude specific filenames (space-separated)                       |
| `--on-conflict`       | Strategy for file name conflicts (`rename`, `newer`, `skip`, etc.) |
| `--interactive`, `-i` | Prompt before each operation                                       |
| `--dry-run`           | Simulate actions without copying/moving                            |
| `--verbose`, `-v`     | Show detailed logs in terminal                                     |
| `--summary`           | Path to save a summary log file                                    |
| `--max-workers`       | Number of threads to use (default: 4)                              |
| `--no-create`         | Do not create destination directories if missing                   |

##

### 🔸 Examples

#### Copy Only `.txt` Files, Renaming on Conflict

```bash
fylex copy ./docs ./archive --match-glob '*.txt' --on-conflict rename
```

#### Move Files Except `.log` With Prompt, and Let the Larger Prevail

```bash
fylex move ./input ./output --exclude-glob '*.log' --on-conflict larger --interactive
```

#### Simulate Full Copy with Detailed Log

```bash
fylex copy ./dataset ./backup --dry-run --verbose --summary summary.log
```

##

## Python API

You can use `fylex` programmatically within your Python code for custom workflows:

```python
from fylex import copyfiles, movefiles

# Example: Copy with custom filters
copyfiles(
    src="./input",
    dest="./output",
    match_glob="*.csv",
    exclude_names=["debug.csv"],
    on_conflict="newer",
    interactive=False,
    dry_run=False,
    max_workers=8,
    summary="summary.log",
    verbose=True
)
```

```python
# Example: Move and rename if duplicate exists
movefiles(
    src="./download",
    dest="./archive",
    on_conflict="rename",
    interactive=False
)
```

##

##  Conflict Resolution Modes

| Mode      | Description                                           |
| --------- | ----------------------------------------------------- |
| `replace` | Always overwrite destination                          |
| `skip`    | Do not copy if destination exists                     |
| `rename`  | Auto-rename to avoid overwriting (e.g. `file(1).txt`) |
| `prompt`  | Ask user what to do for each conflict                 |
| `newer`   | Keep the most recently modified file                  |
| `older`   | Keep the oldest version                               |
| `larger`  | Keep the larger file                                  |
| `smaller` | Keep the smaller file                                 |

##

##  Dry Run & Logging

* `--dry-run`: shows what would happen without touching the disk
* `--verbose`: detailed log of every matched and skipped file
* `--summary`: logs all decisions and actions to a file

##

##  Installation

Install via PyPI:

```bash
pip install fylex
```

Or install from source:

```bash
git clone https://github.com/Crystallinecore/fylex
cd fylex
pip install .
```

##

##  Dependencies

* Python 3.8+
* `xxhash`: For high-speed hashing

```bash
pip install xxhash
```

##

## License

MIT License © Sivaprasad Murali — https://github.com/Crystallinecore/fylex

xxHash used under BSD License — [https://github.com/Cyan4973/xxHash](https://github.com/Cyan4973/xxHash)

##

##  Author

**Sivaprasad Murali** —
[sivaprasad.off@gmail.com](mailto:sivaprasad.off@gmail.com)


##
>  *“Your files. Your rules. Just smarter.”*
##


