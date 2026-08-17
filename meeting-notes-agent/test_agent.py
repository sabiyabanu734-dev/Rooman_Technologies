from unittest.mock import MagicMock, patch
import pytest
from src.agent import MeetingNotesAgent
from src.schemas import MeetingSummary


@patch("src.agent.genai.Client")
def test_agent_parsing_mocked(mock_client_cls):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client

    mock_response = MagicMock()
    mock_response.text = """{
        "title": "Database Schema Planning",
        "overview": "Alice and Bob coordinated database schema work.",
        "discussion_points": [
            "Database schema implementation details",
            "Peer review process"
        ],
        "key_decisions": [
            "Database schema design will be completed by tomorrow."
        ],
        "action_items": [
            {
                "task": "Complete the database schema design",
                "owner": "Alice",
                "due_date": "Tomorrow",
                "priority": "High"
            },
            {
                "task": "Review database schema design",
                "owner": "Bob",
                "due_date": "TBD",
                "priority": "Medium"
            }
        ]
    }"""
    mock_client.models.generate_content.return_value = mock_response

    agent = MeetingNotesAgent()
    sample_text = "Alice agreed to complete the database schema design by tomorrow. Bob will review it."
    result = agent.process_transcript(sample_text)

    assert isinstance(result, MeetingSummary)
    assert result.title == "Database Schema Planning"
    assert len(result.action_items) == 2
    assert result.action_items[0].owner == "Alice"
    assert result.action_items[0].priority == "High"
    assert result.action_items[1].owner == "Bob"