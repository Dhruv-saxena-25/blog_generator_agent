from src.state.blogstate import BlogState
from langchain_core.messages import AIMessage

def generate_content(state: BlogState, llm):
    
    prompt = f"""Write a comprehensive blog post titled "{state['title']}" and based on the web search results {state['search_results']} with:
    1. Engaging introduction with hook
    2. 3-5 subheadings with detailed content
    3. Practical examples/statistics
    4. Clear transitions between sections
    5. Actionable conclusion
    Style: Professional yet conversational (Flesch-Kincaid 60-70). Use markdown formatting"""
    
    response = llm.invoke(prompt)
    state['blog_content'].append(AIMessage(content= response.content))

    return state
