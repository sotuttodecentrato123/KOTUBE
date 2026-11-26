# KOTUBE

Trascrive video YouTube in testo, con esportazione in TXT, DOCX e ODT.

Usa i sottotitoli del video quando disponibili (italiano o inglese); se non ci
sono, scarica l'audio e lo trascrive con Whisper.

## Requisiti

- Windows (i launcher sono .bat/.ps1)
- Python 3.10+ (testato con Python 3.13)
- Node.js consigliato per yt-dlp (estrazione dei formati YouTube)
- Connessione internet

## Installazione

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Avvio

- Doppio clic su `Avvia_KOTUBE.bat`
- oppure:

```powershell
.venv\Scripts\python.exe KOTUBE.py
```

Si apre il browser su http://127.0.0.1:48217/

## Arresto

- Doppio clic su `Ferma_KOTUBE.bat`
- oppure chiudere il processo `pythonw.exe`

## Note

- I video senza sottotitoli usano faster-whisper: al primo uso viene scaricato
  il modello `medium` (circa 1,5 GB) e la trascrizione richiede qualche minuto.
- I sottotitoli cercati sono `it` e `en`.
- I file generati finiscono nella cartella `output/` (esclusa da Git).
- La `.venv` non e' inclusa nel repository: va ricreata con i comandi sopra.

## Struttura

```text
KOTUBE.py          applicazione Flask
trascrizione.py    download, sottotitoli e Whisper
requirements.txt   dipendenze Python
Procfile           avvio con gunicorn (deploy)
static/            loghi IT/EN/JA
avvia_kotube.py    launcher Python
Avvia_KOTUBE.bat   avvio Windows
Ferma_KOTUBE.bat   arresto Windows
ferma_kotube.ps1   script di arresto
kotube.ico         icona avvio
kotube_stop.ico    icona arresto
```

## Repository

https://github.com/sotuttodecentrato123/KOTUBE