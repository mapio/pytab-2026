# Istruzioni per la valutazione degli studenti

## Contesto

Corso Python di base per personale tecnico (università). La valutazione finale è "abilitato/non abilitato" senza voto numerico. È preferibile che tutti risultino abilitati. Le soluzioni agli esercizi si trovano in `soluzioni.xlsx` nella stessa cartella.

## Struttura del foglio Excel

Colonne: `Id | Ora di inizio | Ora di completamento | Posta elettronica | Nome | Esercizio | Soluzione`

- Uno stesso studente può avere più righe (una per esercizio consegnato, o revisioni dello stesso esercizio)
- La chiave studente è la coppia `(Posta elettronica, Nome)`
- La voce con email `massimo.santini@unimi.it` è un'entry di test del docente: **escluderla sempre**

## Esercizi del corso

1. Cognome in AL/MZ – input, confronto stringhe, condizionale
2. Conta le vocali – iterazione su stringa, contatore
3. Sequenze di Collatz – ciclo while con condizione di terminazione
4. Tabellina formattata – cicli annidati, formattazione output
5. Codifica ROT13 – aritmetica su caratteri (esercizio avanzato)
6. Secondo esercizio – variante (alcuni studenti consegnano più esercizi in un'unica risposta)

## Criteri di valutazione

La valutazione è qualitativa (non sintattica): **non eseguire il codice né controllare la sintassi**. Valutare la logica, la chiarezza e la correttezza concettuale.

| Voto | Significato |
| ---- | ----------- |
| A | Codice corretto, pulito, idiomatico Python; padronanza evidente |
| B | Funzionante con difetti minori (stile, ridondanze, piccoli errori logici) |
| C | Comprende i concetti di base ma con errori significativi (bug logici, sintassi errata, codice incompleto) |
| D | Assenza di comprensione; da usare solo in casi estremi |

Dato il contesto del corso, **preferire C a D** quando lo studente mostra almeno comprensione parziale dei concetti.

## Errori tipici da considerare nella valutazione

- **Confronto stringhe per cognome**: `< 'M'` è la forma corretta (robusta); `<= 'L'` ha edge case problematici; `< 'L'` è errato (esclude L)
- **Ciclo di Collatz**: deve avere un `while` che termina su `n == 1`; soluzioni con un solo passo (senza ciclo) sono incomplete
- **Conteggio vocali**: il `print` deve stare fuori dal ciclo for
- **Divisione intera**: usare `//` in Python 3; `/` restituisce float
- **Variabili non definite**: riferimento a variabile mai assegnata è un errore concettuale
- **Uso scorretto di `or`**: `print('A') or print('B')` stampa entrambi (None è falsy)

## Alberatura dei sorgenti estratti

Lo script `estrai_soluzioni.py` popola `valutazioni/soluzioni/` con questa struttura:

```text
valutazioni/soluzioni/
├── Nome Cognome/
│   ├── <esercizio>-1.py      ← prima consegna
│   ├── <esercizio>-2.py      ← eventuale revisione
│   └── ...
└── ...
```

Il nome dell'esercizio viene slugificato (lowercase, spazi → trattini, caratteri speciali rimossi).  
Esempi: `cognome-in-al-mz-1.py`, `sequenze-di-collatz-2.py`.

## Output atteso

File CSV `valutazioni.csv` con colonne:

```csv
nome,email,numero_esercizi,totale_consegne,voto,giudizio
```

- `nome`: nome e cognome dello studente
- `email`: indirizzo email
- `numero_esercizi`: quanti esercizi distinti ha consegnato (conta una volta anche se riconsegnato)
- `totale_consegne`: numero totale di righe nel foglio (include revisioni dello stesso esercizio)
- `voto`: lettera da A a D
- `giudizio`: frase breve (1-2 righe) su punti di forza e debolezza; **non menzionare i conteggi**, che sono già nelle colonne dedicate

## Come rigenerare le valutazioni

1. Aggiornare `soluzioni.xlsx` con le nuove soluzioni
2. Dalla directory `valutazioni/`, eseguire lo script di estrazione:

   ```bash
   .venv/bin/python3 estrai_soluzioni.py
   ```

   Questo sovrascrive i file in `soluzioni/` con i contenuti aggiornati.

3. Aprire una conversazione con Claude nel contesto di questo repository
4. Digitare `/valuta` per avviare il flusso guidato di estrazione + valutazione

## Skill `/valuta`

Il comando `/valuta` (definito in `.claude/commands/valuta.md`) esegue in sequenza:

1. Lancia `estrai_soluzioni.py` per aggiornare l'alberatura `soluzioni/`
2. Legge i file `.py` per studente
3. Analizza il codice secondo i criteri di questo documento
4. Riscrive `valutazioni.csv`

## Ambiente

- Python: `uv venv --no-project` + `uv pip install openpyxl` nella cartella `valutazioni/`
- Lettura Excel: `openpyxl`
- Script di estrazione: `valutazioni/estrai_soluzioni.py`
