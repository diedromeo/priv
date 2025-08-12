from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Happy Birthday Bestie 🎀</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #ffb3ec, #b3c7ff);
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
.card-container {
    perspective: 1500px;
}
.card {
    width: 90vw;
    max-width: 900px;
    height: 90vh;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 1s;
}
.card.open {
    transform: rotateY(-180deg);
}
.side {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    overflow-y: auto;
}
.front {
    background: linear-gradient(135deg, #ff90d4, #ffd166);
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.front h1 {
    font-size: 2rem;
    text-align: center;
}
.front button {
    padding: 10px 20px;
    background: white;
    color: #ff60b8;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 15px;
}
.back {
    background: #fff;
    color: #333;
    transform: rotateY(180deg);
    padding: 20px;
}
.message {
    font-size: 1rem;
    margin-bottom: 20px;
}
.scrapbook {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
}
.scrapbook .item {
    background: white;
    padding: 5px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transform: rotate(calc(-5deg + 10deg * var(--i)));
    border: 5px solid var(--color);
}
.scrapbook img, .scrapbook video {
    display: block;
    width: 180px;
    height: 180px;
    object-fit: cover;
    border-radius: 4px;
}
</style>
</head>
<body>

<div class="card-container">
    <div class="card" id="card">
        <div class="side front">
            <h1>Happy Birthday Bestie 🎉<br>Click to open your surprise 🎀</h1>
            <button onclick="openCard()">Open Card</button>
        </div>
        <div class="side back">
            <h2>Dear Bestie 💌</h2>
            <p class="message">
                Who knew a cute coincidence online would turn into almost a year of pure madness & friendship?  
                You’re a real hustler — hardworking, strong, and full of dreams.  
                From random memes to heartfelt talks, every chat with you is a highlight.  
                Keep shining, keep hustling, and remember — I’m always rooting for you from my side of the screen.  
                Here’s to more laughs, late-night talks, and crazy moments! 💫
            </p>
            <div class="scrapbook">
                {% for idx in range(1,9) %}
                <div class="item" style="--i:{{ loop.index }}; --color: {{ colors[loop.index0 % colors|length] }}">
                    <img src="/media/{{ idx }}.jpg" alt="Photo {{ idx }}">
                </div>
                {% endfor %}
                {% for idx in range(1,5) %}
                <div class="item" style="--i:{{ loop.index }}; --color: {{ colors[(loop.index0+3) % colors|length] }}">
                    <video src="/media/{{ idx }}.mp4" controls muted></video>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
function openCard(){
    document.getElementById("card").classList.add("open");
    launchConfetti();
}
function launchConfetti(){
    const duration = 2 * 1000;
    const end = Date.now() + duration;
    (function frame() {
        confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0 }
        });
        confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1 }
        });
        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    colors = ["#ff90d4", "#ffd166", "#8fe3ff", "#b0ffb4", "#ffb3ec", "#b3c7ff"]
    return render_template_string(HTML, colors=colors)

@app.route("/media/<path:filename>")
def media(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

if __name__ == "__main__":
    app.run(debug=True)
