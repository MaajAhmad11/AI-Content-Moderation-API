{% verbatim %}<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AI Content Moderation · Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>
  :root{
    --bg:#0a0a0c; --bg-soft:#101013; --panel:#141418; --panel-2:#191920;
    --line:#26262e; --line-soft:#1d1d24;
    --txt:#ECECEF; --txt-dim:#9a9aa6; --txt-faint:#62626d;
    --primary:#6366f1; --primary-glow:rgba(99,102,241,.35);
    --safe:#10b981; --safe-bg:rgba(16,185,129,.10); --safe-line:rgba(16,185,129,.30);
    --flag:#f43f5e; --flag-bg:rgba(244,63,94,.10); --flag-line:rgba(244,63,94,.32);
    --radius:16px;
    --mono:'JetBrains Mono',ui-monospace,monospace;
    font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    background:
      radial-gradient(900px 500px at 80% -10%, rgba(99,102,241,.12), transparent 60%),
      radial-gradient(700px 500px at 0% 110%, rgba(16,185,129,.07), transparent 55%),
      var(--bg);
    color:var(--txt); min-height:100vh; line-height:1.5;
    -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:1080px;margin:0 auto;padding:28px 22px 80px}

  /* Header */
  header{display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:30px}
  .brand{display:flex;align-items:center;gap:12px}
  .logo{
    width:40px;height:40px;border-radius:11px;display:grid;place-items:center;
    background:linear-gradient(145deg,#6366f1,#4338ca);
    box-shadow:0 6px 20px -6px var(--primary-glow),inset 0 1px 0 rgba(255,255,255,.18);
  }
  .logo svg{width:21px;height:21px}
  .brand h1{font-size:16px;font-weight:700;letter-spacing:-.01em}
  .brand p{font-size:12px;color:var(--txt-faint);font-weight:500}
  .status{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:500;color:var(--txt-dim);
    background:var(--panel);border:1px solid var(--line);padding:7px 12px;border-radius:999px}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--txt-faint);transition:.3s}
  .dot.on{background:var(--safe);box-shadow:0 0 0 4px var(--safe-bg)}
  .dot.off{background:var(--flag);box-shadow:0 0 0 4px var(--flag-bg)}

  .grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
  @media(max-width:860px){.grid{grid-template-columns:1fr}}

  .card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
    box-shadow:0 1px 0 rgba(255,255,255,.02) inset, 0 20px 40px -30px rgba(0,0,0,.8)}
  .card-pad{padding:22px}

  /* Tabs */
  .tabs{display:flex;gap:4px;background:var(--bg-soft);border:1px solid var(--line-soft);
    padding:4px;border-radius:12px;margin-bottom:20px}
  .tab{flex:1;border:none;background:transparent;color:var(--txt-dim);font:inherit;font-size:13.5px;
    font-weight:600;padding:9px;border-radius:9px;cursor:pointer;transition:.18s;display:flex;
    align-items:center;justify-content:center;gap:7px}
  .tab svg{width:15px;height:15px;opacity:.85}
  .tab.active{background:var(--panel-2);color:var(--txt);box-shadow:0 1px 0 rgba(255,255,255,.05) inset,0 4px 12px -6px rgba(0,0,0,.6)}

  label{display:block;font-size:12px;font-weight:600;color:var(--txt-dim);margin:0 0 7px 2px;letter-spacing:.01em}
  .field{margin-bottom:16px}
  input,textarea{width:100%;background:var(--bg-soft);border:1px solid var(--line);color:var(--txt);
    font:inherit;font-size:14px;padding:12px 13px;border-radius:11px;transition:.16s;resize:vertical}
  input::placeholder,textarea::placeholder{color:var(--txt-faint)}
  input:focus,textarea:focus{outline:none;border-color:var(--primary);box-shadow:0 0 0 3px var(--primary-glow)}
  textarea{min-height:96px;line-height:1.55}

  .chips{display:flex;flex-wrap:wrap;gap:7px;margin:-4px 0 16px}
  .chip{font-size:11.5px;font-weight:600;padding:6px 11px;border-radius:999px;cursor:pointer;
    border:1px solid var(--line);background:var(--panel-2);color:var(--txt-dim);transition:.15s}
  .chip:hover{border-color:var(--primary);color:var(--txt)}
  .chip.bad:hover{border-color:var(--flag-line);color:#ffb3c0}
  .chip.good:hover{border-color:var(--safe-line);color:#7ee2c1}

  .btn{width:100%;border:none;font:inherit;font-size:14.5px;font-weight:700;color:#fff;
    background:linear-gradient(145deg,#6366f1,#4f46e5);padding:13px;border-radius:12px;cursor:pointer;
    transition:.16s;display:flex;align-items:center;justify-content:center;gap:9px;
    box-shadow:0 8px 22px -10px var(--primary-glow),inset 0 1px 0 rgba(255,255,255,.18)}
  .btn:hover{transform:translateY(-1px);box-shadow:0 12px 26px -10px var(--primary-glow)}
  .btn:active{transform:translateY(0)}
  .btn:disabled{opacity:.6;cursor:not-allowed;transform:none}
  .spin{width:16px;height:16px;border:2px solid rgba(255,255,255,.35);border-top-color:#fff;
    border-radius:50%;animation:sp .6s linear infinite}
  @keyframes sp{to{transform:rotate(360deg)}}

  /* Result panel */
  .result-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
  .result-head h2{font-size:13px;font-weight:600;color:var(--txt-dim);letter-spacing:.02em;text-transform:uppercase}
  .empty{display:flex;flex-direction:column;align-items:center;justify-content:center;
    text-align:center;padding:46px 20px;color:var(--txt-faint)}
  .empty svg{width:38px;height:38px;margin-bottom:14px;opacity:.4}
  .empty p{font-size:13.5px;max-width:240px}

  .verdict{border-radius:14px;padding:20px;border:1px solid var(--line);background:var(--bg-soft);
    animation:pop .25s ease}
  @keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
  .verdict.safe{border-color:var(--safe-line);background:var(--safe-bg)}
  .verdict.flag{border-color:var(--flag-line);background:var(--flag-bg)}
  .verdict-top{display:flex;align-items:center;gap:12px;margin-bottom:16px}
  .badge{width:46px;height:46px;border-radius:13px;display:grid;place-items:center;flex-shrink:0}
  .badge svg{width:24px;height:24px}
  .safe .badge{background:var(--safe);color:#04130d}
  .flag .badge{background:var(--flag);color:#1a0307}
  .verdict-title{font-size:19px;font-weight:800;letter-spacing:-.02em}
  .safe .verdict-title{color:#3ee0aa}
  .flag .verdict-title{color:#ff7088}
  .verdict-sub{font-size:12.5px;color:var(--txt-dim);font-weight:500}

  .meter-wrap{margin:4px 0 16px}
  .meter-label{display:flex;justify-content:space-between;font-size:11.5px;color:var(--txt-dim);
    font-weight:600;margin-bottom:6px}
  .meter{height:8px;border-radius:99px;background:var(--line);overflow:hidden}
  .meter span{display:block;height:100%;border-radius:99px;width:0;transition:width .7s cubic-bezier(.2,.8,.2,1)}
  .safe .meter span{background:linear-gradient(90deg,#10b981,#34d399)}
  .flag .meter span{background:linear-gradient(90deg,#f43f5e,#fb7185)}

  .meta{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .meta-item{background:rgba(0,0,0,.22);border:1px solid var(--line-soft);border-radius:10px;padding:10px 12px}
  .meta-item .k{font-size:10.5px;color:var(--txt-faint);font-weight:600;text-transform:uppercase;letter-spacing:.04em}
  .meta-item .v{font-size:13px;font-weight:600;margin-top:2px;font-family:var(--mono);word-break:break-word}

  details.raw{margin-top:14px}
  details.raw summary{font-size:12px;color:var(--txt-dim);cursor:pointer;font-weight:600;
    list-style:none;display:flex;align-items:center;gap:6px}
  details.raw summary::-webkit-details-marker{display:none}
  details.raw summary::before{content:"›";font-size:16px;transition:.2s;display:inline-block}
  details.raw[open] summary::before{transform:rotate(90deg)}
  pre{margin-top:10px;background:#0c0c10;border:1px solid var(--line-soft);border-radius:10px;
    padding:13px;font-family:var(--mono);font-size:12px;color:#cdd3ff;overflow:auto;line-height:1.6}

  .err{background:var(--flag-bg);border:1px solid var(--flag-line);color:#ff95a6;
    padding:12px 14px;border-radius:11px;font-size:13px;font-weight:500}

  /* History */
  .hist-head{display:flex;align-items:center;justify-content:space-between;margin:34px 4px 14px}
  .hist-head h3{font-size:14px;font-weight:700;letter-spacing:-.01em}
  .clear{background:none;border:none;color:var(--txt-faint);font:inherit;font-size:12.5px;
    font-weight:600;cursor:pointer}
  .clear:hover{color:var(--flag)}
  .hist-list{display:flex;flex-direction:column;gap:8px}
  .hist-row{display:flex;align-items:center;gap:12px;background:var(--panel);border:1px solid var(--line);
    border-radius:12px;padding:11px 14px;animation:pop .2s ease}
  .pill{font-size:10.5px;font-weight:700;padding:4px 9px;border-radius:99px;flex-shrink:0;letter-spacing:.02em}
  .pill.safe{background:var(--safe-bg);color:#3ee0aa;border:1px solid var(--safe-line)}
  .pill.flag{background:var(--flag-bg);color:#ff7088;border:1px solid var(--flag-line)}
  .hist-row .body{flex:1;min-width:0}
  .hist-row .ct{font-size:13px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .hist-row .sub{font-size:11px;color:var(--txt-faint);font-family:var(--mono);margin-top:1px}
  .hist-row .sc{font-size:12px;font-weight:700;font-family:var(--mono);color:var(--txt-dim);flex-shrink:0}
  .hist-empty{text-align:center;color:var(--txt-faint);font-size:13px;padding:18px}
  .type-ico{width:15px;height:15px;color:var(--txt-faint);flex-shrink:0}

  footer{text-align:center;margin-top:40px;font-size:12px;color:var(--txt-faint)}
  footer a{color:var(--txt-dim);text-decoration:none;font-weight:600}
  footer a:hover{color:var(--primary)}
</style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="brand">
      <div class="logo">
        <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2 4 5v6c0 5 3.4 8.5 8 11 4.6-2.5 8-6 8-11V5l-8-3z"/><path d="m9 12 2 2 4-4"/>
        </svg>
      </div>
      <div>
        <h1>AI Content Moderation</h1>
        <p>Real-time text & image safety console</p>
      </div>
    </div>
    <div class="status">
      <span class="dot" id="dot"></span><span id="statusTxt">Checking API…</span>
    </div>
  </header>

  <div class="grid">
    <!-- INPUT -->
    <section class="card card-pad">
      <div class="tabs">
        <button class="tab active" data-mode="text" onclick="setMode('text')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>
          Text
        </button>
        <button class="tab" data-mode="image" onclick="setMode('image')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="1.6"/><path d="m21 15-5-5L5 21"/></svg>
          Image
        </button>
      </div>

      <div class="field">
        <label>User ID</label>
        <input id="userId" value="user_001" placeholder="Unique user identifier" />
      </div>

      <!-- TEXT -->
      <div id="textPane">
        <div class="field">
          <label>Text content</label>
          <textarea id="textInput" placeholder="Type or paste the message to moderate…"></textarea>
        </div>
        <div class="chips">
          <span class="chip bad" onclick="fillText('I will attack you with pure hate')">⚑ Toxic example</span>
          <span class="chip bad" onclick="fillText('Buy now! spam spam spam click here')">⚑ Spam example</span>
          <span class="chip good" onclick="fillText('Hello, hope you have a wonderful day!')">✓ Clean example</span>
        </div>
      </div>

      <!-- IMAGE -->
      <div id="imagePane" style="display:none">
        <div class="field">
          <label>Image URL</label>
          <input id="imageInput" placeholder="https://example.com/photo.jpg" />
        </div>
        <div class="chips">
          <span class="chip bad" onclick="fillImg('https://cdn.example.com/nsfw_photo.jpg')">⚑ Flagged URL</span>
          <span class="chip bad" onclick="fillImg('https://cdn.example.com/weapon_ad.png')">⚑ Weapon URL</span>
          <span class="chip good" onclick="fillImg('https://cdn.example.com/sunset_beach.jpg')">✓ Safe URL</span>
        </div>
      </div>

      <button class="btn" id="submitBtn" onclick="moderate()">
        <span id="btnText">Run moderation</span>
      </button>
    </section>

    <!-- RESULT -->
    <section class="card card-pad">
      <div class="result-head"><h2>Result</h2></div>
      <div id="resultBox">
        <div class="empty">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2 4 5v6c0 5 3.4 8.5 8 11 4.6-2.5 8-6 8-11V5l-8-3z"/></svg>
          <p>Submit some content and the moderation decision will appear here.</p>
        </div>
      </div>
    </section>
  </div>

  <!-- HISTORY -->
  <div class="hist-head">
    <h3>Recent checks</h3>
    <button class="clear" onclick="clearHist()">Clear</button>
  </div>
  <div class="hist-list" id="histList">
    <div class="hist-empty">No checks yet.</div>
  </div>

  <footer>
    Powered by your Django REST API &middot;
    <a href="/swagger/" target="_blank">API Docs</a> &middot;
    <a href="/admin/" target="_blank">Admin logs</a>
  </footer>
</div>

<script>
  const API = { text: "/api/moderate/text/", image: "/api/moderate/image/" };
  let mode = "text";
  let history = JSON.parse(localStorage.getItem("modHistory") || "[]");

  // ---- Health check (uses a deliberately invalid payload -> expect 400 = API alive)
  async function ping(){
    try{
      const r = await fetch(API.text, {method:"POST",headers:{"Content-Type":"application/json"},body:"{}"});
      ok(r.status === 400 || r.status === 200);
    }catch(e){ ok(false); }
  }
  function ok(up){
    const d=document.getElementById("dot"), t=document.getElementById("statusTxt");
    d.className = "dot " + (up?"on":"off");
    t.textContent = up ? "API connected" : "API offline";
  }

  function setMode(m){
    mode=m;
    document.querySelectorAll(".tab").forEach(b=>b.classList.toggle("active",b.dataset.mode===m));
    document.getElementById("textPane").style.display = m==="text"?"block":"none";
    document.getElementById("imagePane").style.display = m==="image"?"block":"none";
  }
  function fillText(v){ document.getElementById("textInput").value=v; }
  function fillImg(v){ document.getElementById("imageInput").value=v; }

  async function moderate(){
    const userId = document.getElementById("userId").value.trim();
    const btn=document.getElementById("submitBtn"), bt=document.getElementById("btnText");
    const box=document.getElementById("resultBox");

    let url, payload;
    if(mode==="text"){
      const text=document.getElementById("textInput").value.trim();
      if(!userId||!text){ showErr("Please enter a user ID and some text."); return; }
      url=API.text; payload={user_id:userId, text};
    }else{
      const image_url=document.getElementById("imageInput").value.trim();
      if(!userId||!image_url){ showErr("Please enter a user ID and an image URL."); return; }
      url=API.image; payload={user_id:userId, image_url};
    }

    btn.disabled=true; bt.textContent=""; btn.insertAdjacentHTML("afterbegin",'<span class="spin"></span>');
    try{
      const r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
      const data=await r.json();
      if(!r.ok){ showErr(formatErrors(data)); ok(true); }
      else { render(data); pushHist(data); ok(true); }
    }catch(e){
      showErr("Could not reach the API. Is the server running at this address?"); ok(false);
    }finally{
      btn.disabled=false; const s=btn.querySelector(".spin"); if(s)s.remove(); bt.textContent="Run moderation";
    }
  }

  function formatErrors(d){
    if(typeof d!=="object") return "Request rejected.";
    return Object.entries(d).map(([k,v])=>`${k}: ${Array.isArray(v)?v.join(", "):v}`).join(" · ");
  }
  function showErr(msg){
    document.getElementById("resultBox").innerHTML=`<div class="err">⚠ ${msg}</div>`;
  }

  function render(d){
    const flagged=d.is_flagged;
    const cls=flagged?"flag":"safe";
    const pct=Math.round((d.confidence_score||0)*100);
    const icon = flagged
      ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M12 8v5M12 17h.01"/><path d="M10.3 3.3 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.3a2 2 0 0 0-3.4 0z"/></svg>'
      : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m20 6-11 11-5-5"/></svg>';
    document.getElementById("resultBox").innerHTML=`
      <div class="verdict ${cls}">
        <div class="verdict-top">
          <div class="badge">${icon}</div>
          <div>
            <div class="verdict-title">${flagged?"Content Flagged":"Content Safe"}</div>
            <div class="verdict-sub">${flagged?(d.flag_reason||"Violates safety policy"):"No policy violations detected"}</div>
          </div>
        </div>
        <div class="meter-wrap">
          <div class="meter-label"><span>Confidence</span><span>${pct}%</span></div>
          <div class="meter"><span style="width:${pct}%"></span></div>
        </div>
        <div class="meta">
          <div class="meta-item"><div class="k">Log ID</div><div class="v">#${d.id}</div></div>
          <div class="meta-item"><div class="k">Type</div><div class="v">${d.content_type}</div></div>
          <div class="meta-item"><div class="k">User</div><div class="v">${esc(d.user_id)}</div></div>
          <div class="meta-item"><div class="k">Time</div><div class="v">${new Date(d.created_at).toLocaleTimeString()}</div></div>
        </div>
        <details class="raw"><summary>Raw JSON response</summary>
          <pre>${esc(JSON.stringify(d,null,2))}</pre>
        </details>
      </div>`;
  }

  function pushHist(d){
    history.unshift({id:d.id,type:d.content_type,flag:d.is_flagged,score:d.confidence_score,reason:d.flag_reason,user:d.user_id});
    history=history.slice(0,12);
    localStorage.setItem("modHistory",JSON.stringify(history));
    renderHist();
  }
  function clearHist(){ history=[]; localStorage.removeItem("modHistory"); renderHist(); }
  function renderHist(){
    const el=document.getElementById("histList");
    if(!history.length){ el.innerHTML='<div class="hist-empty">No checks yet.</div>'; return; }
    const tIco='<svg class="type-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h10"/></svg>';
    const iIco='<svg class="type-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="1.6"/><path d="m21 15-5-5L5 21"/></svg>';
    el.innerHTML=history.map(h=>`
      <div class="hist-row">
        <span class="pill ${h.flag?"flag":"safe"}">${h.flag?"FLAGGED":"SAFE"}</span>
        ${h.type==="text"?tIco:iIco}
        <div class="body">
          <div class="ct">${h.flag?esc(h.reason||"Policy violation"):"No violations"}</div>
          <div class="sub">#${h.id} · ${esc(h.user)}</div>
        </div>
        <span class="sc">${Math.round((h.score||0)*100)}%</span>
      </div>`).join("");
  }
  function esc(s){ return String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c])); }

  // init
  ping(); renderHist();
</script>
</body>
</html>{% endverbatim %}
