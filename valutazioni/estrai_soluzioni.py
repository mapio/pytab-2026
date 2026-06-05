#!/usr/bin/env python3
"""
Legge soluzioni.xlsx e produce:
  - soluzioni/<Nome Cognome>/<esercizio>-N.py   (una per ogni consegna)
  - conteggi.csv  (nome, email, numero_esercizi, totale_consegne)

N è il numero progressivo di consegna per quell'esercizio (1, 2, ...).
"""
import csv
import re
import sys
from pathlib import Path

try:
    import openpyxl
except ImportError:
    sys.exit("Installa openpyxl: uv pip install openpyxl")

SKIP_EMAIL = 'massimo.santini@unimi.it'
XLSX      = Path(__file__).parent / 'soluzioni.xlsx'
OUT       = Path(__file__).parent / 'soluzioni'
CONTEGGI  = Path(__file__).parent / 'conteggi.csv'


def slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[/\\]', '-', text)
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text


def main():
    wb = openpyxl.load_workbook(XLSX)
    ws = wb.active

    # {(nome, email): {esercizio: n_consegne}}  — ordine di prima apparizione
    students: dict[tuple, dict] = {}
    written = 0

    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i == 0:
            continue
        _, _, _, email, nome, esercizio, soluzione = row
        if email == SKIP_EMAIL:
            continue

        key = (nome, email)
        if key not in students:
            students[key] = {}

        n = students[key].get(esercizio, 0) + 1
        students[key][esercizio] = n

        dest = OUT / nome / f"{slug(esercizio)}-{n}.py"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(soluzione or '', encoding='utf-8')
        print(f"  {dest.relative_to(OUT.parent)}")
        written += 1

    # conteggi.csv
    with CONTEGGI.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['nome', 'email', 'numero_esercizi', 'totale_consegne'])
        for (nome, email), exs in sorted(students.items()):
            w.writerow([nome, email, len(exs), sum(exs.values())])

    print(f"\n{written} file scritti per {len(students)} studenti in {OUT.relative_to(OUT.parent.parent)}/")
    print(f"{CONTEGGI.name} aggiornato ({len(students)} righe)")


if __name__ == '__main__':
    main()
