from typing_extensions import TypedDict
from typing import Annotated, List, Dict, Any
from langgraph.graph import add_messages


# Define BlogState TypedDict

class BlogState(TypedDict):
    topic: str
    title: str
    search_results: Annotated[List[Dict[str, Any]], add_messages]
    blog_content: Annotated[List, add_messages]
    reviewed_content: Annotated[List, add_messages]
    is_blog_ready: str
    