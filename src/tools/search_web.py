from langchain_community.tools.tavily_search import TavilySearchResults
from src.state.blogstate import BlogState
from src.utils.language_check import is_english

def search_web(state: BlogState):
    
    search_tool = TavilySearchResults(max_results= 3)
    
    ## Create search query with date and recent news
    query= f"Latest data on {state['topic']}"
    
    ## Execute the search
    search_results= search_tool.invoke({'query': query})
    
    # Filter out YouTube results and non-English content
    filtered_results = []
    
    for result in search_results:
        if "youtube.com" not in result.get("url", "").lower():
            ## Check the content is in english
            content = result.get("content", "") + " " + result.get("title", "")
            if is_english(content):
                filtered_results.append(result)
    
    return {
        "search_results": [
            {
                "role": "system",
                "content": f"{result['title']}\n{result['content']}\n(Source: {result['url']})"
            }
            for result in filtered_results
        ]
    }