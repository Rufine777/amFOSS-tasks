# Task 04

1. **Import Movies:** Run `import_csv.py` to populate the database from `movies.csv`.  
2. **Connect & Query:** `dashboard2.py` uses `connector.py` to fetch data based on user interactions.  
3. **Interact & Export:** Users search, filter, select columns, and export data through the dashboard GUI.

---

## Features

- Search movies by **genre, year, rating, director, or actor**.  
- Select which **columns to display** in the table.  
- **Export filtered or selected data** to a CSV file.  
- Real-time feedback via the **dashboard console**.

---

## Requirements

- Python 3.9+  
- PySide6  
- mysql-connector-python  
- MySQL database with credentials matching `connector.py`  

---

## Steps to Run the Project (Ubuntu)

### 1.Set up the virtual environment
 ```bash 
python3 -m venv venv
```
### 2. Activate the virtual environment
 ```bash 
source venv/bin/activate
```
### 3.Install dependencies
 ```bash
 pip install -r requirements.txt
```
### 4.Run the file
 ```bash 
python3 dashboard2.py
```

