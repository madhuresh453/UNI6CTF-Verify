import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
import time
from concurrent.futures import ThreadPoolExecutor
from config import *

from config import EMAIL, PASSWORD, SMTP_SERVER, SMTP_PORT
import os

if not os.path.exists("output/final_data.csv") or os.path.getsize("output/final_data.csv") == 0:
    print("❌ No data found. Run generator first.")
    exit()

df = pd.read_csv("output/final_data.csv")

# 🔥 FIX COLUMN NAMES
df.columns = df.columns.str.strip()

print("Columns after fix:", df.columns.tolist())

# ✅ KEEP ONLY LATEST UNIQUE CERTIFICATES
if 'Certificate ID' in df.columns:
    df = df.drop_duplicates(subset=['Certificate ID'], keep='last')
else:
    print("❌ Column 'Certificate ID' not found")
    print("Available columns:", df.columns.tolist())
    exit()

# ✅ OPTIONAL: ONLY LAST BATCH (BEST)
df = df.tail(3)   # since your current file has 3 users

print("📊 Total unique emails:", len(df))

context = ssl.create_default_context()

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls(context=context)
    server.login(EMAIL, PASSWORD)

    for i, row in df.iterrows():
        try:
            email = row.get('Email')

            if pd.isna(email):
                print(f"❌ Missing email at row {i}")
                continue

            file_path = row.get('File')

            if not file_path or str(file_path) == "nan":
                print(f"❌ Missing file for {row.get('Username')}")
                continue

            msg = EmailMessage()
            msg['Subject'] = "🎉 UNI6CTF 1.0 Certificate"
            msg['From'] = EMAIL
            msg['To'] = email

            msg.set_content(f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {{
        margin:0;
        padding:0;
        background:#000000;
        font-family: Arial, sans-serif;
        color:#ffffff;
    }}

    .container {{
        max-width:600px;
        margin:20px auto;
        background:#121212;
        border-radius:10px;
        overflow:hidden;
        border:1px solid #2a2a2a;
    }}

    .header {{
        text-align:center;
        padding:20px;
        background:#000000;
        border-bottom:2px solid #FFD700;
    }}

    .logo {{
        width:80px;
        margin-bottom:8px;
    }}

    .title {{
        font-size:20px;
        color:#FFD700;
        font-weight:bold;
    }}

    .content {{
        padding:25px;
        font-size:14px;
        line-height:1.6;
        color:#ffffff;
    }}

    .highlight {{
        color:#FFD700;
        font-weight:bold;
    }}

    .card {{
        background:#1c1c1c;
        padding:15px;
        border-radius:8px;
        margin:20px 0;
        border:1px solid #333;
    }}

    .button {{
        display:inline-block;
        background:#FFD700;
        color:#000000 !important;
        padding:12px 20px;
        border-radius:6px;
        text-decoration:none;
        font-weight:bold;
        margin-top:20px;
    }}

    .preview {{
        margin-top:20px;
        text-align:center;
    }}

    .preview img {{
        width:100%;
        border-radius:8px;
        border:1px solid #333;
    }}

    .footer {{
        text-align:center;
        padding:15px;
        font-size:12px;
        color:#aaaaaa;
        border-top:1px solid #2a2a2a;
    }}
</style>
</head>

<body>

<div class="container">

    <!-- HEADER -->
    <div class="header">
        <img src="{LOGO_URL}" class="logo">
        <div class="title">🏆 UNI6CTF 1.0 Certificate</div>
    </div>

    <!-- CONTENT -->
    <div class="content">

        <p>Dear <span class="highlight">{row['Full Name']}</span>,</p>

        <p>
        Congratulations on successfully participating in 
        <span class="highlight">UNI6CTF 1.0 – Capture The Flag Competition</span>.
        </p>

        <!-- DETAILS -->
        <div class="card">
            <b>Username:</b> {row['Username']}<br>
            <b>Team:</b> {row['Team Name']}<br>
            <b>Rank:</b> {row['Rank']}<br>
            <b>Points:</b> {row['Points']}
        </div>

        <p>Your certificate is attached below.</p>

        <!-- BUTTON -->
        <a href="{BASE_URL}{row['Certificate ID']}" class="button">
            🔍 Verify Certificate
        </a>

        <!-- PREVIEW -->
        <div class="preview">
            <p style="color:#FFD700;">Certificate Preview</p>
            <img src="{CERT_BASE_URL}{row['Username']}.png">
        </div>

        <p style="margin-top:25px;">
        UNI6CTF is a student-driven cybersecurity initiative focused on real-world hacking skills, 
        CTF competitions, and building a strong cybersecurity community.
        </p>

        <p>
        We look forward to your participation in future competitions 🚀
        </p>

        <br>

        <p>
        Best Regards,<br><br>

        <b>Madhuresh Kumar Jha</b><br>
        CEO & Founder, UNI6CTF<br><br>

        <b>Krish Pathania</b><br>
        Co-Founder, UNI6CTF
        </p>

    </div>

    <!-- FOOTER -->
    <div class="footer">
        🌐 uni6ctf.online<br>
        📧 organizers@uni6ctf.online<br><br>
        This is an automated email. Please do not reply.
    </div>

</div>

<!-- TRACKING PIXEL -->
<img src="{TRACK_URL}{row['Certificate ID']}" width="1" height="1">

</body>
</html>
""", subtype='html')



        # ✅ ATTACH CERTIFICATE
            with open(file_path, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype='image',
                    subtype='png',
                    filename="certificate.png"
                )

            # ✅ SEND MAIL (NO NEW CONNECTION)
            server.send_message(msg)

            print(f"✅ Sent: {email}")

            time.sleep(2)  # 🔥 prevent SMTP timeout

        except Exception as e:
            print(f"❌ Failed: {row.get('Username')} → {e}")

    


