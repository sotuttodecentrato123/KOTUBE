from flask import Flask, render_template_string, request, send_file, redirect
import trascrizione as t
import os
import glob

app = Flask(__name__)
os.makedirs("output", exist_ok=True)

PAGINA = """
<!doctype html>
<html lang="{{ lang }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>KOTUBE - Nuovo Design Chiaro</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #f3f4f6;
            --container-bg: #ffffff;
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --brand-red: #e50914;
            --brand-red-hover: #b80710;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 20px 40px -10px rgba(0, 0, 0, 0.08), 0 10px 20px -5px rgba(0, 0, 0, 0.04);
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .top-bar {
            position: absolute;
            top: 24px;
            left: 24px;
            right: 24px;
            display: flex;
            justify-content: space-between;
        }
        .btn-nav {
            color: var(--text-main);
            text-decoration: none;
            background: var(--container-bg);
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        .btn-nav:hover {
            background: var(--brand-red);
            color: white;
            border-color: var(--brand-red);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }
        .lang-switch a {
            color: var(--text-main);
            text-decoration: none;
            background: var(--container-bg);
            padding: 10px 16px;
            border-radius: 8px;
            margin-left: 8px;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow-sm);
            transition: all 0.2s ease;
        }
        .lang-switch a:hover {
            background: var(--brand-red);
            color: white;
            border-color: var(--brand-red);
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }
        .container {
            background: var(--container-bg);
            padding: 48px;
            border-radius: 24px;
            box-shadow: var(--shadow-lg);
            text-align: center;
            max-width: 600px;
            width: 100%;
            position: relative;
            animation: fadeIn 0.6s ease-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Logo originale, sistemato con angoli e ombra */
        .logo {
            max-width: 85%;
            height: auto;
            margin-bottom: 32px;
            border-radius: 16px;
            box-shadow: var(--shadow-sm);
        }

        h1 {
            margin-top: 0;
            font-size: 24px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 32px;
            letter-spacing: -0.5px;
        }

        textarea {
            width: 100%;
            height: 90px;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            background: #f9fafb;
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
            font-size: 16px;
            box-sizing: border-box;
            resize: none;
            margin-bottom: 24px;
            transition: all 0.2s ease;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
        }
        textarea:focus {
            outline: none;
            border-color: var(--brand-red);
            background: #ffffff;
            box-shadow: 0 0 0 4px rgba(229, 9, 20, 0.1);
        }

        button[type="submit"] {
            background: var(--brand-red);
            color: white;
            border: none;
            padding: 18px 30px;
            font-size: 16px;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 100%;
            box-shadow: 0 4px 14px 0 rgba(229, 9, 20, 0.3);
        }
        button[type="submit"]:hover {
            background: var(--brand-red-hover);
            transform: translateY(-2px);
            box-shadow: 0 6px 20px 0 rgba(229, 9, 20, 0.4);
        }

        #loading {
            display: none;
            margin-top: 32px;
            font-size: 16px;
            color: var(--brand-red);
            font-weight: 500;
            min-height: 50px;
        }
        .spinner {
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--brand-red);
            border-radius: 50%;
            width: 32px;
            height: 32px;
            animation: spin 1s linear infinite;
            margin: 0 auto 16px auto;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .fade-text { animation: textFade 0.5s ease-in-out; }
        @keyframes textFade { from { opacity: 0; } to { opacity: 1; } }

        .risultato-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 40px;
            margin-bottom: 16px;
            border-top: 1px solid var(--border-color);
            padding-top: 24px;
        }
        .risultato-header h3 { margin: 0; font-size: 18px; color: var(--text-main); }

        .btn-copia {
            background: #ffffff;
            color: var(--text-main);
            border: 1px solid var(--border-color);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
        }
        .btn-copia:hover {
            background: var(--bg-color);
            border-color: var(--brand-red);
            color: var(--brand-red);
            box-shadow: var(--shadow-md);
        }
        .btn-copia.copiato {
            background: #dcfce7;
            color: #166534;
            border-color: #166534;
            box-shadow: none;
        }

        .risultato {
            text-align: left;
            background: #f9fafb;
            padding: 28px;
            border-radius: 16px;
            border: 1px solid var(--border-color);
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            font-size: 15px;
            line-height: 1.7;
            color: var(--text-main);
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
        }

        .download-buttons {
            display: flex;
            gap: 12px;
            margin-top: 24px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .download-buttons a {
            background: #ffffff;
            color: var(--text-main);
            text-decoration: none;
            padding: 14px 20px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            font-size: 15px;
            font-weight: 600;
            transition: all 0.2s ease;
            flex: 1;
            min-width: 130px;
            box-shadow: var(--shadow-sm);
        }
        .download-buttons a:hover {
            background: var(--bg-color);
            border-color: var(--brand-red);
            color: var(--brand-red);
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }
        .errore {
            color: var(--brand-red);
            margin-top: 20px;
            font-weight: 500;
            font-size: 15px;
            background: #fee2e2;
            padding: 12px;
            border-radius: 8px;
        }
        .btn-svuota {
            background: transparent;
            color: var(--text-muted);
            border: 1px solid var(--border-color);
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin-top: 40px;
            transition: all 0.2s ease;
        }
        .btn-svuota:hover {
            background: #fee2e2;
            color: var(--brand-red);
            border-color: var(--brand-red);
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <div><a href="/cronologia" class="btn-nav">🕒 Cronologia</a></div>
        <div class="lang-switch"><a href="/?lang=it">IT</a><a href="/?lang=en">EN</a><a href="/?lang=ja">JA</a></div>
    </div>
    <div class="container">
        <img src="/static/logo_{{ lang }}.png" alt="Logo" class="logo">
        <h1>{{ titolo }}</h1>

        <form method="POST" id="form_trascrizione" onsubmit="mostraCaricamento()">
            <textarea name="url_video" id="url_input" placeholder="{{ placeholder }}">{{ url_inserito }}</textarea>
            <button type="submit" id="btn_genera">{{ bottone }}</button>
        </form>

        <div id="loading">
            <div class="spinner"></div>
            <span id="messaggio_caricamento" class="fade-text">🔍 Analisi del link in corso...</span>
        </div>

        {% if errore %}<div class="errore">{{ errore }}</div>{% endif %}
        {% if testo %}
            <div class="risultato-header">
                <h3>Trascrizione completata</h3>
                <button class="btn-copia" id="btnCopia" onclick="copiaTesto()">📋 Copia Testo</button>
            </div>
            <div class="risultato" id="testoRisultato">{{ testo }}</div>
            {% if nome_file %}
            <div class="download-buttons">
                <a href="/scarica/{{ nome_file }}.txt">📄 Scarica .TXT</a>
                <a href="/scarica/{{ nome_file }}.docx">📝 Scarica .DOCX</a>
                <a href="/scarica/{{ nome_file }}.odt">📋 Scarica .ODT</a>
            </div>
            {% endif %}
        {% endif %}
        <a href="/svuota" class="btn-svuota" onclick="return confirm('Sei sicuro di voler cancellare tutti i file vecchi?')">🗑️ Svuota cartella Output</a>
    </div>

    <script>
        var messaggi = [
            "🔍 Analisi del link in corso...",
            "⬇️ Scaricando il video da YouTube...",
            "🎧 Estrazione dell'audio in corso...",
            "✍️ Trascrizione del parlato (potrebbe volerci un po')...",
            "📝 Creazione dei file Word e TXT...",
            "🚀 Quasi pronto, ultimi ritocchi..."
        ];

        var intervallo;
        var indice_messaggio = 0;

        function mostraCaricamento() {
            var url = document.getElementById("url_input").value;
            if(url.trim() !== "") {
                document.getElementById("btn_genera").style.display = "none";
                document.getElementById("loading").style.display = "block";

                var spanMessaggio = document.getElementById("messaggio_caricamento");

                intervallo = setInterval(function() {
                    indice_messaggio++;
                    if (indice_messaggio < messaggi.length) {
                        spanMessaggio.classList.remove("fade-text");
                        void spanMessaggio.offsetWidth; 
                        spanMessaggio.classList.add("fade-text");
                        spanMessaggio.innerText = messaggi[indice_messaggio];
                    }
                }, 4000);
            }
        }

        function copiaTesto() {
            var testo = document.getElementById("testoRisultato").innerText;
            var btn = document.getElementById("btnCopia");
            navigator.clipboard.writeText(testo).then(function() {
                btn.innerText = "✅ Copiato!";
                btn.classList.add("copiato");
                setTimeout(function() { btn.innerText = "📋 Copia Testo"; btn.classList.remove("copiato"); }, 2000);
            }).catch(function(err) { alert("Ops, non sono riuscito a copiare il testo: " + err); });
        }
    </script>
</body>
</html>
"""

