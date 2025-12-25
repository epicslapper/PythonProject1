TicketProjectFolder/
└── parent/
    ├── main.py          # Single source of truth
    ├── validate.py      # Helper / validation functions
    └── sync.py          # Auto-sync script
          │
          ▼
    ┌───────────────────┐
    │   sync.py copies   │
    │   files to child   │
    │   projects         │
    └───────────────────┘
          │
          ▼
┌───────────────────┐      ┌───────────────────┐
│   PP_3_13         │      │   PP_3_14         │
│ ┌───────────────┐ │      │ ┌───────────────┐ │
│ │ .venv/        │ │      │ │ .venv/        │ │
│ │ pyproject.toml│ │      │ │ pyproject.toml│ │
│ │ uv.lock       │ │      │ │ uv.lock       │ │
│ │ requirements.txt│     │ │ requirements.txt│ │
│ │ runtime.txt   │ │      │ │ runtime.txt   │ │
│ └───────────────┘ │      │ └───────────────┘ │
└───────────────────┘      └───────────────────┘
          │                        │
          ▼                        ▼
┌───────────────────┐      ┌───────────────────┐
│ Streamlit run     │      │ Streamlit run     │
│ Python 3.13       │      │ Python 3.14       │
│ main.py → app     │      │ main.py → app     │
└───────────────────┘      └───────────────────┘
