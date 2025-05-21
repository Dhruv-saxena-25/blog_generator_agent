from src.state.blogstate import BlogState
from langchain_core.messages import AIMessage


def review_content(state: BlogState, llm):
    content= state['blog_content'][-1].content
    prompt = f"""Critically review this blog content:
    - Clarity & Structure
    - Grammar & Style
    - SEO optimization
    - Reader engagement
    Provide specific improvement suggestions. Content:\n{content}"""
    
    feedback = llm.invoke(prompt)
    state['reviewed_content'].append(AIMessage(content=feedback.content))
    return state

    
    