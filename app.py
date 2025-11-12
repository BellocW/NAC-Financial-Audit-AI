from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def audit_csv(file):
    df = pd.read_csv(file)
    issues = []

    # Check for duplicate entries
    duplicates = df[df.duplicated()]
    if not duplicates.empty:
        issues.append(f"Duplicate entries found: {len(duplicates)}")

    # Check for missing acquittals
    missing_acq = df[df['Acquittal'].isnull()]
    if not missing_acq.empty:
        issues.append(f"Missing acquittals: {len(missing_acq)}")

    return issues

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csvfile"]
        issues = audit_csv(file)
        return render_template("index.html", issues=issues)
    return render_template("index.html", issues=None)

if __name__ == "__main__":
    app.run(debug=True)
