from typing import TypedDict, Annotated
import operator

# The shared "notepad" for the agents
class AgencyState(TypedDict):
    topic: str
    research_notes: str
    draft: str
    feedback: str
    revision_count: int