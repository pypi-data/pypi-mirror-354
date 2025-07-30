# errorex

**Explain errors better.**

`errorex` is a Python library that automatically explains and logs runtime errors in your code by capturing:
- Code traceback (excluding library noise)
- Local variable snapshots
- Suggestions for common errors
- LLM-ready GPT prompts

## 💡 Example

```python
from errorex import explain_errors

...

@explain_errors(log=True, suggest=True)
def run():
    df = pd.read_csv("somefile.csv")
    model.fit(df[['feature']], df['label'])  # Will fail if NaNs or mismatch

run()

🛠 Features
📍 User-focused Tracebacks: Filters out noisy frames from libraries.

🧠 Local Variable Snapshot: Captures all in-scope variables at the error line.

💡 Error Suggestions: Auto-suggests common fixes (e.g., NaNs, shape mismatches).

🤖 LLM Debug Prompt: Structured error message ready to paste into ChatGPT.

📝 Markdown Report Logging: Saves error reports to logs/error_report_<timestamp>.md.


📦 Installation
bash
Copy
Edit
pip install errorex
(Or, if you're developing locally)

bash
Copy
Edit
git clone https://github.com/minalbansal14/errorex.git
cd errorex
pip install -e .
🧪 Tests
bash
Copy
Edit
pytest tests/
🧠 Example Output (Markdown Log)
markdown
Copy
Edit
## ⚠️ Exception:
ValueError: Input y contains NaN

## 📍 Traceback:
- File: `simple_pipeline.py`, Line: 21
  ```python
  model.fit(X, y)
🧠 Local Variables:
y: 0.0, 1.0, NaN

💡 Suggestions:
It looks like your data contains missing values. Try using df.dropna().

🤖 GPT Prompt:
mathematica
Copy
Edit
Here’s the error and variables. How can I fix it?
👤 Author
Created by Minal Bansal
Contributions welcome via issues or PRs.