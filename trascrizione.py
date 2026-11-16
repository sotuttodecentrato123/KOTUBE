"""
Motore per scaricare e trascrivere video da YouTube.
"""
import re
import sys
import tempfile
from pathlib import Path
import os

import yt_dlp
from docx import Document
from odf.opendocument import OpenDocumentText
from odf.text import H, P

CARTELLA_OUTPUT = Path("output")
LINGUE_SOTTOTITOLI = ["it", "en"]
MODELLO_WHISPER = "medium"
FRASI_PER_PARAGRAFO = 6

# Controlla se il file cookies esiste e lo usa
OPZIONI_BASE = {
    "quiet": True,
    "extractor_args": {"youtube": {"player_client": ["android"]}},
}
if os.path.exists("cookies.txt"):
    OPZIONI_BASE["cookiefile"] = "cookies.txt"

def estrai_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})", url)
    if not m:
        raise ValueError("URL YouTube non valido.")
    return m.group(1)

def titolo_video(url):
    opzioni = OPZIONI_BASE.copy()
    opzioni["skip_download"] = True
    with yt_dlp.YoutubeDL(opzioni) as ydl:
        return ydl.extract_info(url, download=False).get("title", "video")

def prova_sottotitoli(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        try:
            api = YouTubeTranscriptApi()
            parti = api.fetch(video_id, languages=LINGUE_SOTTOTITOLI)
            return [p.text for p in parti]
        except AttributeError:
            dati = YouTubeTranscriptApi.get_transcript(video_id, languages=LINGUE_SOTTOTITOLI)
            return [d["text"] for d in dati]
    except Exception:
        return None

def trascrivi_audio(url):
    from faster_whisper import WhisperModel
    with tempfile.TemporaryDirectory() as tmp:
        opzioni = OPZIONI_BASE.copy()
        opzioni["format"] = "bestaudio/best"
        opzioni["outtmpl"] = str(Path(tmp) / "audio.%(ext)s")
        
        with yt_dlp.YoutubeDL(opzioni) as ydl:
            ydl.download([url])
        file_audio = next(Path(tmp).glob("audio.*"))

        print("Trascrizione con Whisper... puo' richiedere tempo.")
        modello = WhisperModel(MODELLO_WHISPER, device="cpu", compute_type="int8")
        segmenti, _ = modello.transcribe(str(file_audio), vad_filter=True)
        return [s.text.strip() for s in segmenti]

def in_paragrafi(frasi):
    frasi = [re.sub(r"\s+", " ", f).strip() for f in frasi if f.strip()]
    return [" ".join(frasi[i : i + FRASI_PER_PARAGRAFO]) for i in range(0, len(frasi), FRASI_PER_PARAGRAFO)]

def nome_sicuro(testo):
    return re.sub(r'[\\/:*?"<>|]', "", testo).strip()[:100] or "trascrizione"

def salva_txt(titolo, paragrafi, percorso):
    percorso.write_text(titolo + "\n\n" + "\n\n".join(paragrafi), encoding="utf-8")

def salva_docx(titolo, paragrafi, percorso):
    doc = Document()
    doc.add_heading(titolo, level=1)
    for p in paragrafi:
        doc.add_paragraph(p)
    doc.save(percorso)

def salva_odt(titolo, paragrafi, percorso):
    doc = OpenDocumentText()
    doc.text.addElement(H(outlinelevel=1, text=titolo))
    for p in paragrafi:
        doc.text.addElement(P(text=p))
    doc.save(str(percorso))

def elabora_video(url):
    video_id = estrai_id(url)
    titolo = titolo_video(url)
    print(f"Video trovato: {titolo}")

    frasi = prova_sottotitoli(video_id)
    if frasi:
        print("Sottotitoli trovati.")
    else:
        print("Sottotitoli non disponibili: passo alla trascrizione dell'audio.")
        frasi = trascrivi_audio(url)

    paragrafi = in_paragrafi(frasi)

    CARTELLA_OUTPUT.mkdir(exist_ok=True)
    nome_base = nome_sicuro(titolo)
    base = CARTELLA_OUTPUT / nome_base
    salva_txt(titolo, paragrafi, base.with_suffix(".txt"))
    salva_docx(titolo, paragrafi, base.with_suffix(".docx"))
    salva_odt(titolo, paragrafi, base.with_suffix(".odt"))
    
    testo_completo = titolo + "\n\n" + "\n\n".join(paragrafi)
    return testo_completo, nome_base

def leggi_testo_salvato(nome_file):
    percorso = CARTELLA_OUTPUT / nome_file
    if percorso.exists():
        return percorso.read_text(encoding="utf-8")
    return None

if __name__ == "__main__":
    indirizzo = sys.argv[1] if len(sys.argv) > 1 else input("Incolla l'URL del video: ").strip()
    elabora_video(indirizzo)
