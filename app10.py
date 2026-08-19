from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("output/final_data10.csv")

@app.route("/verify")
def verify():
    cert_id = request.args.get("id")

    result = df[df['Certificate ID'] == cert_id]

    if not result.empty:
        return render_template("valid.html", data=result.iloc[0])
    else:
        return render_template("invalid.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)