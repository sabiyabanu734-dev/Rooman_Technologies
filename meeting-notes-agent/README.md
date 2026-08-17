```markdown
# Meeting Notes Agent

An AI-powered CLI tool built with Python, Pydantic, and the Google GenAI SDK (`google-genai`) that parses unstructured meeting transcripts and generates validated, structured JSON summaries containing key decisions, discussion points, and prioritized action items.

---

## Features

* **Structured Data Extraction:** Uses Pydantic schemas to enforce strict JSON structure (`title`, `overview`, `discussion_points`, `key_decisions`, `action_items`).
* **Resilient API Retries:** Implements exponential backoff retry logic via `tenacity` to handle transient API issues like `503 Service Unavailable`.
* **Model Fallback:** Automatically cascades across alternative models (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) if high API demand affects the primary model.
* **Mocked Test Suite:** Includes unit tests built with `unittest.mock` to ensure fast offline testing without consuming API quota.

---

## Project Structure

```text
meeting-notes-agent/
├── data/
│   ├── transcripts/      # Raw transcript .txt files
│   └── outputs/          # Generated JSON summary files
├── src/
│   ├── agent.py          # Core MeetingNotesAgent class & retry logic
│   ├── config.py         # Environment variables & model settings
│   └── schemas.py        # Pydantic data models (MeetingSummary, ActionItem)
├── test_agent.py         # Pytest suite with mocked API responses
├── main.py               # CLI entry point
├── README.md             # Project documentation
├── notes.md              # Architecture & troubleshooting notes
└── .env                  # API keys and environment configuration

```

---

## Prerequisites

* **Python 3.10+**
* **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

---

## Step-by-Step Setup Guide

### Step 1: Open Terminal & Navigate to Project Directory

```powershell
cd meeting-notes-agent

```

### Step 2: Create & Activate Virtual Environment

* **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

```


* **macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```



### Step 3: Install Required Dependencies

```powershell
pip install google-genai pydantic pytest tenacity python-dotenv

```

### Step 4: Configure Your Environment File

Create a `.env` file in the project root directory and add your API key:

```env
GEMINI_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY"
DEFAULT_MODEL="gemini-2.5-flash"

```

---

## How to Use (3-Step Workflow)

### Step 1: Add Your Meeting Transcript

Place your text transcript file inside the `data/transcripts/` directory (e.g., `data/transcripts/q3_sync.txt`).

### Step 2: Run the CLI Command

Pass the input transcript file path and desired output JSON file path to `main.py`:

```powershell
python main.py --input data/transcripts/q3_sync.txt --output data/outputs/q3_sync_output.json

```

### Step 3: View the Generated Summary

Display the output JSON directly in your terminal:

* **Windows (PowerShell):**
```powershell
Get-Content data/outputs/q3_sync_output.json

```


* **macOS / Linux:**
```bash
cat data/outputs/q3_sync_output.json

```



---

## Sample Input & Output

### Input Transcript (`data/transcripts/q3_sync.txt`)

```text
Meeting: Q3 Product & Infrastructure Sync
Date: October 14, 2026
Attendees: Sarah (Engineering Lead), Alex (Product Manager), Marcus (DevOps Lead)

Alex: Thanks for joining, everyone. First item on the agenda is the cloud migration. Marcus, how are we looking?
Marcus: We're target-ready for AWS migration, but we need to finalize the database cluster config by Friday. I'll handle that configuration by October 17th.
Sarah: Sounds good. On the feature side, the new reporting dashboard is complete, but QA flagged two edge cases in export formats. I'll assign David to patch those by next Tuesday, October 20th.
Alex: Great. Did we make a call on the legacy API deprecation timeline?
Sarah: Yes, we agreed to officially deprecate API v1 on November 30th and notify external developers by the end of this week.
Alex: Perfect. I'll draft and send out the developer announcement email by October 16th.

```

### Output JSON (`data/outputs/q3_sync_output.json`)

```json
{
  "title": "Q3 Product & Infrastructure Sync",
  "overview": "The team aligned on AWS database cluster readiness, fixing dashboard QA export bugs, deprecating API v1 by late November, and developer communications.",
  "discussion_points": [
    "AWS migration progress and database cluster configuration requirements",
    "QA edge cases in reporting dashboard export formats",
    "Legacy API v1 deprecation timeline and developer communication strategy"
  ],
  "key_decisions": [
    "Officially deprecate API v1 on November 30, 2026",
    "Notify external developers regarding API v1 deprecation by the end of the current week"
  ],
  "action_items": [
    {
      "task": "Draft and send out developer announcement email regarding API v1 deprecation",
      "owner": "Alex",
      "due_date": "October 16, 2026",
      "priority": "High"
    },
    {
      "task": "Finalize database cluster configuration for AWS migration",
      "owner": "Marcus",
      "due_date": "October 17, 2026",
      "priority": "High"
    },
    {
      "task": "Patch export format edge cases in reporting dashboard",
      "owner": "David",
      "due_date": "October 20, 2026",
      "priority": "High"
    }
  ]
}

```

---

## Running Unit Tests

Run the offline unit test suite to verify agent logic without hitting live API endpoints or using quota:

```powershell
pytest test_agent.py

```

```

```