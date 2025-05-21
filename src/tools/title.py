from src.state.blogstate import BlogState

def generate_title(state: BlogState, llm):
    
    prompt = f"""Generate compelling blog title options about {state["topic"]} that are:
    - SEO-friendly
    - Attention-grabbing
    - Between 6-12 words
    Return only the title, no explanation or extra text."""
    response = llm.invoke(prompt)
    state['title'] = response.content.split("\n")[0].strip('"')
    return state


