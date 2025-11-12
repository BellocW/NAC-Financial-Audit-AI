from flask import Flask, render_template, request
import pandas as pd
import openai  # Optional, for AI summaries

app = Flask(__name__)

# Optional: Set your OpenAI API key
# openai.api_key = "YOUR_OPENAI_API_KEY"

def audit_csv(file):
    df = pd.read_csv(file)
    issues = []

    # 1. Duplicate entries
    duplicates = df[df.duplicated()]
    if not duplicates.empty:
        issues.append(f"Duplicate entries found: {len(duplicates)}")

    # 2. Missing acquittals
    if 'Acquittal' in df.columns:
        missing_acq = df[df['Acquittal'].isnull()]
        if not missing_acq.empty:
            issues.append(f"Missing acquittals: {len(missing_acq)}")
    else:
        issues.append("Column 'Acquittal' not found in CSV")

    # 3. Suspense account check (example)
    if 'Account' in df.columns and 'Balance' in df.columns:
        suspense = df[(df['Account'] == 'Suspense') & (df['Balance'] != 0)]
        if not suspense.empty:
            issues.append(f"Suspense account out of balance: {suspense['Balance'].sum()}")

    return issues

# Optional AI summary function
def generate_ai_summary(issues):
    if not issues:
        return "No issues detected. All accounts look clean."
    # Simple GPT prompt
    prompt = "Summarize these audit issues in a professional internal audit report tone:\n"
    for issue in issues:
        prompt += "- " + issue + "\n"
    
    # Call OpenAI API (uncomment if you have API key)
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
    """
    # If no API, just return text summary
    return "Audit Summary:\n" + "\n".join(issues)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csvfile"]
        issues = audit_csv(file)
        summary = generate_ai_summary(issues)
        return render_template("index.html", issues=issues, summary=summary)
    return render_template("index.html", issues=None, summary=None)

if __name__ == "__main__":
    app.run(debug=True)
