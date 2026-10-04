# Setup Guide: Python and VS Code

No need to complete this before Seminar 1 on Saturday 8/29. Bring your laptop to Seminar 1. This is what that session is for.

**You will install:**

- Python 3: the programming language
- Visual Studio Code (VS Code): the editor you will use to write and run code

---

## Step 1: Install Python

### Windows

1. Go to [python.org/downloads](https://python.org/downloads) and download the latest Python 3.x installer.
2. Run the installer.
3. **On the first screen, check "Add Python to PATH" before clicking Install Now.** If you skip this, Python will not run from the terminal.
4. Click **Install Now** and wait for it to finish.

### Mac

1. Go to [python.org/downloads](https://python.org/downloads) and download the latest Python 3.x installer (`.pkg` file).
2. Open the file and follow the installer steps. No extra options needed.

---

## Step 2: Install VS Code

1. Go to [code.visualstudio.com](https://code.visualstudio.com) and download the installer for your operating system.
2. Run the installer with default settings.
3. Open VS Code.

---

## Step 3: Install the Python Extension

1. In VS Code, click the **Extensions** icon in the left sidebar (four squares).
2. Search for **Python**.
3. Install the extension published by **Microsoft** (first result).

The first time you open a `.py` file, VS Code will ask you to select a Python interpreter. Choose the Python 3.x version you just installed.

---

## Step 4: Open Your Files

1. Pull the latest from your fork of the course GitHub repo (`github.com/AdaptiveMesh/cs5045`). The files are under `M1/`: `example.py` and `health_survey.csv`.
2. Save both files in the same folder on your computer.
3. In VS Code: **File → Open Folder** and select that folder.

Both files should appear in the left panel.

---

## Step 5: Run the Program

1. Open a terminal inside VS Code: **Terminal → New Terminal**.
2. Type the following and press Enter:

**Windows:**
```
python example.py
```

**Mac:**
```
python3 example.py
```

You should see several lines of output: a formatted summary of a small health dataset. If you see output, your environment is working. Copy that output; you'll need it for the assignment submission (see `assignment.md`).

---

## Troubleshooting

**"python is not recognized" / "command not found" (Windows):**
Python was not added to PATH. Uninstall Python, reinstall it, and check the "Add to PATH" box on the first screen.

**"python is not recognized" / "command not found" (Mac):**
Try `python3` instead of `python`.

**VS Code does not find your Python installation:**
Look at the bottom status bar in VS Code. Click where it says "Select Interpreter" and choose Python 3.x from the list.

**Nothing works:**
Bring your laptop to Seminar 1 on 8/29. You will not be the only one with a problem, and we will get it sorted.
