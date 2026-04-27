import streamlit as st
import pandas as pd
import json
import time
from app.graph.builder import build_graph

# Page configuration for a premium feel
st.set_page_config(
    page_title="Extractor AI | LangGraph",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #121212 0%, #1a1a1a 100%);
    }
    
    /* Title styling */
    .title-text {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    /* Subtitle */
    .subtitle-text {
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Card-like containers */
    div.stTextArea textarea {
        background-color: #262730 !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        color: #eee !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #FF512F 0%, #DD2476 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(221, 36, 118, 0.4);
        color: white;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0e1117;
        border-right: 1px solid #333;
    }
    
    /* Success metrics/tables */
    [data-testid="stTable"] {
        background-color: #1e1e1e;
        border-radius: 10px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title & Header
st.markdown('<h1 class="title-text">Extractor AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Structured Data Extraction powered by LangGraph & Gemini</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.title("Settings")
    st.info("Define the schema for extraction. The AI will strictly follow this structure.")
    
    default_schema = {
        "name": {},
        "age": {},
        "city": {},
        "profession": {},
        "salary": {},
        "skills": {}
    }
    
    schema_str = st.text_area(
        "Extraction Schema (JSON)",
        value=json.dumps(default_schema, indent=2),
        height=350
    )
    
    try:
        schema = json.loads(schema_str)
        st.success("✅ Schema Validated")
    except Exception as e:
        st.error(f"❌ Invalid JSON: {e}")
        schema = None

    st.markdown("---")
    st.markdown("### About")
    st.caption("This demo uses a multi-agentic workflow to extract, validate, and repair structured data from unstructured text.")

# Main Layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📝 Input Content")
    paragraph = st.text_area(
        "Enter paragraph text here:",
        placeholder="e.g., Sarah is a 28-year-old UX designer based in San Francisco. She earns $120k annually and specializes in Figma and React.",
        height=250,
        label_visibility="collapsed"
    )
    
    extract_btn = st.button("🚀 Run Extraction Pipeline")

with col2:
    st.subheader("📊 Extraction Result")
    
    if extract_btn:
        if not paragraph:
            st.warning("Please enter some text to extract.")
        elif not schema:
            st.warning("Please provide a valid JSON schema.")
        else:
            with st.status("🏗️ Agentic Workflow in Progress...", expanded=True) as status:
                try:
                    # Initialize graph
                    st.write("Initializing LangGraph engine...")
                    graph = build_graph()
                    
                    input_data = {
                        "paragraph": paragraph,
                        "schema": schema,
                        "iteration_count": 0 # Initialize iteration count if not handled by input node
                    }
                    
                    # Stream execution for visual feedback
                    steps_container = st.container()
                    
                    final_result = None
                    
                    # Track nodes
                    node_icons = {
                        "input": "📥",
                        "extract": "🔍",
                        "validate": "🛡️",
                        "repair": "🔧",
                        "output": "📤"
                    }
                    
                    # Use invoke for simplicity but we'll simulate the "feeling" of steps
                    # because we want to show the final table which is in the state.
                    
                    # Run the graph
                    start_time = time.time()
                    
                    # We stream to show progress
                    for step in graph.stream(input_data):
                        for node_name, state_update in step.items():
                            icon = node_icons.get(node_name, "⚙️")
                            st.write(f"{icon} **{node_name.capitalize()} Agent** completed its task.")
                            
                            # If it's the repair node, show a special message
                            if node_name == "repair":
                                st.info("Repaired missing fields based on context.")
                    
                    # Get final result
                    final_result = graph.invoke(input_data)
                    
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    status.update(label=f"✅ Completed in {duration:.2f}s", state="complete", expanded=False)
                    
                    # Display the results
                    if "final_table" in final_result:
                        st.table(final_result["final_table"])
                        
                        with st.expander("🔍 View Raw JSON Output"):
                            st.json(final_result["extracted_data"])
                            
                        st.success(f"Successfully extracted {len(final_result['extracted_data'])} fields.")
                    else:
                        st.error("The workflow completed but no final table was generated.")
                        
                except Exception as e:
                    status.update(label="❌ Error occurred", state="error")
                    st.error(f"An error occurred during extraction: {str(e)}")
                    st.exception(e)
    else:
        st.info("Enter text and click 'Run Extraction Pipeline' to see results here.")

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666;">Built with LangGraph, Streamlit, and Google Gemini</div>', 
    unsafe_allow_html=True
)
