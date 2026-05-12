"""
REVA-ID — Google Colab Setup & Runner
======================================
Jalankan sel ini satu per satu di Google Colab.
"""

# ── SEL 1: Install dependencies ───────────────────────────────────────────────
INSTALL = """
!pip install streamlit plotly scikit-learn openpyxl statsmodels -q
!pip install pyngrok -q
"""

# ── SEL 2: Upload file project ────────────────────────────────────────────────
UPLOAD_NOTE = """
# Cara 1 — Upload ZIP (direkomendasikan):
from google.colab import files
uploaded = files.upload()   # Upload reva_id.zip
!unzip -q reva_id.zip -d /content/reva_id

# Cara 2 — Clone dari GitHub (jika sudah push ke repo):
# !git clone https://github.com/USERNAME/reva-id.git /content/reva_id
"""

# ── SEL 3: Jalankan Streamlit via ngrok ───────────────────────────────────────
RUN_STREAMLIT = """
import subprocess, threading, time
from pyngrok import ngrok

# Ganti dengan token ngrok Anda (gratis di https://dashboard.ngrok.com)
NGROK_TOKEN = "PASTE_TOKEN_NGROK_ANDA_DI_SINI"
ngrok.set_auth_token(NGROK_TOKEN)

# Jalankan Streamlit di background
proc = subprocess.Popen(
    ["streamlit", "run", "/content/reva_id/app.py",
     "--server.port", "8501",
     "--server.headless", "true",
     "--server.enableCORS", "false"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
time.sleep(4)

# Buka tunnel publik
tunnel = ngrok.connect(8501)
print("=" * 60)
print("✅ REVA-ID Dashboard berjalan di:")
print(f"   {tunnel.public_url}")
print("=" * 60)
"""

# ── SEL 4 (alternatif tanpa ngrok): LocalTunnel ───────────────────────────────
RUN_LOCALTUNNEL = """
!npm install -g localtunnel -q

import subprocess, time, threading

proc = subprocess.Popen(
    ["streamlit", "run", "/content/reva_id/app.py", "--server.port", "8501"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)
time.sleep(5)

# Buka tunnel
lt = subprocess.Popen(
    ["lt", "--port", "8501"],
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
for line in lt.stdout:
    decoded = line.decode()
    if "https://" in decoded:
        print("✅ Akses dashboard di:", decoded.strip())
        break
"""

if __name__ == "__main__":
    print("=" * 60)
    print("REVA-ID — Panduan Setup Google Colab")
    print("=" * 60)
    print("\n1. Install dependencies:")
    print(INSTALL)
    print("\n2. Upload project:")
    print(UPLOAD_NOTE)
    print("\n3. Jalankan dengan ngrok:")
    print(RUN_STREAMLIT)
    print("\n3b. Atau dengan localtunnel (tanpa token):")
    print(RUN_LOCALTUNNEL)
