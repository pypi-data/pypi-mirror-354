# 🗺️ IAM Map — AWS IAM Graph Analyzer

A powerful CLI to explore IAM users, groups, and policies across AWS accounts — with AI-powered natural language support via **Ollama + Mistral**.

---

## 💊 Choose Your Path

### 🔵 The Blue Pill — Just Install and Play

1. **Install the package:**

```bash
pip install iam-map
````

2. **Export a graph:**

```bash
iam-map export-graph --profile my-account
```

3. **Start ollama:**

```bash
ollama run mistral
```

4. **Ask questions with natural language:**

```bash
iam-map shell --profile my-account
```

Example prompts:

```
💬 > Who has EC2 or Lambda access but not S3?
💬 > Which users are in dev or test group with full Admin rights?
```

That’s it. Explore your IAM relationships like never before.

---