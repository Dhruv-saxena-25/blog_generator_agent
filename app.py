import streamlit as st
from src.state.blogstate import BlogState
from dotenv import load_dotenv
import os
from src.llm.llms import get_llm
from src.graph.builder import init_graph


# ─── Sidebar inputs 
st.sidebar.header("🤖 LLM Configuration")   

provider = st.sidebar.selectbox("LLM Provider", ["Groq", "Gemini", "OpenAI"])

model_options = {
    "Groq": ["qwen-qwq-32b", "mistral-saba-24b", "llama-3.3-70b-versatile"],
    "Gemini": ["gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-2.0-flash", "gemini-2.5-pro-preview"],
    "OpenAI": ["gpt-4-32k", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]
}

model_name = st.sidebar.selectbox("Model", model_options[provider])

# ─── API Key Input ────────────────────────────────────────────────────────────
api_keys = {}

if provider == "Groq":
    groq_key = st.sidebar.text_input("🔗 Groq API Key", type="password")
    api_keys["GROQ_API_KEY"] = groq_key
    # st.sidebar.markdown("🔑 [Get Groq API Key](https://console.groq.com/keys)")

elif provider == "Gemini":
    google_key = st.sidebar.text_input("🔗 Gemini API Key", type="password")
    api_keys["GEMINI_API_KEY"] = google_key
    # st.sidebar.markdown("🔑 [Get Gemini API Key](https://aistudio.google.com/app/apikey)")

elif provider == "OpenAI":
    openai_key = st.sidebar.text_input("🔗 OpenAI API Key", type="password")
    api_keys["OPENAI_API_KEY"] = openai_key
    # st.sidebar.markdown("🔑 [Get OpenAI API Key](https://platform.openai.com/account/api-keys)")

# ─── Initialize LLM if Key is Provided ───────────────────────────────────────
api_key = api_keys.get(f"{provider.upper()}_API_KEY", "")

# Dynamic help link per provider
api_key_links = {
    "Groq": "https://console.groq.com/keys",
    "Gemini": "https://aistudio.google.com/app/apikey",
    "OpenAI": "https://platform.openai.com/account/api-keys"
}

llm = None
if api_key.strip():
    try:
        llm = get_llm(provider, model_name, api_key)
        st.session_state.llm = llm
        st.sidebar.success(f"✅ LLM Initialized: {model_name}")
    except Exception as e:
        st.error(f"❌ Failed to initialize LLM: {e}")
else:
    st.sidebar.warning(
        f"⚠️ Please enter your {provider} API key to proceed. [Get it here]({api_key_links[provider]})"
    )

    
    
# ─── Tavily API Configuration ────────────────────────────────────────────────
st.sidebar.header("🔍 TAVILY Configuration")

# Ask for Tavily API key
tavily_api_key = st.sidebar.text_input(
    "Tavily API Key:",
    type="password",
    value=st.session_state.get("TAVILY_API_KEY", "")
)

# Save to session and env if provided
if tavily_api_key:
    st.session_state["TAVILY_API_KEY"] = tavily_api_key
    os.environ["TAVILY_API_KEY"] = tavily_api_key
    st.sidebar.success("✅ Tavily API Key Set!")
else:
    st.sidebar.warning("⚠️ Please enter your TAVILY_API_KEY to proceed. [Get it here](https://app.tavily.com/home)")
    

# ─── Reset Session Button ─────────────────────────────────────────────────────
if st.sidebar.button("🔄 Reset Session"):
    # Clear session and environment-stored keys
    st.session_state.clear()
    st.rerun()

# ─── Sidebar: Workflow Diagram ───────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.subheader("🧭 Workflow Overview")
st.sidebar.image("workflow_graph.png", use_container_width=True)
    

# Initialize session state
if 'blog_state' not in st.session_state:
    st.session_state.blog_state = None
if 'graph' not in st.session_state:
    st.session_state.graph = None
if 'graph_image' not in st.session_state:
    st.session_state.graph_image = None


# ─── Main Title & Introduction ───────────────────────────────────────────────
st.title("🚀 CraftAI: Intelligent Blog Builder")

st.markdown("""
### ✨ *Your AI-Powered Blog Writing Companion*

Effortlessly generate, refine, and perfect your blog content using advanced language models.

---

**🔍 Features at a Glance:**  
- ✅ **SEO-Optimized Structure**  
- ✍️ **Grammar & Style Refinement**  
- 🔄 **Interactive Feedback Loops**  
- 🧠 **Multi-Model Support** *(Groq, Gemini, OpenAI)*

---

> 💡 *From first draft to polished post — professional blog creation, made seamless.*
""")

# Blog input UI
topic = st.text_input("Enter your blog topic:", placeholder="Generative AI in Healthcare")
generate_btn = st.button("Generate Blog Post")

if generate_btn:
    if not api_key:
        st.error("Please provide a Groq API key in the sidebar!")
        st.stop()

    if not topic:
        st.error("Please enter a blog topic!")
        st.stop()

    try:
        # Initialize and run graph
        st.session_state.graph = init_graph(llm)
        st.session_state.blog_state = BlogState(
            topic=topic,
            title="",
            search_results=[],
            blog_content=[],
            reviewed_content=[],
            is_blog_ready=""
        )

        # Execute the graph
        final_state = st.session_state.graph.invoke(st.session_state.blog_state)
        st.session_state.blog_state = final_state

        # Display results
        st.success("✅ Blog post generation complete!")
        st.markdown("---")
        st.subheader("📝 Final Blog Post")
        st.markdown(final_state["blog_content"][-1].content)

        st.markdown("---")
        st.subheader("📌 Generated Title")
        st.write(final_state["title"])

        st.markdown("---")
        st.subheader("🌐 Web Search Results")
        st.info(final_state["search_results"][-1].content)

        st.markdown("---")
        st.subheader("🧪 Quality Assurance Report")
        verdict = final_state["is_blog_ready"]
        quality_check = final_state["reviewed_content"][-1].content
        if verdict == "Pass":
            st.success(quality_check)
        else:
            st.warning(quality_check)

        st.markdown("---")
        st.subheader("📊 Generation Summary")
        st.write(f"**Topic:** {final_state['topic']}")
        st.write(f"**Status**: {'✅ Approved' if verdict == 'Pass' else '❌ Needs Revision'}")
        st.write(f"**Review Cycles**: {len(final_state['reviewed_content']) - 1}")

    except Exception as e:
        st.error(f"Error in blog generation: {str(e)}")

        