PAGINA_CRONOLOGIA = """
<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>KOTUBE - Cronologia</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #f3f4f6; --container-bg: #ffffff; --text-main: #1f2937; --text-muted: #6b7280; --brand-red: #e50914; --brand-red-hover: #b80710; --border-color: #e5e7eb; --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1); --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        body { background-color: var(--bg-color); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 40px 20px; box-sizing: border-box; }
        .container { background: var(--container-bg); padding: 48px; border-radius: 24px; box-shadow: var(--shadow-lg); max-width: 600px; width: 100%; animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        h1 { margin-top: 0; font-size: 24px; font-weight: 600; text-align: center; margin-bottom: 32px; }
        .btn-back { display: inline-block; color: var(--text-main); text-decoration: none; background: var(--container-bg); padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; border: 1px solid var(--border-color); transition: 0.2s; margin-bottom: 24px; box-shadow: var(--shadow-md); }
        .btn-back:hover { background: var(--brand-red); color: white; border-color: var(--brand-red); transform: translateY(-1px); }
        .lista-file { list-style: none; padding: 0; margin: 0; }
        .lista-file li { padding: 20px 16px; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; transition: background 0.2s; border-radius: 8px; }
        .lista-file li:hover { background: #f9fafb; }
        .lista-file li:last-child { border-bottom: none; }
        .lista-file a { color: var(--text-main); text-decoration: none; font-weight: 500; font-size: 16px; }
        .lista-file a:hover { color: var(--brand-red); }
        .empty-msg { text-align: center; color: var(--text-muted); font-size: 16px; padding: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="btn-back">← Torna alla Home</a>
        <h1>🕒 Cronologia Trascrizioni</h1>
        {% if file_lista %}
            <ul class="lista-file">
            {% for f in file_lista %}
                <li>
                    <a href="/leggi/{{ f }}">{{ f.replace('.txt', '') }}</a>
                    <span style="font-size:13px; color:#9ca3af; background:#e5e7eb; padding:4px 8px; border-radius:6px;">.txt</span>
                </li>
            {% endfor %}
            </ul>
        {% else %}
            <p class="empty-msg">Nessuna trascrizione trovata. Vai alla home e generane una!</p>
        {% endif %}
    </div>
</body>
</html>
"""

