from langgraph.graph import add_messages, StateGraph, END, START
from src.state.blogstate import BlogState
from src.tools.title import generate_title
from src.tools.search_web import search_web
from src.tools.content import generate_content
from src.tools.review import review_content
from src.tools.evaluate import evaluate_content
from src.tools.route import route_based_on_verdict


def init_graph(llm):
    builder = StateGraph(BlogState)
    builder.add_node("title_generator", lambda state: generate_title(state, llm)) ## Generate Title
    builder.add_node("search_web", search_web) ## Search Web using Tavily based in the topic
    builder.add_node("content_generator", lambda state: generate_content(state, llm)) ## Generate Content using the output of title_generator and search_web
    builder.add_node("content_reviewer", lambda state: review_content(state, llm)) ## Review Content and generate feedback
    builder.add_node("quality_check", lambda state: evaluate_content(state, llm)) ## Validate the content based on feedback and generate verdict
  
    builder.add_edge(START, "title_generator")
    builder.add_edge(START, "search_web")
    builder.add_edge("title_generator", "content_generator")
    builder.add_edge("search_web", "content_generator")
    builder.add_edge("content_generator", "content_reviewer")
    builder.add_edge("content_reviewer", "quality_check")
    
    builder.add_conditional_edges(
        "quality_check",
        route_based_on_verdict,
        {"Pass": END, "Fail": "content_generator"}
    )
    return builder.compile()