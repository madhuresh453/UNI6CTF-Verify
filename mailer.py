
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
# ===============================
# ✅ ADD EMAIL SENT COLUMN
# ===============================
if 'Email Sent' not in df.columns:
    df['Email Sent'] = False

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
        
        for i, row in df.iterrows():

            # ❌ SKIP ALREADY SENT
            if row.get('Email Sent') == True:
                print(f"⏩ Skipping {row['Email']} (already sent)")
                continue

            email = str(row['Email']).strip()
            file_path = str(row['File']).strip()
            cert_id = row.get('Certificate ID', 'N/A')

            # 🔍 DEBUG
            print(f"\n➡ Sending to: {email}")
            print(f"➡ File: {file_path}")
            print(f"➡ Cert ID: {cert_id}")

            # ❌ skip if file missing
            if not os.path.exists(file_path):
                print(f"❌ File not found for {email}")
                continue

            try:
                msg = EmailMessage()
                msg['Subject'] = "Your Trivarna 2.0 CTF Certificate Has Arrived 🇮🇳"
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
<meta name="color-scheme" content="light dark">
<meta name="supported-color-schemes" content="light dark">

<style>
    body {{
        margin:0;
        padding:0;
        background:#0f172a;
        font-family:Arial, sans-serif;
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
        background:linear-gradient(135deg,#020617,#0f172a);
        border-bottom:2px solid #facc15;
    }}

    .logo {{
        width:90px;
        margin-bottom:10px;
        filter:brightness(1.2);
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
        background:linear-gradient(135deg,#facc15,#eab308);
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

    .info-box {{
        background:#172033;
        border-left:4px solid #facc15;
        padding:16px;
        border-radius:8px;
        margin:22px 0;
    }}

    .social-box {{
        background:linear-gradient(135deg,#1e293b,#172033);
        padding:18px;
        border-radius:10px;
        margin:22px 0;
        border:1px solid #334155;
        text-align:center;
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

        <div class="title">
            🏆 TRIVARNA 2.0 Certificate
        </div>

    </div>


    <!-- CONTENT -->
    <div class="content">

        <p>
            Dear <span class="highlight">{row['Full Name']}</span>,
        </p>


        <p>
            <b>Trivarna CTF may have wrapped, but what you were part of doesn't end there.</b>
        </p>


        <p>
            Your official <span class="highlight">Trivarna 2.0 certificate</span>
            is attached to this email.
        </p>


        <p>
            This certificate recognizes your participation in the
            <span class="highlight">
                TRIVARNA 2.0 INTERNATIONAL CTF CHAMPIONSHIP
            </span>,
            an international <b>24-hour Capture The Flag championship</b>
            held to mark <span class="highlight">India's 80th Independence Day</span>.
        </p>


        <p>
            Whatever your final standing, you showed up, you competed,
            and you were part of a global field of students, researchers,
            and professionals who spent their Independence Day doing
            exactly what the moment called for:
            <b>defending, exploring, and pushing further.</b>
        </p>


        <!-- PARTICIPANT DETAILS -->
        <div class="card">

            <b>Username:</b> {row['Username']}<br>

            <b>Team:</b> {row['Team Name']}<br>

            <b>Rank:</b> {row['Rank']}<br>

            <b>Points:</b> {row['Points']}

        </div>


        <!-- CERTIFICATE INFORMATION -->
        <div class="info-box">

            <b style="color:#facc15;">
                📜 Your Certificate
            </b>

            <br><br>

            Your certificate is official recognition of your
            participation and can be added to your
            <b>resume, LinkedIn profile, portfolio, or achievements.</b>

            <br><br>

            It is yours to use and share.

        </div>


        <p>
            Your certificate has been generated and is attached
            to this email.
        </p>


        <!-- VERIFY BUTTON -->
        <div style="text-align:center;">

            <a href="{BASE_URL}{row['Certificate ID']}" class="button">
                🔍 Verify Certificate
            </a>

        </div>


        <!-- PREVIEW -->
        <div class="preview">

            <p style="color:#facc15;">
                Certificate Preview
            </p>

            <img src="https://verify.uni6ctf.online/certificates/{row['Username']}.png">

        </div>


        <!-- SPONSOR REWARDS -->
        <div class="info-box">

            <b style="color:#facc15;">
                🎁 Sponsor Rewards
            </b>

            <br><br>

            Sponsor rewards including
            <b>certifications, platform access, vouchers, and more</b>
            will be sent separately in a follow-up email.

            <br><br>

            <b>Please keep an eye on your inbox.</b>

        </div>


        <!-- SOCIAL SHARING -->
        <div class="social-box">

            <p style="color:#facc15; font-size:16px; font-weight:bold;">
                📢 One Small Ask
            </p>

            <p>
                If you're proud of this — and you should be —
                <b>share it!</b>
            </p>

            <p>
                Tag <b>Astitwam</b> and <b>Trivarna CTF</b>
                on LinkedIn or Instagram when you post your certificate.
            </p>

            <p style="color:#cbd5e1;">
                Every share helps the next generation of cyber warriors
                discover this mission the way you did.
            </p>

        </div>


        <!-- EXISTING MESSAGE -->
    


        <p>

            We look forward to your participation in future
            competitions 🚀

        </p>


        <p>

            Thank you for making
            <span class="highlight">Trivarna CTF</span>
            what it was.

            <br><br>

            This is only the beginning of what
            <span class="highlight">Astitwam</span>
            is building.

        </p>


        <br>


        <!-- SIGNATURE -->
        <p>

            Until the next mission,<br><br>

            <b style="color:#ffffff;">
                TEAM ASTITWAM
            </b>

            <br><br>

            📧 astitwamofficials@gmail.com<br>

            🌐 astitwam.in

        </p>

    </div>


    <!-- FOOTER -->
    <div class="footer">

        🌐 https://astitwam.in<br>

        📧 hello@astitwam.in<br><br>

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
                with open("logo.png", "rb") as f:
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
                df.loc[i, 'Email Sent'] = True

                print(f"✅ Sent: {email}")

                time.sleep(1)  # prevent SMTP timeout

            except Exception as e:
                print(f"❌ Failed: {email} → {e}")
    df.to_csv(csv_path, index=False)
    print("\n✅ All Emails Sent Successfully!")

except Exception as e:
    print("❌ SMTP Error:", e)
    
    
    

