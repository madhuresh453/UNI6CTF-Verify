
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage
import time
import os

from config import EMAIL, PASSWORD, SMTP_SERVER, SMTP_PORT, BASE_URL, LOGO_URL, CERT_BASE_URL, TRACK_URL

# ===============================
# 📂 LOAD DATA
# ===============================
csv_path = "output/final_data.csv"

if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
    print("❌ No data found. Run generator first.")
    exit()

df = pd.read_csv(csv_path)

# 🔥 CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()
print("Columns:", df.columns.tolist())

# ===============================
# 🧹 CLEAN DATA
# ===============================
df = df[df['Email'].notna()]
df = df[df['File'].notna()]
df = df.drop_duplicates(subset=['Email'], keep='last')

print("📊 Total emails to send:", len(df))

# ===============================
# 🔐 SMTP SETUP
# ===============================
context = ssl.create_default_context()

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)

        # ===============================
        # 📧 SEND EMAIL LOOP
        # ===============================
        for _, row in df.iterrows():

            email = str(row['Email']).strip()
            file_path = str(row['File']).strip()

            # 🔍 DEBUG
            print(f"\n➡ Sending to: {email}")
            print(f"➡ File: {file_path}")
            print(f"➡ Cert ID: {row.get('Certificate ID')}")

            # ❌ skip if file missing
            if not os.path.exists(file_path):
                print(f"❌ File not found for {email}")
                continue

            try:
                msg = EmailMessage()
                msg['Subject'] = "🎉 UNI6CTF 1.0 Certificate"
                msg['From'] = EMAIL
                msg['To'] = email

                cert_id = row.get('Certificate ID', 'N/A')

                # ===============================
                # 📩 HTML EMAIL
                # ===============================
                html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {{
    margin:0;
    padding:0;
    background:#000;
    font-family:Arial;
    color:#fff;
}}
.container {{
    max-width:600px;
    margin:20px auto;
    background:#121212;
    border-radius:10px;
    border:1px solid #2a2a2a;
}}
.header {{
    text-align:center;
    padding:20px;
    border-bottom:2px solid #FFD700;
}}
.title {{
    color:#FFD700;
    font-size:20px;
    font-weight:bold;
}}
.content {{
    padding:25px;
}}
.card {{
    background:#1c1c1c;
    padding:15px;
    border-radius:8px;
    margin:20px 0;
}}
.button {{
    display:inline-block;
    background:#FFD700;
    color:#000;
    padding:12px 20px;
    border-radius:6px;
    text-decoration:none;
}}
.footer {{
    text-align:center;
    padding:15px;
    font-size:12px;
    color:#aaa;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">
<img src="{LOGO_URL}" width="80">
<div class="title">🏆 UNI6CTF Certificate</div>
</div>

<div class="content">

<p>Dear <b>{row['Full Name']}</b>,</p>

<p>Congratulations on participating in UNI6CTF 1.0!</p>

<div class="card">
<b>Username:</b> {row['Username']}<br>
<b>Team:</b> {row['Team Name']}<br>
<b>Rank:</b> {row['Rank']}<br>
<b>Points:</b> {row['Points']}
</div>

<a href="{BASE_URL}{cert_id}" class="button">
🔍 Verify Certificate
</a>

<div style="margin-top:20px;">
<img src="{CERT_BASE_URL}{row['Username']}.png" width="100%">
</div>

<p style="margin-top:20px;">
UNI6CTF is a cybersecurity platform focused on real-world hacking skills.
</p>

<p>
Best Regards,<br>
UNI6CTF Team
</p>

</div>

<div class="footer">
🌐 uni6ctf.online<br>
📧 organizers@uni6ctf.online
</div>

</div>

<img src="{TRACK_URL}{cert_id}" width="1" height="1">

</body>
</html>
"""

                # ✅ TEXT + HTML (IMPORTANT FIX)
                msg.set_content("Your certificate is attached.")
                msg.add_alternative(html_content, subtype='html')

                # ===============================
                # 📎 ATTACH CERTIFICATE
                # ===============================
                with open(file_path, 'rb') as f:
                    msg.add_attachment(
                        f.read(),
                        maintype='image',
                        subtype='png',
                        filename="certificate.png"
                    )

                # ===============================
                # 🚀 SEND EMAIL
                # ===============================
                server.send_message(msg)

                print(f"✅ Sent: {email}")

                time.sleep(1)  # prevent SMTP timeout

            except Exception as e:
                print(f"❌ Failed: {email} → {e}")

    print("\n✅ All Emails Sent Successfully!")

except Exception as e:
    print("❌ SMTP Error:", e)

