## How to install and set up the project

### Install Python and SQLite (if needed)
If you don't have Python 3.12 or SQLite installed on your system, follow these steps:
1. **Python 3.12 Installation:**
   - Download Python 3.12 from the [official Python website](https://www.python.org/downloads/) and follow the installation instructions for your operating system.

### Project Setup (Under 1 min)
1. Clone this project
   ``` bash
   git clone https://github.com/Zimzozaur/Pulporo-TUI
   ```
2. Move to project
    ```
    cd Pulporo-TUI
    ```
3. Create virtual env in project directory 
   ```
   python -m venv venv
   ```
4. Activate virtual env:
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     \venv\Scripts\Activate.ps1
     ```
5. Install dependencies from requirements.txt
   ```
   pip install -r requirements.txt
   ```
6. Set env var
```bash
# using export 
export PULPORO_API_URL="what ever you like"
```
7. Run app in terminal - Before run [Pulporo API](https://github.com/Zimzozaur/Pulporo-API) server
   ```
    python main.py
   ```
