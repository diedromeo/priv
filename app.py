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
<meta name="theme-color" content="#ff90d4">
<style>
  :root{
    --bg1:#ffb3ec; --bg2:#b3c7ff;
    --cover1:#ff90d4; --cover2:#ffd166;
    --ink:#2a1f2a;
    --tape:#8fe3ff;
    --ring:#6c8cff;
    --accent:#ff90d4;
    --accent2:#ffd166;
  }
  *{box-sizing:border-box}
  html,body{height:100%}
  body{
    margin:0;
    font-family: "Segoe UI", system-ui, -apple-system, Arial, sans-serif;
    background: linear-gradient(135deg,var(--bg1),var(--bg2));
    display:flex; align-items:center; justify-content:center; min-height:100vh;
    color:var(--ink);
  }

  /* container & card */
  .stage{perspective:1600px; width:min(1000px,95vw); height:min(92vh,840px); position:relative}
  .card{
    position:relative; width:100%; height:100%;
    transform-style:preserve-3d; transition:transform 1s cubic-bezier(.2,.8,.2,1);
    border-radius:18px; box-shadow:0 18px 50px rgba(0,0,0,.25); overflow:hidden;
  }
  .card.open{ transform: rotateY(-180deg); }

  .side{
    position:absolute; inset:0;
    backface-visibility:hidden; overflow:hidden;
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
  .rings{ display:flex; gap:10px; justify-content:center; margin:16px 0 26px; }
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
  @media (max-width: 900px){ .spread{ grid-template-columns:1fr; } }

  /* left page: wholesome letter + controls */
  .page{
    padding:24px clamp(16px, 3vw, 28px) 28px;
    background:
      linear-gradient(transparent 85%, #fffb 85%),
      repeating-linear-gradient( to bottom, #0000 0 34px, #0000 33px, #0001 34px );
    overflow:auto;
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
  .controls{ display:flex; gap:10px; flex-wrap:wrap; margin:12px 0 8px }
  .btn{
    appearance:none; border:1px solid #0002; background:#fff; color:#222; border-radius:999px;
    padding:8px 12px; font-weight:700; cursor:pointer;
    box-shadow:0 4px 10px #0001; transition:.2s transform, .2s box-shadow;
  }
  .btn:active{ transform:translateY(1px) }
  .btn.play{ background:linear-gradient(135deg,var(--accent),var(--accent2)); color:#2a1f2a; border:0 }

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
    transform: rotate(var(--rot)); transition:.2s transform, .2s box-shadow;
    will-change: transform;
  }
  .polaroid:hover{ transform: rotate(var(--rot)) translateY(-4px); box-shadow:0 14px 28px rgba(0,0,0,.16) }
  .polaroid img, .polaroid video{ width:100%; height:180px; object-fit:cover; border-radius:6px }
  .label{ text-align:center; margin-top:8px; font-weight:700; font-size:13px; opacity:.8 }

  /* candles mini */
  .candles{
    margin-top:16px; padding:14px; border:1px dashed #0002; border-radius:12px; background:#fff8;
  }
  .meter{ height:8px; background:#0001; border-radius:999px; overflow:hidden; margin:6px 0 6px }
  .meter .bar{ height:100%; width:0%; background:linear-gradient(90deg,#ff9ad0,#ffd166) }
  .cake{
    width:220px; margin:8px auto 6px; display:block;
  }
  .flame{ transform-origin:center; animation: flicker .15s infinite alternate; }
  @keyframes flicker{ from{transform:scale(1) translateY(0)} to{transform:scale(.92) translateY(1px)} }
  .flame.out{ opacity:0; filter: blur(1px); animation:none; transition: opacity .3s ease }
  .smoke{ opacity:0; transition:opacity .5s ease }
  .smoke.show{ opacity:1; animation: smokeUp 1.2s ease forwards }
  @keyframes smokeUp{ 0%{ transform:translateY(0); opacity:.9 } 90%{ transform:translateY(-40px); opacity:0 } 100%{ opacity:0 } }

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
    position:fixed; inset:0; z-index:60; display:grid; place-items:stretch; pointer-events:none;
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
    -webkit-mask: url('#rip') 0/100% 100% no-repeat; mask: url('#rip') 0/100% 100% no-repeat;
    background: #fff; filter: drop-shadow(0 6px 6px #0002);
  }
  .tear.run .sheet{ transform:translateY(-70vh); }

  /* responsive tweaks */
  @media (max-width:520px){
    .polaroid{ width:44vw } .polaroid img,.polaroid video{ height:36vw }
  }

  /* motion respect */
  @media (prefers-reduced-motion: reduce){
    .card{ transition:none }
    .flame,.sparkles::before,.sparkles::after{ animation:none }
  }

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
    <section class="side front" aria-label="Card cover">
      <div class="cover-inner">
        <h1 class="title">Happy Birthday, Bestie 🎉</h1>
        <p class="subtitle">From one random online coincidence to almost a year of solid bond — lucky me.</p>
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
            Who knew one tiny moment online would turn into this much comfort?  
            You’re a proper hustler — hardworking, strong, and full of heart.  
            The way you show up for your goals inspires me, yaar.  
            Today, keep the to-do aside and soak in the love.  
            May this year bring new wins, calmer mornings, louder laughs, and that extra glow you deserve.  
            I’m always cheering for you from my side of the screen.  
            Happy Birthday, bestie. Make a big wish — the universe is listening. 💫
          </p>
          <p class="note" style="margin-top:12px">
            P.S. One day we’ll laugh about how it started with a small coincidence — and became a whole safe zone. 🫶
          </p>

          <div class="controls">
            <button class="btn play" id="musicBtn">Play music 🎶</button>
            <button class="btn" id="relightBtn" style="display:none">Relight candles 🔥</button>
            <button class="btn" id="manualBlowBtn">Blow out now ✨</button>
            <button class="btn" id="calibrateBtn" title="Re-detect your room's quiet level">Recalibrate 🎛️</button>
          </div>

          <!-- Candles mini with mic -->
          <div class="candles" aria-live="polite">
            <svg class="cake" viewBox="0 0 520 360" role="img" aria-label="Birthday cake with five candles">
              <defs>
                <linearGradient id="cakeBody" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#b6bdfc"/><stop offset="100%" stop-color="#6c8cff"/>
                </linearGradient>
                <linearGradient id="wax" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#fff6a6"/><stop offset="100%" stop-color="#ffe37b"/>
                </linearGradient>
                <radialGradient id="flameGrad" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#fffbd1"/><stop offset="60%" stop-color="#ffd166"/><stop offset="100%" stop-color="#ff7b00"/>
                </radialGradient>
                <radialGradient id="smokeGrad" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#ffffffaa"/><stop offset="100%" stop-color="#ffffff00"/>
                </radialGradient>
              </defs>
              <ellipse cx="260" cy="320" rx="180" ry="26" fill="#00000010"/>
              <rect x="110" y="150" width="300" height="120" rx="18" fill="url(#cakeBody)" />
              <g id="candles">
                <g transform="translate(140,120)"><rect width="16" height="60" rx="8" fill="url(#wax)"/><circle class="smoke" r="8" cx="8" cy="-16" fill="url(#smokeGrad)"/><ellipse class="flame" cx="8" cy="-8" rx="7" ry="12" fill="url(#flameGrad)"/></g>
                <g transform="translate(200,120)"><rect width="16" height="60" rx="8" fill="url(#wax)"/><circle class="smoke" r="8" cx="8" cy="-16" fill="url(#smokeGrad)"/><ellipse class="flame" cx="8" cy="-8" rx="7" ry="12" fill="url(#flameGrad)"/></g>
                <g transform="translate(260,120)"><rect width="16" height="60" rx="8" fill="url(#wax)"/><circle class="smoke" r="8" cx="8" cy="-16" fill="url(#smokeGrad)"/><ellipse class="flame" cx="8" cy="-8" rx="7" ry="12" fill="url(#flameGrad)"/></g>
                <g transform="translate(320,120)"><rect width="16" height="60" rx="8" fill="url(#wax)"/><circle class="smoke" r="8" cx="8" cy="-16" fill="url(#smokeGrad)"/><ellipse class="flame" cx="8" cy="-8" rx="7" ry="12" fill="url(#flameGrad)"/></g>
                <g transform="translate(380,120)"><rect width="16" height="60" rx="8" fill="url(#wax)"/><circle class="smoke" r="8" cx="8" cy="-16" fill="url(#smokeGrad)"/><ellipse class="flame" cx="8" cy="-8" rx="7" ry="12" fill="url(#flameGrad)"/></g>
              </g>
            </svg>
            <div class="meter" aria-hidden="true"><div id="meterBar" class="bar"></div></div>
            <div id="micStatus">Tip: click “Play music” to allow audio, then “Blow out now” or enable mic in your browser.</div>
          </div>
        </div>

        <!-- Right page: scrapbook -->
        <div class="scrap" id="scrap">
          {% for i in range(1,9) %}
            <figure class="polaroid" style="--rot: {{ (-6 + (i%5)*3) }}deg; --clr: {{ colors[(i-1) % colors|length] }}">
              <img loading="lazy" src="/media/{{ i }}.jpg" alt="Photo {{ i }}"
                   onerror="this.onerror=null;this.src='data:image/svg+xml;utf8,{{ placeholder_svg('Photo%20'+str(i)) }}'">
              <figcaption class="label">Memory {{ i }}</figcaption>
            </figure>
          {% endfor %}
          {% for v in range(1,5) %}
            <figure class="polaroid" style="--rot: {{ (4 - (v%5)*2) }}deg; --clr: {{ colors[(v+2) % colors|length] }}">
              <video preload="metadata" playsinline controls muted
                     onmouseenter="this.play()" onmouseleave="this.pause()"
                     onloadeddata="this.volume=0.6">
                <source src="/media/{{ v }}.mp4" type="video/mp4">
              </video>
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
  const musicBtn = document.getElementById('musicBtn');

  // Music controls
  let musicOn = false;
  async function toggleMusic(forcePlay=false){
    try{
      if(forcePlay || !musicOn){
        await bgm.play();
        musicOn = true; musicBtn.textContent = "Pause music ⏸️";
      } else {
        bgm.pause(); musicOn = false; musicBtn.textContent = "Play music 🎶";
      }
    }catch(e){ /* ignore if song.mp3 not present or blocked */ }
  }
  musicBtn.addEventListener('click', ()=>toggleMusic());

  openBtn.addEventListener('click', async () => {
    // page tear then flip
    tear.classList.add('run');
    setTimeout(()=> card.classList.add('open'), 180);
    confettiBurst();
    // try to start music softly
    bgm.volume = 0.5; toggleMusic(true);
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

  /* ======= Microphone + blow detection (optional) ======= */
  let audioCtx, analyser, micStream, rafId, baseline = 0.02, threshold = 0.12, listening=false, blown=false;
  const meterBar = document.getElementById('meterBar');
  const micStatus = document.getElementById('micStatus');
  const relightBtn = document.getElementById('relightBtn');
  const manualBlowBtn = document.getElementById('manualBlowBtn');
  const calibrateBtn = document.getElementById('calibrateBtn');

  manualBlowBtn.addEventListener('click', extinguishCandles);
  relightBtn.addEventListener('click', relightCandles);
  calibrateBtn.addEventListener('click', calibrateNoise);

  // Enable mic on first interaction (music click or card open suffices for gesture)
  async function enableMic(){
    try{
      if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
        micStatus.textContent = "Mic not supported here. Use the button to blow out.";
        return;
      }
      if(!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      await audioCtx.resume();
      micStream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation:true, noiseSuppression:true }, video:false });
      const source = audioCtx.createMediaStreamSource(micStream);
      analyser = audioCtx.createAnalyser(); analyser.fftSize = 1024; source.connect(analyser);
      listening = true; blown = false; relightBtn.style.display='none';
      micStatus.textContent = "Listening… blow towards the mic!";
      startLoop(); calibrateNoise();
    }catch(err){
      micStatus.textContent = "Mic blocked/unavailable. Use the button to blow out.";
    }
  }

  // try to enable on open or music press
  openBtn.addEventListener('click', enableMic, {once:true});
  musicBtn.addEventListener('click', enableMic, {once:true});

  function calibrateNoise(){
    if(!analyser){ micStatus.textContent = "Enable mic first to calibrate."; return; }
    micStatus.textContent = "Calibrating room noise…";
    const data = new Uint8Array(analyser.fftSize);
    let samples = 0, sum = 0; const t0 = performance.now();
    (function step(){
      analyser.getByteTimeDomainData(data);
      sum += computeRMS(data); samples++;
      if(performance.now() - t0 < 1000){ requestAnimationFrame(step); }
      else{
        baseline = Math.max(0.01, (sum / samples));
        threshold = Math.max(baseline * 2.6, 0.12);
        micStatus.textContent = `Calibrated ✓ (baseline ~ ${baseline.toFixed(2)}, blow > ${threshold.toFixed(2)})`;
      }
    })();
  }

  function startLoop(){
    cancelAnimationFrame(rafId);
    const data = new Uint8Array(analyser.fftSize);
    let overFrames = 0;
    (function loop(){
      analyser.getByteTimeDomainData(data);
      const vol = computeRMS(data);
      const pct = Math.min(100, Math.round(vol * 200));
      meterBar.style.width = pct + "%";
      if(listening && !blown){
        overFrames = vol > threshold ? overFrames+1 : Math.max(0, overFrames-1);
        if(overFrames > 6) extinguishCandles();
      }
      rafId = requestAnimationFrame(loop);
    })();
  }
  function computeRMS(buf){
    let sumSq = 0; for(let i=0;i<buf.length;i++){ const v = (buf[i] - 128)/128; sumSq += v*v; }
    return Math.sqrt(sumSq / buf.length);
  }

  const flames = Array.from(document.querySelectorAll('.flame'));
  const smokes = Array.from(document.querySelectorAll('.smoke'));
  function extinguishCandles(){
    blown = true; listening = false;
    flames.forEach(f => f.classList.add('out'));
    smokes.forEach((s, i) => setTimeout(()=>{ s.classList.add('show'); setTimeout(()=>s.classList.remove('show'), 1200); }, 60*i));
    confettiBurst();
    micStatus.textContent = "Candles out! Make a wish 🎉";
    relightBtn.style.display='inline-block';
  }
  function relightCandles(){
    blown = false; listening = true;
    flames.forEach(f => f.classList.remove('out'));
    micStatus.textContent = "Relit 🔥 — blow again!";
    relightBtn.style.display='none';
  }
</script>
</body>
</html>
"""

def placeholder_svg(text: str) -> str:
    # tiny inline SVG placeholder with label
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='400' height='300'>"
            f"<rect width='100%'
