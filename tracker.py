from flask import Flask, request

app = Flask(__name__)

@app.route("/track")
def track():
    cert_id = request.args.get("id")
    print(f"📩 Email opened: {cert_id}")
    return "", 204

app.run(port=5000)