PAGINA_LETTURA = """
<!doctype html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>KOTUBE - Lettura</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --bg-color: #f3f4f6; --container-bg: #ffffff; --text-main: #1f2937; --text-muted: #6b7280; --brand-red: #e50914; --border-color: #e5e7eb; --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        body { background-color: var(--bg-color); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 40px 20px; box-sizing: border-box; }
        .container { background: var(--container-bg); padding: 48px; border-radius: 24px; box-shadow: var(--shadow-lg); max-width: 800px; width: 100%; animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .btn-back { display: inline-block; color: var(--text-main); text-decoration: none; background: var(--bg-color); padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; border: 1px solid var(--border-color); transition: 0.2s; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .btn-back:hover { background: var(--brand-red); color: white; border-color: var(--brand-red); transform: translateY(-1px); }
        h1 { margin-top: 0; font-size: 26px; font-weight: 600; margin-bottom: 24px; letter-spacing: -0.5px; }
        .contenuto { white-space: pre-wrap; line-height: 1.8; font-size: 16px; color: var(--text-main); }
    </style>
</head>
<body>
    <div class="container">
        <a href="/cronologia" class="btn-back">← Torna alla Cronologia</a>
        <h1>{{ titolo_file }}</h1>
        <div class="contenuto">{{ contenuto }}</div>
    </div>
</body>
</html>
"""

TRADUZIONI = {
    "it": {"titolo": "Incolla il link di YouTube e premi Genera", "placeholder": "https://www.youtube.com/watch?v=...",
           "bottone": "Genera Testo"},
    "en": {"titolo": "Paste the YouTube link and click Generate", "placeholder": "https://www.youtube.com/watch?v=...",
           "bottone": "Generate Text"},
    "ja": {"titolo": "YouTubeのリンクを貼り付けて「生成」を押してください",
           "placeholder": "https://www.youtube.com/watch?v=...", "bottone": "テキストを生成"}
}


@app.route("/", methods=["GET", "POST"])
def home():
    lang = request.args.get("lang", "it")
    if lang not in TRADUZIONI:
        lang = "it"
    testo_finale = ""
    errore = ""
    url_inserito = ""
    nome_file = ""

    if request.method == "POST":
        url_video = request.form.get("url_video", "")
        url_inserito = url_video
        if url_video:
            try:
                testo_finale, nome_file = t.elabora_video(url_video)
            except Exception as e:
                errore = f"Errore durante l'elaborazione: {str(e)}"
        else:
            errore = "Inserisci un link valido."

    return render_template_string(
        PAGINA, lang=lang, titolo=TRADUZIONI[lang]["titolo"],
        placeholder=TRADUZIONI[lang]["placeholder"], bottone=TRADUZIONI[lang]["bottone"],
        testo=testo_finale, errore=errore, url_inserito=url_inserito, nome_file=nome_file
    )


@app.route("/scarica/<nome_file>")
def scarica_file(nome_file):
    percorso = os.path.join("output", nome_file)
    if os.path.exists(percorso):
        return send_file(percorso, as_attachment=True, mimetype='application/octet-stream')
    else:
        return "File non trovato.", 404


@app.route("/svuota")
def svuota_cartella():
    file_da_cancellare = glob.glob("output/*")
    for f in file_da_cancellare:
        try:
            os.remove(f)
        except Exception:
            pass
    return redirect("/")


@app.route("/cronologia")
def cronologia():
    files = glob.glob("output/*.txt")
    nomi_file = [os.path.basename(f) for f in files]
    nomi_file.sort(key=lambda x: os.path.getmtime(os.path.join("output", x)), reverse=True)
    return render_template_string(PAGINA_CRONOLOGIA, file_lista=nomi_file)


@app.route("/leggi/<nome_file>")
def leggi_file(nome_file):
    contenuto = t.leggi_testo_salvato(nome_file)
    if contenuto:
        titolo = nome_file.replace('.txt', '')
        return render_template_string(PAGINA_LETTURA, titolo_file=titolo, contenuto=contenuto)
    else:
        return "File non trovato.", 404


if __name__ == "__main__":
    print("Avvio di KOTUBE su http://127.0.0.1:48217")
    app.run(debug=True, port=48217)