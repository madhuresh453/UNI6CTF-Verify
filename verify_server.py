from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder=".")

DATA_FILE = "output/final_data.csv"

# ===============================
# 📂 LOAD DATA (SAFE)
# ===============================
def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        print("❌ No data file found")
        return pd.DataFrame()

    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()
    return df


# ===============================
# 🔍 VERIFY ROUTE
# ===============================
@app.route("/verify")
def verify():
    cert_id = request.args.get("id")

    if not cert_id:
        return "❌ Invalid request (no ID)"

    df = load_data()

    if df.empty:
        return "❌ No certificate data available"

    # ✅ CHECK COLUMN EXISTS
    if 'Certificate ID' not in df.columns:
        return "❌ Invalid data format"

    result = df[df['Certificate ID'] == cert_id]

    if result.empty:
        return render_template("invalid.html")

    row = result.iloc[0]

    return render_template("valid.html", data=row)


# ===============================
# 🏠 HOME PAGE (OPTIONAL)
# ===============================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Verify Certificate</title>

<style>
body {
    margin:0;
    font-family:'Segoe UI', Arial;
    background: radial-gradient(circle at top, #111, #000);
    color:white;
    text-align:center;
}

/* CONTAINER */
.container {
    margin-top:120px;
}

/* LOGO */
.logo {
    font-size:14px;
    color:#aaa;
    margin-bottom:10px;
}

/* TITLE */
.title {
    font-size:34px;
    font-weight:bold;
}

.subtitle {
    margin-top:10px;
    color:#aaa;
    font-size:14px;
}

/* SEARCH BOX */
.search-box {
    margin-top:30px;
}

input {
    padding:14px;
    width:280px;
    border-radius:10px;
    border:none;
    outline:none;
    font-size:15px;
}

/* BUTTON */
button {
    padding:14px 22px;
    background:#FFD700;
    border:none;
    border-radius:10px;
    font-weight:bold;
    margin-left:10px;
    cursor:pointer;
    transition:0.2s;
}

button:hover {
    background:#ffcc00;
    transform:scale(1.05);
}

/* CARD */
.card {
    margin-top:50px;
    display:inline-block;
    padding:20px;
    background:#121212;
    border-radius:12px;
    border:1px solid #222;
    box-shadow:0 0 30px rgba(255,215,0,0.1);
}

/* RECENT */
.recent {
    margin-top:15px;
    font-size:13px;
    color:#aaa;
}

.recent span {
    color:#FFD700;
    cursor:pointer;
}

/* FOOTER */
.footer {
    position:fixed;
    bottom:10px;
    width:100%;
    font-size:12px;
    color:#666;
}
</style>
</head>

<body>

<div class="container">

    <!-- BRAND -->
    <div class="logo">UNI6CTF • Cybersecurity Excellence Platform</div>

    <!-- TITLE -->
    <div class="title">🔍 Verify Certificate</div>

    <div class="subtitle">
        Enter your certificate ID to verify authenticity
    </div>

    <!-- SEARCH -->
    <div class="search-box">
        <form action="/verify">
            <input type="text" name="id" placeholder="UNI6CTF-2026-0001" required>
            <button type="submit">Verify</button>
        </form>
    </div>

    <!-- CARD -->
    <div class="card">
        🟢 Secure Verification System <br>
        🔐 QR & Hash Protected Certificates <br>
        🌐 Trusted by UNI6CTF
    </div>

    <!-- RECENT (OPTIONAL) -->
    <div class="recent">
        Try: 
        <span onclick="fill('UNI6CTF-2026-0001')">0001</span> • 
        <span onclick="fill('UNI6CTF-2026-0002')">0002</span> • 
        <span onclick="fill('UNI6CTF-2026-0003')">0003</span>
    </div>

</div>

<div class="footer">
© UNI6CTF | Certificate Verification Portal
</div>

<script>
function fill(val){
    document.querySelector("input").value = val;
}
</script>

</body>
</html>
"""


@app.route("/cert/<username>")
def cert(username):
    return f"/output/certificates/{username}.png"


from flask import send_from_directory

@app.route('/certificates/<path:filename>')
def serve_certificate(filename):
    return send_from_directory('output/certificates', filename)


from flask import send_file

@app.route("/secure/<cert_id>")
def secure_download(cert_id):
    df = load_data()
    row = df[df['Certificate ID'] == cert_id]

    if row.empty:
        return "Unauthorized"

    file_path = row.iloc[0]['File']
    return send_file(file_path, as_attachment=True)

@app.route("/user/<username>")
def profile(username):
    df = load_data()
    user = df[df['Username'] == username]

    return user.to_html()


@app.route("/leaderboard")
def leaderboard():
    df = load_data()
    df = df.sort_values(by="Points", ascending=False)
    return df.head(10).to_html()

@app.route("/track/<cert_id>")
def track(cert_id):
    print("Scanned:", cert_id)
    return ""



# ===============================
# 🚀 RUN SERVER
# ===============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)