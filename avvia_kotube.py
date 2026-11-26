import os
import sys
import threading
import time
import traceback
import webbrowser

REPO = os.path.dirname(os.path.abspath(__file__))
os.chdir(REPO)

# Con pythonw stdout/stderr sono None: li mando su un log, cosi' eventuali
# errori di yt-dlp o di Flask restano visibili in avvio_log.txt.
if sys.stdout is None or sys.stderr is None:
    try:
        _log = open(os.path.join(REPO, "avvio_log.txt"), "a", encoding="utf-8", buffering=1)
    except Exception:
        _log = None
    if _log is not None:
        if sys.stdout is None:
            sys.stdout = _log
        if sys.stderr is None:
            sys.stderr = _log


def main():
    from KOTUBE import app

    if os.environ.get("KOTUBE_NO_BROWSER") != "1":
        def apri():
            time.sleep(1.5)
            webbrowser.open("http://127.0.0.1:48217/")

        threading.Thread(target=apri, daemon=True).start()

    app.run(host="127.0.0.1", port=48217, debug=False)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        with open(os.path.join(REPO, "avvio_errore.txt"), "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise
