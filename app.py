from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Happy Birthday, Bestie 🎀</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root{
    --bg1:#ffb3ec; --bg2:#b3c7ff;
    --cover1:#ff90d4; --cover2:#ffd166;
    --ink:#2a1f2a;
    --tape:#8fe3ff;
    --ring:#6c8cff;
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{
    margin:0;
    font-family: "Segoe UI", system-ui, -apple-system, Arial, sans-serif;
    background: linear-gradient(135deg,var(--bg1),var(--bg2));
    display:flex; align-items:center; justify-content:center; min-height:100vh;
  }

  /* container & card */
  .stage{perspective:1600px; width:min(1000px,95vw); height:min(92vh,820px)}
  .card{
    position:relative; width:100%; height:100%;
    transform-style:preserve-3d; transition:transform 1s cubic-bezier(.2,.8,.2,1);
  }
  .card.open{ transform: rotateY(-180deg); }

  .side{
    position:absolute; inset:0;
    backface-visibility:hidden; border-radius:18px; overflow:hidden;
    box-shadow:0 18px 50px rgba(0,0,0,.25);
  }

  /* front cover */
  .front{
    color:#fff;
    background: radial-gradient(900px 600px at -10% -20%, #fff8, transparent 60%),
                linear-gradient(135deg,var(--cover1),var(--cover2));
    display:grid; place-items:center;
  }
  .cover-inner{ text-align:center; padding:28px }
  .title{ font-size: clamp(28px, 5.5vw, 56px); margin:0 0 8px; text-shadow:0 6px 24px #0003 }
  .subtitle{ margin:0 0 18px; opacity:.95 }
  .rings{
    display:flex; gap:10px; justify-content:center; margin:16px 0 26px;
  }
  .rings span{
    width:14px; height:14px; border-radius:50%;
    box-shadow:0 0 0 6px #fff2 inset;
    background:conic-gradient(from 0deg, #fff0 0 75%, #fff8 75% 100%);
    outline:4px solid var(--ring);
  }
  .openBtn{
    appearance:none; border:0; cursor:pointer; font-weight:800;
    padding:12px 18px; border-radius:12px; color:#241a21; background:#fff;
    box-shadow:0 12px 24px rgba(255,255,255,.25), inset 0 1px 0 #fff;
    transition:.2s transform;
  }
  .openBtn:active{ transform:translateY(1px) }

  /* inside spread (two pages) */
  .inside{ background:#fff; transform: rotateY(180deg); color:var(--ink); }
  .spread{ display:grid; grid-template-columns:1fr 1fr; height:100% }
  @media (max-width: 860px){ .spread{ grid-template-columns:1fr; } }

  /* left page: wholesome letter */
  .page{
    padding:24px clamp(16px, 3vw, 28px) 28px;
    background:
      linear-gradient(transparent 85%, #fffb 85%),
      repeating-linear-gradient( to bottom, #0000 0 34px, #0000 33px, #0001 34px );
  }
  .page h2{ margin:8px 0 10px; color:#cf2b8f }
  .tape{
    display:inline-block; background:var(--tape); color:#034; font-weight:700;
    padding:6px 10px; border-radius:8px; transform:rotate(-3deg);
    box-shadow:0 4px 10px #0002; margin-bottom:8px;
  }
  .note{
    line-height:1.65; font-size:clamp(14px, 2.1vw, 16px);
    background:#fff8; border:1px dashed #0002; border-radius:12px; padding:14px 16px;
  }

  /* right page: colorful scrapbook */
  .scrap{
    padding:18px; display:flex; flex-wrap:wrap; gap:14px; align-content:flex-start; overflow:auto;
    background:
      radial-gradient(600px 460px at 80% -20%, #ffecfe, transparent 60%),
      radial-gradient(600px 460px at 0% 120%, #e8f7ff, transparent 60%),
      #fff;
  }
  .polaroid{
    --clr: #ff90d4;
    width:180px; background:#fff; border:6px solid var(--clr);
    border-radius:10px; padding:8px 8px 16px;
    box-shadow:0 10px 24px rgba(0,0,0,.12);
    transform: rotate(var(--rot)); transition:.2s transform;
  }
  .polaroid:hover{ transform: rotate(var(--rot)) translateY(-4px); }
  .polaroid img, .polaroid video{ width:100%; height:180px; object-fit:cover; border-radius:6px }
  .label{ text-align:center; margin-top:8px; font-weight:700; font-size:13px; opacity:.8 }

  /* confetti canvas */
  #confetti{ position:fixed; inset:0; pointer-events:none; z-index:50 }

  /* gentle sparkles */
  .sparkles{ position:absolute; inset:0; pointer-events:none; }
  .sparkles::before, .sparkles::after{
    content:"✨"; position:absolute; font-size:22px; animation:float 6s linear infinite; opacity:.6
  }
  .sparkles::after{ animation-delay:2.5s; left:80%; top:20% }
  .sparkles::before{ left:12%; top:70% }
  @keyframes float{ 0%{ transform:translateY(0)} 50%{ transform:translateY(-16px)} 100%{ transform:translateY(0)} }

  /* PAGE TEAR OVERLAY */
  .tear{
    position:fixed; inset:0; z-index:60; display:grid; place-items:stretch;
    pointer-events:none;
  }
  .tear .sheet{
    background: linear-gradient(#fff 0 0) padding-box, repeating-linear-gradient(90deg,#0001 0 14px,#0000 14px 28px) border-box;
    border-bottom:0; border:1px solid #0001;
    height:55vh; width:100%; align-self:start;
    box-shadow:0 40px 70px rgba(0,0,0,.25);
    transform:translateY(0); transition: transform 1.2s cubic-bezier(.2,.8,.2,1);
    position:relative;
  }
  .tear .edge{
    position:absolute; left:0; right:0; bottom:-1px; height:40px;
    /* jagged edge using SVG mask */
    -webkit-mask: url('#rip') 0/100% 100% no-repeat; mask: url('#rip') 0/100% 100% no-repeat;
    background: #fff;
    filter: drop-shadow(0 6px 6px #0002);
  }
  .tear.run .sheet{ transform:translateY(-70vh); } /* slides up like ripping */

  /* accessibility */
  .sr-only{ position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); border:0; }
</style>
</head>
<body>

<canvas id="confetti"></canvas>
<div class="sparkles" aria-hidden="true"></div>

<!-- TEAR OVERLAY (hidden SVG defines the jagged mask) -->
<svg width="0" height="0" aria-hidden="true">
  <defs>
    <svg id="rip" viewBox="0 0 1200 200" preserveAspectRatio="none">
      <path d="M0,0 H1200 V140
               c-40,-20 -80,-20 -120,0
               s-80,20 -120,0
               s-80,-20 -120,0
               s-80,20 -120,0
               s-80,-20 -120,0
               s-80,20 -120,0
               s-80,-20 -120,0
               s-80,20 -120,0
               V0 Z" fill="#000"/>
    </svg>
  </defs>
</svg>
<div class="tear" id="tear" aria-hidden="true">
  <div class="sheet">
    <div class="edge"></div>
  </div>
</div>

<div class="stage">
  <div class="card" id="card">
    <!-- FRONT COVER -->
    <section class="side front">
      <div class="cover-inner">
        <h1 class="title">Happy Birthday, Bestie 🎉</h1>
        <p class="subtitle">From one random online coincidence to almost a year of pure bond — lucky me.</p>
        <div class="rings" aria-hidden="true"><span></span><span></span><span></span></div>
        <button class="openBtn" id="openBtn" aria-controls="inside">Open Card 🎀</button>
      </div>
    </section>

    <!-- INSIDE SPREAD -->
    <section id="inside" class="side inside" role="region" aria-label="Inside of the greeting card">
      <div class="spread">
        <!-- Left page -->
        <div class="page">
          <span class="tape">For my online bestie</span>
          <h2>Dear You,</h2>
          <p class="note">
            Who knew one small moment online would turn into such a solid friendship?
            You’re a proper hustler — hardworking, strong, and full of heart. The way you keep
            showing up for your goals inspires me, yaar.<br><br>
            Today, keep the to-do list aside and soak in all the love. May this year bring you
            new wins, calm mornings, louder laughs, and that extra glow you deserve.
            I’m always cheering for you from my side of the screen. Happy Birthday, bestie.
            Make a big wish — the universe is listening. 💫
          </p>
          <p class="note" style="margin-top:12px">
            P.S. One day we’ll laugh about how this started with a small coincidence — and how it became a comfort zone. 🫶
          </p>
        </div>

        <!-- Right page: scrapbook -->
        <div class="scrap" id="scrap">
          {% for i in range(1,9) %}
            <figure class="polaroid" style="--rot: {{ (-6 + (i%5)*3) }}deg; --clr: {{ colors[(i-1) % colors|length] }}">
              <img src="/media/{{ i }}.jpg" alt="Photo {{ i }}">
              <figcaption class="label">Memory {{ i }}</figcaption>
            </figure>
          {% endfor %}
          {% for v in range(1,5) %}
            <figure class="polaroid" style="--rot: {{ (4 - (v%5)*2) }}deg; --clr: {{ colors[(v+2) % colors|length] }}">
              <video src="/media/{{ v }}.mp4" playsinline controls muted></video>
              <figcaption class="label">Clip {{ v }}</figcaption>
            </figure>
          {% endfor %}
        </div>
      </div>
    </section>
  </div>
</div>

<audio id="bgm" src="/media/song.mp3" preload="none"></audio>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
  const openBtn = document.getElementById('openBtn');
  const card = document.getElementById('card');
  const tear = document.getElementById('tear');
  const bgm = document.getElementById('bgm');

  openBtn.addEventListener('click', async () => {
    // run the tear animation first
    tear.classList.add('run');
    // a tiny delay so the tear starts moving, then flip card
    setTimeout(()=> card.classList.add('open'), 180);
    // confetti celebration
    confettiBurst();
    // try music if present (ignore failures)
    try { await bgm.play(); } catch(e) {}

    // stop and hide the tear overlay after it slides away
    setTimeout(()=> { tear.style.display='none'; }, 1600);
  });

  function confettiBurst(){
    const duration = 1600, end = Date.now() + duration;
    (function frame(){
      confetti({ particleCount: 8, angle: 60, spread: 60, origin:{x:0} });
      confetti({ particleCount: 8, angle: 120, spread: 60, origin:{x:1} });
      if(Date.now() < end) requestAnimationFrame(frame);
    }());
  }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    # bright palette for polaroid borders
    colors = ["#ff90d4", "#ffd166", "#8fe3ff", "#b0ffb4", "#b3c7ff", "#ff9ab0", "#a5f0c5", "#d3b8ff"]
    return render_template_string(HTML, colors=colors)

@app.route("/media/<path:filename>")
def media(filename):
    # serve files from the same directory as app.py
    return send_from_directory(os.path.dirname(__file__), filename)

if __name__ == "__main__":
    app.run(debug=True)
