import requests
import nbformat
from nbformat.v4 import new_notebook, new_code_cell

def fetch(note_id, notebook_path=None):
    url = f"https://api.dontpad.com/{note_id}.body.json?lastModified=0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        body = response.json().get("body", "")
        
        if not body.strip():
            raise ValueError("Note is empty or not found.")
        
        nb = new_notebook()
        nb.cells.append(new_code_cell(body))

        if notebook_path is None:
            notebook_path = f"{note_id}.ipynb"
        
        with open(notebook_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        
        print(f"Notebook saved to: {notebook_path}")
        return notebook_path
    except Exception as e:
        print("Error fetching or saving notebook:", e)
        return None
