# /valuta — Estrai soluzioni e valuta gli studenti

Leggi `valutazioni/ISTRUZIONI.md` per i criteri di valutazione, poi esegui i passi seguenti nell'ordine.

## Passo 1 — Estrai i sorgenti e i conteggi

Esegui lo script dalla directory `valutazioni/`:

```bash
cd valutazioni && .venv/bin/python3 estrai_soluzioni.py
```

Lo script produce:

- `valutazioni/soluzioni/<Nome Cognome>/<esercizio>-N.py` — i sorgenti da leggere
- `valutazioni/conteggi.csv` — colonne `nome,email,numero_esercizi,totale_consegne` calcolate in Python

## Passo 2 — Leggi e analizza i sorgenti

Per ogni directory studente in `valutazioni/soluzioni/`:

- Leggi tutti i file `.py`
- Analizza la qualità del codice secondo i criteri in ISTRUZIONI.md (logica, correttezza concettuale, stile Python)
- **Non eseguire il codice né controllare la sintassi**
- Se ci sono più consegne dello stesso esercizio (`-1.py`, `-2.py`, …), tieni conto dell'evoluzione
- Produci per ogni studente: un voto (A–D) e un giudizio breve (1-2 righe)
- **Non menzionare i conteggi nel giudizio**: sono già in `conteggi.csv`

## Passo 3 — Scrivi valutazioni/valutazioni.csv

Leggi `valutazioni/conteggi.csv` e fai il join con i giudizi del passo 2 usando `nome` come chiave.
Scrivi `valutazioni/valutazioni.csv` con le colonne nell'ordine:

```csv
nome,email,numero_esercizi,totale_consegne,voto,giudizio
```

Le colonne `nome`, `email`, `numero_esercizi`, `totale_consegne` vengono da `conteggi.csv` così come sono.
Le colonne `voto` e `giudizio` vengono dall'analisi AI del passo 2.

Escludi sempre la voce con email `massimo.santini@unimi.it` (entry di test del docente) — lo script la filtra già.
