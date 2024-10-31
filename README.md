# Web Scraping MiniProject
010123105 Statistics for Computer Engineers CprE. KMUTNB BKK


## Setup
**Activate the virtual environment**:
- **On Windows**:
```bash
python -m venv webscraping_env
.\webscraping_env\Scripts\activate
```

- **On macOS and Linux**:
```bash
python3 -m venv webscraping_env
source webscraping_env/bin/activate
```

**Install Required Libraries**:
```bash
pip install selenium
pip install bs4
pip install matplotlib
pip install schedule
```

## Running the Project
```bash
python src/scrapingData.py
python src/visualizeData.py
```