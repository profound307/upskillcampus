# Student Management System

A professional, modular Student Management System (SMS) built using Python 3, Object-Oriented Programming (OOP), and JSON-based file persistence. This application supports two modes of interaction:
1. **Console CLI Application**: A clean menu-driven command-line terminal client.
2. **Full-Stack Web Portal**: A beautiful, modern glassmorphic dashboard interface powered by a lightweight Flask backend and custom Vanilla CSS.

Both applications share the exact same underlying logic layer and database file, ensuring real-time synchronicity of student records.

---

## Folder Structure

```
student_management_system/
│
├── main.py                 # Console CLI Entry Point
├── app.py                  # Flask Web Server Entry Point
├── student.py              # Student Class definitions & validations
├── manager.py              # StudentManager Class (persistence & operations)
│
├── data/
│   └── students.json       # Shared JSON file persistence database
│
├── static/                 # Web assets
│   ├── css/
│   │   └── style.css       # Custom premium glassmorphic stylesheet
│   └── js/
│       └── app.js          # Asynchronous frontend client-side scripts
│
├── templates/
│   └── index.html          # Responsive Web App dashboard layout
│
├── requirements.txt        # Dependency file (primarily Flask)
├── README.md               # Quickstart & setup guide
├── report.md               # Project report & documentation
└── test_logic.py          # Automated unittest test suite
```

---

## Features

### Core Operations
- **Add Student**: Insert new student records with automatic validation.
- **View All Students**: Retrieve and list records in an elegant CLI table or web dashboard.
- **Search Student by ID**: Quickly lookup specific students by their unique identification key.
- **Update Student**: Modify existing information while maintaining strict validations.
- **Delete Student**: Erase student records from persistence.
- **Sorting**: Order students by Name alphabetically or by Marks (descending).

### strict Validations
- **Prevent Duplicate IDs**: Automatically intercepts duplicate primary keys.
- **Email Format**: RegEx patterns check for proper standard structure.
- **Marks Constraint**: Ensures values remain strictly between `0` and `100` inclusive.
- **Age Bounds**: Age must be greater than `0`.

---

## Installation & Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.14.2)
- Virtual Environment tool (`venv`) recommended

### Steps
1. Navigate to the project root directory:
   ```bash
   cd student_management_system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **On Windows**:
     ```powershell
     .\venv\Scripts\activate
     ```
   - **On macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage Instructions

### 1. Launching the Console CLI Client
To start the interactive command-line client, run:
```bash
python main.py
```
This launches the text menu dashboard. Follow the on-screen numbers (1-8) to manage students.

### 2. Launching the Web Portal (Full Stack)
To run the local server and open the web dashboard:
1. Start the Flask dev server:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
3. Use the visual dashboard, modal forms, sorting keys, search boxes, and deletion prompts.

### 3. Running Automated Tests
To execute the unit test suite and verify the validation library:
```bash
python -m unittest test_logic.py
```
