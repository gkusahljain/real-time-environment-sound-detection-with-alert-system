let stream = null;
let interval = null;
let lastAlertTime = 0;

const ALERT_COOLDOWN = 60 * 1000;   // 60 seconds
const ALERT_DISPLAY_TIME = 20 * 1000; // 20 seconds

/* ===================== UPLOAD ===================== */
async function upload() {
  const fileInput = document.getElementById("fileInput");
  if (!fileInput.files.length) {
    alert("Select a WAV file");
    return;
  }

  showLoading("⏳ Analyzing uploaded audio...");

  const formData = new FormData();
  formData.append("audio", fileInput.files[0]);

  try {
    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    display(data);
    const alertBox = document.getElementById("alerts-container");

    if (data.alerts && data.alerts.length > 0) {
      alertBox.classList.remove("idle");
      alertBox.classList.add("active");
    } else {
      alertBox.classList.remove("active");
      alertBox.classList.add("idle");
    }

  } catch (err) {
    showError("❌ Backend not reachable");
  }
}

/* ===================== MONITORING ===================== */
async function start() {
  if (stream) return;

  try {
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    interval = setInterval(sendChunk, 2000);
    showLoading("🎧 Monitoring environment...");
  } catch (err) {
    showError("❌ Microphone permission denied");
  }
}

function stop() {
  if (interval) clearInterval(interval);
  interval = null;

  if (stream) {
    stream.getTracks().forEach(t => t.stop());
    stream = null;
  }

  document.getElementById("results").innerHTML =
    "<p class='hint'>🛑 Monitoring stopped</p>";
}

/* ===================== AUDIO CHUNK ===================== */
function sendChunk() {
  if (!stream) return;

  const recorder = new MediaRecorder(stream, { mimeType: "audio/webm" });
  const chunks = [];

  recorder.ondataavailable = e => {
    if (e.data.size > 0) chunks.push(e.data);
  };

  recorder.onstop = async () => {
    if (chunks.length === 0) return;

    const blob = new Blob(chunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", blob);

    try {
      const res = await fetch("http://127.0.0.1:8000/monitor", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      display(data);
    } catch (err) {
      console.error(err);
    }
  };

  recorder.start();
  setTimeout(() => recorder.stop(), 2000);
}

/* ===================== UI HELPERS ===================== */
function showLoading(text) {
  document.getElementById("results").innerHTML =
    `<p class="loading">${text}</p>`;
}

function showError(msg) {
  document.getElementById("results").innerHTML =
    `<p class="error">${msg}</p>`;
}

/* ===================== DISPLAY ===================== */
function display(data) {
  const resultsBox = document.getElementById("results");
  const alertsBox = document.getElementById("alerts");

  /* ---------- RESULTS ---------- */
  if (!data.results || data.results.length === 0) {
    resultsBox.innerHTML = "<p class='hint'>No dominant sounds detected</p>";
  } else {
    resultsBox.innerHTML = data.results.map(r => {
      const percent = Math.round(r.score * 100);
      return `
        <div class="result-item">
          🎵 <b>${r.label}</b>
          <div class="bar-bg">
            <div class="bar-fill" style="width:${percent}%"></div>
          </div>
          <span>${percent}%</span>
        </div>
      `;
    }).join("");
  }

  /* ---------- SPECTROGRAM ---------- */
  const specContainer = document.getElementById("spectrogram-container");
  if (data.spectrogram) {
    specContainer.innerHTML = `
      <h3>📊 Mel Spectrogram</h3>
      <img src="data:image/png;base64,${data.spectrogram}" style="max-width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);">
    `;
  } else {
    specContainer.innerHTML = "";
  }

  /* ---------- ALERTS (WITH COOLDOWN) ---------- */
  const now = Date.now();

  if (data.alerts && data.alerts.length > 0) {
    alertsBox.innerHTML = data.alerts.map(a => {
      const pct = Math.round(a.confidence * 100);
      return `
        <div class="alert-item">
          🚨 <b>${a.type}</b> detected (${pct}%)
        </div>
      `;
    }).join("");
  } else {
    alertsBox.innerHTML = "<p class='hint'>No active alerts</p>";
  }
}
