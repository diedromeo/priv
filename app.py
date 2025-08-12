from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Birthday Card 🎀</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {
    background: linear-gradient(135deg, #ffb3ec, #b3c7ff);
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    height: 100vh;
    justify-content: center;
    align-items: center;
}
.card-container {
    perspective: 1500px;
}
.card {
    width: 400px;
    height: 500px;
    position: relative;
    transform-style: preserve-3d;
    transition: transform 1s ease-in-out;
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
}
.front {
    background: #ff90d4;
    color: white;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.front h1 {
    font-size: 2rem;
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
    background: white;
    color: #333;
    transform: rotateY(180deg);
    padding: 20px;
    overflow-y: auto;
    border-radius: 15px;
}
.song {
    margin: 10px 0;
}
.gallery {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 10px;
}
.gallery img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 10px;
}
</style>
</head>
<body>

<div class="card-container">
    <div class="card" id="card">
        <div class="side front">
            <h1>Happy Birthday Bestie 🎉</h1>
            <p>Click to open your surprise 🎀</p>
            <button onclick="openCard()">Open Card</button>
        </div>
        <div class="side back">
            <h2>Dear Bestie,</h2>
            <p>
            Who knew a random coincidence online would turn into almost a year of pure friendship?  
            You’re one of the strongest, most hardworking people I know — a true hustler.  
            From late-night chats to silly memes, every moment with you has been special.  
            Keep shining and chasing your dreams, I’m always rooting for you! 💫
            </p>
            <div class="song">
                <iframe width="100%" height="100" src="https://mobcup.com.co/aage-rahiyo-na-peeche-rahiyo-sang-rahiyo-ringtone-download-rw4t2ga" frameborder="0"></iframe>
            </div>
            <div class="gallery">
                <img src="https://via.placeholder.com/100?text=Memory+1">
                <img src="https://via.placeholder.com/100?text=Memory+2">
                <img src="https://via.placeholder.com/100?text=Memory+3">
            </div>
        </div>
    </div>
</div>

<script>
function openCard(){
    document.getElementById("card").classList.add("open");
    launchConfetti();
}

function launchConfetti(){
    const duration = 2 * 1000;
    const end = Date.now() + duration;

    (function frame() {
        const colors = ['#ff90d4', '#ffd166', '#8fe3ff', '#b0ffb4'];
        confetti({
            particleCount: 5,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: colors
        });
        confetti({
            particleCount: 5,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: colors
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
}
</script>
<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
