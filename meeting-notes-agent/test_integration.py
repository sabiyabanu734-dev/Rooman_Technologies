import pytest
from src.agent import MeetingNotesAgent
from src.schemas import MeetingSummary


@pytest.mark.integration
def test_live_api_call():
    sample_text = "Alice agreed to complete the database schema design by tomorrow. Bob will review it."
    agent = MeetingNotesAgent()
    result = agent.process_transcript(sample_text)

    assert isinstance(result, MeetingSummary)
    assert len(result.action_items) >= 1