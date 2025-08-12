from flask import Flask, send_from_directory, render_template
import os, urllib.parse

app = Flask(__name__)

# inline helper to make a small placeholder SVG (if any image is missing)
def placeholder_svg(text: str) -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='400' height='300'>"
        f"<rect width='100%' height='100%' fill='%23e9e9ef'/>"
        f"<text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' "
        f"font-family='Segoe UI' font-size='20' fill='%23999'>{text}</text>"
        f"</svg>"
    )

def enc_svg(label: str) -> str:
    return urllib.parse.quote(placeholder_svg(label))

@app.route("/")
def home():
    # bright border colors for the scrapbook polaroids
    colors = ["#ff90d4", "#ffd166", "#8fe3ff", "#b0ffb4", "#b3c7ff", "#ff9ab0", "#a5f0c5", "#d3b8ff"]
    return render_template("template.html",
                           colors=colors,
                           placeholder_svg=enc_svg,
                           str=str)

# serve all media files from the same folder as app.py
@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
