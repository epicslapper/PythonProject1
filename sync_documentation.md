TicketProjectFolder/
├── parent/
│   ├── main.py          # Parent main source file
│   ├── validate.py      # Validation / helper functions
│   └── sync.py           # Background sync script
│
├── PP_3_13/
│   ├── pyproject.toml   # UV project file (Python 3.13)
│   ├── uv.lock          # Locked dependencies for 3.13
│   ├── requirements.txt # Dependencies for 3.13
│   ├── runtime.txt      # Streamlit Cloud Python version (3.13)
│   └── .venv/           # Virtual environment for Python 3.13
│
├── PP_3_14/
│   ├── pyproject.toml   # UV project file (Python 3.14)
│   ├── uv.lock          # Locked dependencies for 3.14
│   ├── requirements.txt # Dependencies for 3.14
│   ├── runtime.txt      # Streamlit Cloud Python version (3.14)
│   └── .venv/           # Virtual environment for Python 3.14
│
├── requirements.txt     # Optional global dependencies
└── runtime.txt          # Optional global Streamlit Cloud Python version

# Workflow:

1. Edit source files ONLY in the `parent/` folder.
   - main.py, validate.py, etc.
2. Run `sync.py` (manually or auto-start from main.py) to propagate changes:
   - Copies parent files into PP_3_13 and PP_3_14 child projects.
3. Run Streamlit in the desired environment:

   # Python 3.13
   ~/TicketProjectFolder/PP_3_13/.venv/bin/python -m streamlit run main.py

   # Python 3.14
   ~/TicketProjectFolder/PP_3_14/.venv/bin/python -m streamlit run main.py

   - In PyCharm: configure interpreter for each project to point to its .venv
   - No need to manually activate environments

4. Git workflow:
   - GitHub is the source of truth.
   - Commit + push parent and child projects as needed.
   - Pull on other machines to sync projects.
   - Only parent files need editing; child projects auto-updated via sync.py.

# Notes / Considerations:

- Each child project has its own `.venv` and Python version.
- Each child project may have its own `requirements.txt` and `runtime.txt`.
- `sync.py` uses `pathlib` and relative paths, so it works on macOS and Linux.
- Auto-adjust sync interval: faster when parent files change, slower when idle.
- Can add new child projects (e.g., Python 3.15) by creating UV project and updating TARGET_PROJECTS.
- Keep parent files as **single source of truth** to simplify workflow.
- Optional: rename `.venv` folders to `.venv313` / `.venv314` for clarity.
- This setup avoids dependency hell and allows safe multi-Python version testing.
