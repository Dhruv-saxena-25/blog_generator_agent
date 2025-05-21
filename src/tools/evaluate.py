from src.state.blogstate import BlogState
from langchain_core.messages import AIMessage

def evaluate_content(state: BlogState, llm):
    content = state["blog_content"][-1].content
    feedback = state["reviewed_content"][-1].content
    
    prompt = f"""Evaluate blog content against editorial feedback (Pass/Fail):
    Content: {content}
    Feedback: {feedback}
    Answer only Pass or Fail:"""
    response = llm.invoke(prompt)
    
    verdict = response.content.strip().upper()
    state["is_blog_ready"] = "Pass" if "PASS" or "Pass" in verdict else "Fail"
    state["reviewed_content"].append(AIMessage(content=f"Verdict: {response.content}"))
    return state