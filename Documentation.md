# Code Mentor Bot Documentation

## Documentation.md

### Directory Structure
```plaintext
app
├── frontend
│   ├── app.py
│   └── streamlit_app.py
├── main.py
├── models
│   └── code_model.py
├── routers
│   └── code_routes.py
└── services
    ├── code_converter.py
    ├── code_debug.py
    └── complexity_analyzer.py
```

### How to Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kshitijkumrawat20/Code-Mentor-Bot-.git
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI Server**:
   ```bash
   uvicorn Code-Mentor-Bot-.app.main:app --reload
   ```

4. **Start Streamlit (In a New Shell)**:
   ```bash
   cd Code-Mentor-Bot-/app/frontend
   streamlit run app.py
   ```

---

