import csv

def run(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return {"rows": len(rows), "columns": list(rows[0].keys()) if rows else []}