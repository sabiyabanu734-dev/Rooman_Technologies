# Architecture & Tradeoff Notes

## Model Selection & Approach
- **Google GenAI SDK (`google-genai`)**: Uses `gemini-3.6-flash` for fast, cost-effective transcript processing and structured output generation.
- **Native Pydantic Schema Enforcement**: Uses `types.GenerateContentConfig` with `response_mime_type="application/json"` and `response_schema=MeetingSummary` to force deterministic JSON responses directly from the model.

## Validation Strategy
- **Pydantic Model Parsing**: Responses are validated using `MeetingSummary.model_validate_json()`.
- **Fallback Defaults**: Handled via schema prompts (`"Unassigned"` for missing task owners, `"TBD"` for absent due dates).

## Known Failure Cases & Limitations
1. **Implicit Mentions**: If an action item is introduced using pronouns (e.g., "I'll handle that") without explicit speaker labels in the text, assignment accuracy decreases.
2. **Relative Dates**: Relative timelines (e.g., "by next Friday") are extracted as stated. Converting to exact calendar dates is most accurate when the meeting date is provided in the transcript context.