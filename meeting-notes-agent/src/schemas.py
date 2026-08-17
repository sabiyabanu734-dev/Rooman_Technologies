from typing import List, Optional
from pydantic import BaseModel, Field


class ActionItem(BaseModel):
    task: str = Field(description="Actionable summary of the assigned task.")
    owner: str = Field(description="Name of the assigned individual. 'Unassigned' if unspecified.")
    due_date: Optional[str] = Field(description="Target completion date in YYYY-MM-DD or specific timeline. 'TBD' if unstated.")
    priority: str = Field(description="Priority rating: High, Medium, or Low.")


class MeetingSummary(BaseModel):
    title: str = Field(description="Descriptive name of the meeting.")
    overview: str = Field(description="1-2 sentence core overview of the conversation.")
    key_decisions: List[str] = Field(description="Explicit decisions confirmed by participants.")
    discussion_points: List[str] = Field(description="Main topic areas discussed.")
    action_items: List[ActionItem] = Field(description="List of extracted action items.")