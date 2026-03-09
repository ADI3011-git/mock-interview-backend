<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>InterviewAI — Voice Mock Interview</title>
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/docx/7.8.2/docx.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #7c6af7;
    --accent2: #f76a8c;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --success: #4ade80;
    --danger: #f87171;
    --glow: rgba(124,106,247,0.18);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }
  body::before {
    content: '';
    position: fixed; inset: 0;
    background: radial-gradient(ellipse 80% 50% at 50% -10%, rgba(124,106,247,0.12), transparent),
                radial-gradient(ellipse 50% 40% at 90% 80%, rgba(247,106,140,0.07), transparent);
    pointer-events: none; z-index: 0;
  }

  /* ── SCREENS ── */
  .screen { display: none; min-height: 100vh; position: relative; z-index: 1; }
  .screen.active { display: flex; flex-direction: column; }

  /* ── SETUP SCREEN ── */
  #setup-screen {
    align-items: center; justify-content: center;
    padding: 2rem;
  }
  .setup-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    width: 100%; max-width: 520px;
    box-shadow: 0 0 80px var(--glow);
  }
  .logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 2.5rem;
    display: flex; align-items: center; gap: 0.5rem;
  }
  .logo-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--accent2); }
  h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    line-height: 1.15;
    margin-bottom: 0.5rem;
  }
  h1 span { color: var(--accent); }
  .subtitle { color: var(--muted); font-size: 0.95rem; margin-bottom: 2rem; }

  label {
    display: block;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
  }
  .field { margin-bottom: 1.4rem; }
  input[type="text"], input[type="password"], select {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    padding: 0.75rem 1rem;
    outline: none;
    transition: border-color 0.2s;
  }
  input:focus, select:focus { border-color: var(--accent); }
  select option { background: var(--bg); }

  .upload-zone {
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
  }
  .upload-zone:hover, .upload-zone.dragover {
    border-color: var(--accent);
    background: rgba(124,106,247,0.05);
  }
  .upload-zone input { position: absolute; inset: 0; opacity: 0; cursor: pointer; width: 100%; }
  .upload-icon { font-size: 2rem; margin-bottom: 0.5rem; }
  .upload-text { font-size: 0.9rem; color: var(--muted); }
  .upload-text strong { color: var(--accent); }
  .file-name {
    font-size: 0.85rem; color: var(--success);
    margin-top: 0.5rem; display: none;
  }

  .btn {
    width: 100%;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 0.85rem 1.5rem;
    font-family: 'Syne', sans-serif;
    font-size: 1rem; font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.03em;
  }
  .btn:hover { background: #6a59e0; transform: translateY(-1px); box-shadow: 0 8px 24px var(--glow); }
  .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
  .btn-outline {
    background: transparent;
    border: 1px solid var(--border);
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem; font-weight: 400;
  }
  .btn-outline:hover { border-color: var(--accent); color: var(--accent); background: transparent; box-shadow: none; }

  /* ── LOADING SCREEN ── */
  #loading-screen {
    align-items: center; justify-content: center;
    gap: 1.5rem; text-align: center;
  }
  .spinner {
    width: 56px; height: 56px;
    border: 3px solid var(--border);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .loading-text { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 600; }
  .loading-sub { color: var(--muted); font-size: 0.85rem; }

  /* ── INTERVIEW SCREEN ── */
  #interview-screen { padding: 2rem; gap: 1.5rem; }
  .interview-header {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 1rem;
  }
  .interview-meta { display: flex; align-items: center; gap: 1rem; }
  .role-badge {
    background: rgba(124,106,247,0.15);
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem; color: var(--accent);
    font-weight: 500;
  }
  .progress-text { color: var(--muted); font-size: 0.85rem; }
  .progress-bar-wrap {
    background: var(--border); border-radius: 999px;
    height: 4px; width: 100%; max-width: 600px; margin: 0 auto;
  }
  .progress-bar {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    transition: width 0.5s ease;
    width: 0%;
  }

  .interview-body {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 2rem; max-width: 680px; margin: 0 auto; width: 100%;
  }

  .ai-avatar {
    width: 80px; height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    box-shadow: 0 0 40px var(--glow);
    position: relative;
  }
  .ai-avatar.speaking::after {
    content: '';
    position: absolute; inset: -6px;
    border-radius: 50%;
    border: 2px solid var(--accent);
    animation: pulse-ring 1s ease-out infinite;
  }
  @keyframes pulse-ring {
    0% { transform: scale(1); opacity: 0.8; }
    100% { transform: scale(1.3); opacity: 0; }
  }

  .question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    width: 100%;
    text-align: center;
  }
  .q-label { color: var(--muted); font-size: 0.75rem; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1rem; }
  .q-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem; font-weight: 600;
    line-height: 1.5;
  }

  .voice-controls {
    display: flex; flex-direction: column;
    align-items: center; gap: 1rem; width: 100%;
  }
  .mic-btn {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: var(--surface);
    border: 2px solid var(--border);
    color: var(--text);
    font-size: 1.8rem;
    cursor: pointer;
    transition: all 0.2s;
    display: flex; align-items: center; justify-content: center;
  }
  .mic-btn:hover { border-color: var(--accent); color: var(--accent); }
  .mic-btn.recording {
    background: rgba(247,106,140,0.15);
    border-color: var(--accent2);
    color: var(--accent2);
    animation: mic-pulse 1s ease infinite;
  }
  @keyframes mic-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(247,106,140,0.4); }
    50% { box-shadow: 0 0 0 12px rgba(247,106,140,0); }
  }
  .voice-status { color: var(--muted); font-size: 0.85rem; text-align: center; min-height: 1.2em; }
  .transcript-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    width: 100%;
    min-height: 60px;
    font-size: 0.9rem;
    color: var(--text);
    font-style: italic;
    display: none;
  }
  .submit-answer-btn {
    display: none;
    width: auto;
    padding: 0.7rem 2rem;
    font-size: 0.9rem;
  }

  /* ── FEEDBACK SCREEN ── */
  #feedback-screen { padding: 2rem; }
  .feedback-inner { max-width: 700px; margin: 0 auto; }
  .feedback-header { text-align: center; margin-bottom: 2.5rem; }
  .feedback-header h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem;
  }
  .overall-score {
    display: inline-flex; flex-direction: column;
    align-items: center;
    background: linear-gradient(135deg, rgba(124,106,247,0.2), rgba(247,106,140,0.1));
    border: 1px solid rgba(124,106,247,0.3);
    border-radius: 20px;
    padding: 1.5rem 2.5rem;
    margin: 1rem auto;
  }
  .score-num {
    font-family: 'Syne', sans-serif;
    font-size: 3rem; font-weight: 800; color: var(--accent);
    line-height: 1;
  }
  .score-label { color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }

  .feedback-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 1rem; margin-bottom: 1.5rem;
  }
  @media (max-width: 500px) { .feedback-grid { grid-template-columns: 1fr; } }
  .param-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.2rem;
  }
  .param-name { font-size: 0.8rem; color: var(--muted); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }
  .param-score { font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 700; }
  .param-bar { height: 4px; background: var(--border); border-radius: 999px; margin-top: 0.5rem; overflow: hidden; }
  .param-bar-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--accent2)); }

  .feedback-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
  }
  .feedback-section h3 {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 1rem;
  }
  .feedback-section h3.green { color: var(--success); }
  .feedback-section h3.red { color: var(--danger); }
  .feedback-section h3.accent { color: var(--accent); }
  .feedback-section ul { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
  .feedback-section ul li {
    font-size: 0.9rem; line-height: 1.5;
    padding-left: 1.2rem; position: relative;
  }
  .feedback-section ul li::before {
    content: '→'; position: absolute; left: 0;
    color: var(--accent); font-size: 0.8rem;
  }

  .restart-btn { margin-top: 1.5rem; }

  /* ── MISC ── */
  .error-msg {
    background: rgba(248,113,113,0.1);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.85rem; color: var(--danger);
    margin-top: 0.75rem; display: none;
  }
</style>
</head>
<body>

<!-- LOGIN SCREEN -->
<div id="login-screen" class="screen active" style="align-items:center;justify-content:center;padding:2rem;">
  <div class="setup-card" style="text-align:center;max-width:420px;">
    <div class="logo" style="justify-content:center;"><div class="logo-dot"></div> InterviewAI</div>
    <h1 style="margin-bottom:0.5rem;">Sign in to<br/><span>InterviewAI</span></h1>
    <p class="subtitle">Only authorized users can access this platform.</p>
    <div id="g_id_onload" data-client_id="464022428512-r6bo5gov362ha7bcggnnmtc26ub721e5.apps.googleusercontent.com" data-callback="handleGoogleLogin" data-auto_prompt="false"></div>
    <div class="g_id_signin" data-type="standard" data-size="large" data-theme="filled_black" data-text="sign_in_with" data-shape="rectangular" data-logo_alignment="left" style="display:flex;justify-content:center;margin-top:1.5rem;"></div>
    <div class="error-msg" id="login-error" style="display:none;margin-top:1rem;"></div>
  </div>
</div>

<!-- SETUP SCREEN -->
<div id="setup-screen" class="screen">
  <div class="setup-card">
    <div class="logo"><div class="logo-dot"></div> InterviewAI</div>
    <h1>Ace your next<br/><span>interview</span></h1>
    <p class="subtitle">Upload your resume, pick a role — get a real voice interview powered by AI.</p>



    <div class="field">
      <label>Your Resume (PDF)</label>
      <div class="upload-zone" id="upload-zone">
        <input type="file" id="resume-file" accept=".pdf"/>
        <div class="upload-icon">📄</div>
        <div class="upload-text"><strong>Click to upload</strong> or drag & drop<br/>PDF only</div>
        <div class="file-name" id="file-name"></div>
      </div>
    </div>

    <div class="field">
      <label>Target Role</label>
      <select id="role-select">
        <option value="">— Select a role —</option>
        <option value="Supply Chain Manager">Supply Chain Manager</option>
        <option value="Operations Consultant">Operations Consultant</option>
        <option value="Demand Planner">Demand Planner</option>
        <option value="Procurement Manager">Procurement Manager</option>
        <option value="Business Analyst">Business Analyst</option>
        <option value="Strategy Consultant">Strategy Consultant</option>
        <option value="Product Manager">Product Manager</option>
        <option value="Data Analyst">Data Analyst</option>
        <option value="HR Manager">HR Manager</option>
        <option value="Finance Analyst">Finance Analyst</option>
      </select>
    </div>

    <div class="field">
      <label>Interview Type</label>
      <select id="interview-type">
        <option value="Technical/Domain">Technical / Domain</option>
        <option value="HR/Behavioral">HR / Behavioral</option>
        <option value="Mixed">Mixed (HR + Technical)</option>
      </select>
    </div>

    <button class="btn" id="start-btn" onclick="startInterview()">Start Interview →</button>
    <div class="error-msg" id="error-msg"></div>
  </div>
</div>

<!-- LOADING SCREEN -->
<div id="loading-screen" class="screen">
  <div class="spinner"></div>
  <div>
    <div class="loading-text" id="loading-text">Analyzing your resume…</div>
    <div class="loading-sub">Preparing personalized questions</div>
  </div>
</div>

<!-- INTERVIEW SCREEN -->
<div id="interview-screen" class="screen">
  <div class="interview-header">
    <div class="logo"><div class="logo-dot"></div> InterviewAI</div>
    <div class="interview-meta">
      <div class="role-badge" id="role-badge">Role</div>
      <div class="progress-text" id="progress-text">Q 1 of 7</div>
    </div>
  </div>
  <div class="progress-bar-wrap"><div class="progress-bar" id="progress-bar"></div></div>

  <div class="interview-body">
    <div class="ai-avatar" id="ai-avatar">🤖</div>

    <div class="question-card">
      <div class="q-label">Interviewer — Alex</div>
      <div class="q-text" id="q-text">Loading question…</div>
    </div>

    <div class="voice-controls">
      <button class="mic-btn" id="mic-btn" onclick="toggleRecording()" title="Hold to speak">🎤</button>
      <div class="voice-status" id="voice-status">Press mic to start answering</div>
      <textarea class="transcript-box" id="transcript-box" placeholder="Your answer will appear here — you can edit it before submitting..." style="resize:vertical;min-height:80px;width:100%;"></textarea>
      <div style="display:flex;gap:0.75rem;width:100%;justify-content:center;">
      <button class="btn submit-answer-btn" id="submit-btn" onclick="submitAnswer()">Submit Answer →</button>
      <button class="btn btn-outline submit-answer-btn" id="skip-btn" onclick="skipQuestion()" style="width:auto;padding:0.7rem 1.5rem;">Skip ⏭</button>
      </div>
    </div>
  </div>
</div>

<!-- FEEDBACK SCREEN -->
<div id="feedback-screen" class="screen">
  <div class="feedback-inner">
    <div class="feedback-header">
      <h2>Interview Complete 🎉</h2>
      <p style="color:var(--muted);font-size:0.9rem;">Here's your detailed performance feedback</p>
      <div class="overall-score">
        <div class="score-num" id="overall-score">—</div>
        <div class="score-label">Overall Score / 50</div>
      </div>
    </div>

    <div class="feedback-grid" id="params-grid"></div>
    <div id="feedback-sections"></div>

    <button class="btn" id="download-btn" onclick="downloadPracticeGuide()" style="margin-bottom:1rem;">📥 Download Practice Guide</button>
    <button class="btn btn-outline restart-btn" onclick="restart()">← Start New Interview</button>
  </div>
</div>

<script>
  // ── STATE ──
  const BACKEND_URL = 'https://mock-interview-backend-ocw5.onrender.com';

  // ── GOOGLE LOGIN ──
function handleGoogleLogin(response) {
  showScreen('setup-screen');
}
  
  let resumeText = '';
  let targetRole = '';
  let interviewType = '';
  let questions = [];
  let currentQ = 0;
  let answers = [];
  let recognition = null;
  let isRecording = false;
  let currentTranscript = '';
  let synth = window.speechSynthesis;

  // ── FILE UPLOAD ──
  const uploadZone = document.getElementById('upload-zone');
  const fileInput = document.getElementById('resume-file');
  const fileNameEl = document.getElementById('file-name');

  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dragover'); });
  uploadZone.addEventListener('dragleave', () => uploadZone.classList.remove('dragover'));
  uploadZone.addEventListener('drop', e => {
    e.preventDefault(); uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', () => { if (fileInput.files[0]) handleFile(fileInput.files[0]); });

  function handleFile(file) {
    fileNameEl.textContent = '✓ ' + file.name;
    fileNameEl.style.display = 'block';
  }

  // ── SHOW SCREEN ──
  function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
  }

  // ── START INTERVIEW ──
  async function startInterview() {
    targetRole = document.getElementById('role-select').value;
    interviewType = document.getElementById('interview-type').value;
    const file = document.getElementById('resume-file').files[0];
    const errorEl = document.getElementById('error-msg');
    errorEl.style.display = 'none';

    if (!file) return showError('Please upload your resume PDF.');
    if (!targetRole) return showError('Please select a target role.');

    showScreen('loading-screen');

    try {
      const base64 = await fileToBase64(file);
      document.getElementById('loading-text').textContent = 'Generating questions…';

      // Generate questions via backend
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          max_tokens: 1500,
          messages: [{
            role: 'user',
            content: [
              { type: 'document', source: { type: 'base64', media_type: 'application/pdf', data: base64 } },
              { type: 'text', text: `You are a senior interviewer. The candidate is applying for: ${targetRole}. Interview type: ${interviewType}.

Based on this resume, generate exactly 7 interview questions. Mix general role questions with resume-specific ones.

Respond ONLY with a JSON array of 7 strings. No preamble, no markdown. Example:
["Question 1?","Question 2?","Question 3?","Question 4?","Question 5?","Question 6?","Question 7?"]` }
            ]
          }]
        })
      });

      const data = await response.json();
      if (data.error) throw new Error(typeof data.error === 'string' ? data.error : JSON.stringify(data.error));

      const raw = data.content.map(c => c.text || '').join('');
      const clean = raw.replace(/```json|```/g, '').trim();
      questions = JSON.parse(clean);

      if (!Array.isArray(questions) || questions.length === 0) throw new Error('Failed to generate questions.');

      currentQ = 0; answers = [];
      document.getElementById('role-badge').textContent = targetRole;
      showScreen('interview-screen');
      showQuestion();

    } catch (err) {
      showScreen('setup-screen');
      showError('Error: ' + err.message);
    }
  }

  function showError(msg) {
    const el = document.getElementById('error-msg');
    el.textContent = msg; el.style.display = 'block';
  }

  function fileToBase64(file) {
    return new Promise((res, rej) => {
      const r = new FileReader();
      r.onload = () => res(r.result.split(',')[1]);
      r.onerror = () => rej(new Error('File read failed'));
      r.readAsDataURL(file);
    });
  }

  // ── SHOW QUESTION ──
  function showQuestion() {
    const total = questions.length;
    document.getElementById('q-text').textContent = questions[currentQ];
    document.getElementById('progress-text').textContent = `Q ${currentQ + 1} of ${total}`;
    document.getElementById('progress-bar').style.width = `${((currentQ) / total) * 100}%`;
    const tb = document.getElementById('transcript-box'); tb.style.display = 'none'; tb.value = '';
    document.getElementById('submit-btn').style.display = 'none';
    document.getElementById('skip-btn').style.display = 'inline-block';
    document.getElementById('voice-status').textContent = 'Press mic to start answering';
    document.getElementById('mic-btn').classList.remove('recording');
    currentTranscript = '';

    // Speak question
    setTimeout(() => speakText(questions[currentQ]), 400);
  }

  // ── SPEECH SYNTHESIS ──
  function speakText(text) {
    synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.rate = 0.95; utter.pitch = 1;
    const voices = synth.getVoices();
    const preferred = voices.find(v => v.name.includes('Google UK English Male') || v.name.includes('Daniel') || v.name.includes('Alex'));
    if (preferred) utter.voice = preferred;
    const avatar = document.getElementById('ai-avatar');
    utter.onstart = () => avatar.classList.add('speaking');
    utter.onend = () => avatar.classList.remove('speaking');
    synth.speak(utter);
  }

  // ── SPEECH RECOGNITION ──
  function toggleRecording() {
    if (isRecording) stopRecording();
    else startRecording();
  }

  function startRecording() {
    synth.cancel();
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { alert('Speech Recognition not supported in this browser. Use Chrome.'); return; }

    recognition = new SR();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = e => {
      let interim = '', final = '';
      for (let i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) final += e.results[i][0].transcript;
        else interim += e.results[i][0].transcript;
      }
      currentTranscript += final;
      const tBox = document.getElementById('transcript-box');
      tBox.style.display = 'block';
      tBox.value = currentTranscript + (interim ? ' ' + interim : '');
    };

    recognition.onerror = e => {
      document.getElementById('voice-status').textContent = 'Error: ' + e.error;
      stopRecording();
    };

    recognition.start();
    isRecording = true;
    document.getElementById('mic-btn').classList.add('recording');
    document.getElementById('voice-status').textContent = '🔴 Recording… press mic again to stop';
  }

  function stopRecording() {
    if (recognition) recognition.stop();
    isRecording = false;
    document.getElementById('mic-btn').classList.remove('recording');
    document.getElementById('voice-status').textContent = 'Answer captured. Submit when ready.';
    if (currentTranscript.trim()) {
      document.getElementById('submit-btn').style.display = 'inline-block';
      document.getElementById('skip-btn').style.display = 'inline-block';
    } else {
      document.getElementById('voice-status').textContent = 'No answer detected. Try again.';
    }
  }

  // ── SUBMIT ANSWER ──
  function submitAnswer() {
    const editedAnswer = document.getElementById('transcript-box').value.trim() || currentTranscript.trim();
    answers.push({ question: questions[currentQ], answer: editedAnswer });
    currentQ++;

    if (currentQ < questions.length) {
      showQuestion();
    } else {
      generateFeedback();
    }
  }

  // ── GENERATE FEEDBACK ──
  async function generateFeedback() {
    showScreen('loading-screen');
    document.getElementById('loading-text').textContent = 'Generating feedback…';

    const transcript = answers.map((a, i) => `Q${i+1}: ${a.question}\nA: ${a.answer}`).join('\n\n');

    try {
      const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          max_tokens: 1500,
          messages: [{
            role: 'user',
            content: `You are an expert MBA interview evaluator. The candidate applied for: ${targetRole}. Interview type: ${interviewType}.

Here is the full interview transcript:
${transcript}

Evaluate and respond ONLY with a JSON object (no markdown, no preamble):
{
  "overall": <number out of 50>,
  "params": [
    {"name": "Concept Clarity", "score": <out of 10>},
    {"name": "Practical Application", "score": <out of 10>},
    {"name": "Communication", "score": <out of 10>},
    {"name": "Depth of Knowledge", "score": <out of 10>},
    {"name": "Confidence & Composure", "score": <out of 10>}
  ],
  "strengths": ["point 1", "point 2", "point 3"],
  "improvements": ["point 1", "point 2", "point 3"],
  "topics": ["topic 1", "topic 2", "topic 3"]
}`
          }]
        })
      });

      const data = await response.json();
      const raw = data.content.map(c => c.text || '').join('');
      const clean = raw.replace(/```json|```/g, '').trim();
      const fb = JSON.parse(clean);
      renderFeedback(fb);

    } catch (err) {
      showScreen('interview-screen');
      alert('Feedback generation failed: ' + err.message);
    }
  }

  // ── RENDER FEEDBACK ──
  function renderFeedback(fb) {
    document.getElementById('overall-score').textContent = fb.overall;

    // Params grid
    const grid = document.getElementById('params-grid');
    grid.innerHTML = fb.params.map(p => `
      <div class="param-card">
        <div class="param-name">${p.name}</div>
        <div class="param-score">${p.score}<span style="color:var(--muted);font-size:0.9rem">/10</span></div>
        <div class="param-bar"><div class="param-bar-fill" style="width:${p.score * 10}%"></div></div>
      </div>
    `).join('');

    // Sections
    document.getElementById('feedback-sections').innerHTML = `
      <div class="feedback-section">
        <h3 class="green">✓ Strengths</h3>
        <ul>${fb.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
      </div>
      <div class="feedback-section">
        <h3 class="red">✗ Areas to Improve</h3>
        <ul>${fb.improvements.map(s => `<li>${s}</li>`).join('')}</ul>
      </div>
      <div class="feedback-section">
        <h3 class="accent">📚 Topics to Revise</h3>
        <ul>${fb.topics.map(s => `<li>${s}</li>`).join('')}</ul>
      </div>
    `;

    showScreen('feedback-screen');
  }

  // ── DOWNLOAD PRACTICE GUIDE ──
  async function callGroq(prompt) {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        max_tokens: 2000,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await response.json();
    const raw = data.content.map(c => c.text || '').join('');
    return raw.replace(/```json|```/g, '').trim();
  }

  async function downloadPracticeGuide() {
    const btn = document.getElementById('download-btn');
    btn.textContent = '⏳ Generating guide…';
    btn.disabled = true;

    try {
      const questionList = answers.map((a, i) => `Q${i+1}: ${a.question}`).join('\n');

      // Call 1: Ideal answers for interview questions
      btn.textContent = '⏳ Generating ideal answers…';
      const idealRaw = await callGroq(`You are an expert interview coach for ${targetRole} roles.

Here are the interview questions:
${questionList}

Respond ONLY with a JSON array (no markdown, no preamble):
[
  {"question": "question text", "answer": "ideal answer max 2 sentences"},
  ...
]
Keep each answer to 2 sentences max. Provide ideal answers for all ${answers.length} questions.`);

      const idealAnswers = JSON.parse(idealRaw);

      // Call 2: 20 practice questions
      btn.textContent = '⏳ Generating practice questions…';
      const practiceRaw = await callGroq(`You are an expert interview coach for ${targetRole} roles.

Generate exactly 10 practice interview questions with ideal answers. Keep each answer to 2 sentences max.

Respond ONLY with a JSON array (no markdown, no preamble):
[
  {"question": "question text", "answer": "ideal answer max 2 sentences"},
  ...
]`);

      const practiceQuestions = JSON.parse(practiceRaw);

      // Build Word document
      btn.textContent = '⏳ Building document…';
      const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = docx;

      const doc = new Document({
        sections: [{
          properties: {},
          children: [
            new Paragraph({
              text: `Interview Practice Guide — ${targetRole}`,
              heading: HeadingLevel.HEADING_1,
              alignment: AlignmentType.CENTER,
            }),
            new Paragraph({ text: '' }),
            new Paragraph({
              text: 'PART 1: Your Interview Questions & Ideal Answers',
              heading: HeadingLevel.HEADING_2,
            }),
            new Paragraph({ text: '' }),
            ...idealAnswers.flatMap((item, i) => [
              new Paragraph({ children: [new TextRun({ text: `Q${i+1}: ${item.question}`, bold: true, size: 24 })] }),
              new Paragraph({ children: [new TextRun({ text: `Ideal Answer: ${item.answer}`, color: '2E7D32' })] }),
              new Paragraph({ text: '' }),
            ]),
            new Paragraph({
              text: 'PART 2: 10 Practice Questions & Ideal Answers',
              heading: HeadingLevel.HEADING_2,
            }),
            new Paragraph({ text: '' }),
            ...practiceQuestions.flatMap((item, i) => [
              new Paragraph({ children: [new TextRun({ text: `Q${i+1}: ${item.question}`, bold: true, size: 24 })] }),
              new Paragraph({ children: [new TextRun({ text: `Ideal Answer: ${item.answer}`, color: '1565C0' })] }),
              new Paragraph({ text: '' }),
            ]),
          ]
        }]
      });

      const blob = await Packer.toBlob(doc);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Interview_Practice_Guide_${targetRole.replace(/ /g,'_')}.docx`;
      a.click();
      URL.revokeObjectURL(url);

      btn.textContent = '✅ Downloaded!';
      btn.disabled = false;

    } catch (err) {
      btn.textContent = '❌ Failed. Try again.';
      btn.disabled = false;
      console.error(err);
      alert('Error: ' + err.message);
    }
  }

  // ── SKIP QUESTION ──
  function skipQuestion() {
    answers.push({ question: questions[currentQ], answer: '[Skipped]' });
    currentQ++;
    if (currentQ < questions.length) {
      showQuestion();
    } else {
      generateFeedback();
    }
  }

  // ── RESTART ──
  function restart() {
    questions = []; answers = []; currentQ = 0; currentTranscript = '';
    document.getElementById('resume-file').value = '';
    document.getElementById('file-name').style.display = 'none';
    document.getElementById('role-select').value = '';
    showScreen('setup-screen');
  }

  // Preload voices
  window.speechSynthesis.onvoiceschanged = () => synth.getVoices();
</script>
</body>
</html>F
