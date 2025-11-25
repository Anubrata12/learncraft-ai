from typing import Dict, Any
from google.adk.tools.tool_context import ToolContext


# Store topic_name
def save_topic(tool_context: ToolContext, topic_name: str) -> Dict[str, Any]:
    tool_context.state["app:topic_name"] = topic_name
    return {"status": "saved"}


# Retrieve topic_name
def load_topic(tool_context: ToolContext) -> Dict[str, Any]:
    topic = tool_context.state.get("app:topic_name", None)
    return {"topic_name": topic}
