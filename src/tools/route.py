from src.state.blogstate import BlogState

def route_based_on_verdict(state: BlogState):
    return "Pass" if state['is_blog_ready'] == "Pass" else "Fail"

