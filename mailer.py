
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
                msg['Subject'] = "🎉🎉 UNI6CTF 1.0 Certificate 🎉🎉"
                msg['From'] = EMAIL
                msg['To'] = email

                cert_id = row.get('Certificate ID', 'N/A')

                # ===============================
                # 📩 HTML EMAIL
                # ===============================
                html_content = f"""<!DOCTYPE html>
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">
<style>
    body {{
        margin:0;
        padding:0;
        background:#0f172a;
        font-family: Arial, sans-serif;
        color:#f3f4f6;
    }}

    .container {{
        max-width:600px;
        margin:20px auto;
        background:#111827;
        border-radius:12px;
        overflow:hidden;
        border:1px solid #1f1f1f;
        box-shadow:0 0 20px rgba(0,0,0,0.6);
    }}

    .header {{
        text-align:center;
        padding:25px;
        background:linear-gradient(135deg, #020617, #0f172a);
        border-bottom:2px solid #facc15;
    }}

    .logo {{
        width:90px;
        margin-bottom:10px;
        filter: brightness(1.2);
         border-radius:50%;
    object-fit:cover;
    border:2px solid #facc15;
    }}

    .title {{
        font-size:22px;
        color:#facc15 !important;
        font-weight:bold;
        letter-spacing:0.5px;
        text-shadow:0 0 8px rgba(250,204,21,0.5);
    }}

    .content {{
        padding:28px;
        font-size:14px;
        line-height:1.7;
        color:#f3f4f6 !important;
    }}

    .highlight {{
        color:#facc15;
        font-weight:bold;
    }}

    .card {{
        background:#1e293b;
        padding:16px;
        border-radius:10px;
        margin:22px 0;
        border:1px solid #2a2a2a;
        box-shadow:0 0 10px rgba(0,0,0,0.4);
    }}

    .button {{
        display:inline-block;
        background:linear-gradient(135deg, #facc15, #eab308);
        color:#000000 !important;
        padding:12px 22px;
        border-radius:8px;
        text-decoration:none;
        font-weight:bold;
        margin-top:20px;
        box-shadow:0 0 10px rgba(250,204,21,0.4);
    }}

    .button:hover {{
        background:#fde047;
    }}

    .preview {{
        margin-top:25px;
        text-align:center;
    }}

    .preview img {{
        width:100%;
        border-radius:10px;
        border:1px solid #2a2a2a;
        box-shadow:0 0 12px rgba(0,0,0,0.5);
    }}

    .footer {{
        text-align:center;
    padding:18px;
    font-size:12px;
    color:#9ca3af !important;
    border-top:1px solid #1f2937;
    background:#020617;
    }}
</style>

</head>

<body>

<div class="container">

    <!-- HEADER -->
    <div class="header">
        <img src="cid:logo" class="logo">
        <div class="title">🏆 UNI6CTF 1.0 Certificate</div>
    </div>

    <!-- CONTENT -->
    <div class="content">

        <p>Dear <span class="highlight">{row['Full Name']}</span>,</p>

        <p>
        successfully completed participation in 
        <span class="highlight">UNI6CTF 1.0 – Capture The Flag Competition</span>.
        </p>

        <!-- DETAILS -->
        <div class="card">
            <b>Username:</b> {row['Username']}<br>
            <b>Team:</b> {row['Team Name']}<br>
            <b>Rank:</b> {row['Rank']}<br>
            <b>Points:</b> {row['Points']}
        </div>

        <p>Your certificate has been generated and is attached</p>

        <!-- BUTTON -->
        <a href="{BASE_URL}{row['Certificate ID']}" class="button">
            🔍 Verify Certificate
        </a>

        <!-- PREVIEW -->
        <div class="preview">
            <p style="color:#facc15;">Certificate Preview</p>
            <img src="https://verify.uni6ctf.online/certificates/{row['Username']}.png">
        </div>

        <p style="margin-top:25px;">
        UNI6CTF is a student-driven cybersecurity initiative focused on developing real-world hacking skills, organizing CTF competitions, and building a strong cybersecurity community.
        </p>

        <p>
        We look forward to your participation in future competitions 🚀
        </p>

        <br>

        <p>
        Best Regards,<br><br>

        <b style="color:#ffffff;">Madhuresh Kumar Jha</b><br>
        CEO & Founder, UNI6CTF<br><br>

        <b style="color:#ffffff;">Krish Pathania</b><br>
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
"""

                # ✅ TEXT + HTML (IMPORTANT FIX)
                msg.set_content("Your certificate is attached.")
                msg.add_alternative(html_content, subtype='html')
                with open("UNI6CTF_logo.png", "rb") as f:
                    msg.get_payload()[1].add_related(
                        f.read(),
                        maintype="image",
                        subtype="png",
                        cid="logo"
                    )
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

