import asyncio
import streamlit as st

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm import RequestParams

# --- Page Configuration ---
st.set_page_config(page_title="Browser MCP Agent", page_icon="🌐", layout="wide")

# --- Custom CSS for Styling ---
st.markdown(
    """
<style>
    /* Main app container with gradient background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #1a1a2e, #16213e, #0f3460) !important;
    }

    /* General text color */
    body {
        color: #FAFAFA;
    }

    /* Main header */
    .main-header {
        font-size: 2.8rem; /* Slightly larger */
        font-weight: bold;
        color: #E0E0E0; /* Lighter color for contrast */
        text-align: center;
        margin-bottom: 1.5rem; /* More space */
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* Subtle shadow */
    }

    /* Subheader/description styling */
    .description {
        text-align: center;
        color: #B0B0B0;
        margin-bottom: 2.5rem;
        font-size: 1.1rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
        color: #FAFAFA;
    }
    [data-testid="stSidebar"] h3 {
        color: #FFFFFF;
        font-weight: bold;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #A0A0A0;
    }

    /* Text Area for command input */
    [data-testid="stTextArea"] textarea {
        background-color: #2A2A2A;
        color: #FFFFFF;
        border: 1px solid #4A4A4A;
        border-radius: 8px; /* Slightly more rounded */
        font-size: 1.05rem;
        padding: 12px;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3); /* Inner shadow */
    }

    /* Run button */
    .stButton button {
        background-color: #007BFF; /* Blue for primary action */
        color: #FFFFFF;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.8rem 1.5rem; /* Slightly larger padding */
        width: 100%;
        border: none;
        transition: background-color 0.3s ease; /* Smooth transition */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); /* Outer shadow */
    }
    .stButton button:hover {
        background-color: #0056b3;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
    }

    /* Response area */
    .response-container {
        margin-top: 2.5rem;
        background-color: rgba(42, 42, 42, 0.8); /* Semi-transparent background */
        padding: 1.8rem;
        border-radius: 10px;
        border: 1px solid #4A4A4A;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4); /* Shadow for depth */
    }
    .response-container h3 {
        color: #FFFFFF;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- Main App Layout ---

# Title and description
st.markdown("<h1 class='main-header'>🌐 Browser MCP Agent</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='description'>Interact with a powerful web browsing agent that can navigate and interact with websites</p>",
    unsafe_allow_html=True,
)

# Setup sidebar with example commands
with st.sidebar:
    st.markdown("### Example Commands")

    st.markdown("**Navigation**")
    st.markdown("- Go to github.com/priyank766 and rate the main page")

    st.markdown("___")
    st.caption("Note: The agent uses Playwright to control a real browser.")

# Query input
query = st.text_area(
    "Your Command",
    placeholder="Ask the agent to navigate to websites and interact with them",
    label_visibility="collapsed",
)

# Initialize app and agent
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.mcp_app = MCPApp(name="streamlit_mcp_agent")
    st.session_state.mcp_context = None
    st.session_state.mcp_agent_app = None
    st.session_state.browser_agent = None
    st.session_state.llm = None
    st.session_state.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(st.session_state.loop)
    st.session_state.is_processing = False


# Setup function that runs only once
async def setup_agent():
    if not st.session_state.initialized:
        try:
            # Create context manager and store it in session state
            st.session_state.mcp_context = st.session_state.mcp_app.run()
            st.session_state.mcp_agent_app = (
                await st.session_state.mcp_context.__aenter__()
            )

            # Create and initialize agent
            st.session_state.browser_agent = Agent(
                name="browser",
                instruction="""You are a helpful web browsing assistant that can interact with websites using playwright.
                    - Navigate to websites and perform browser actions (click, scroll, type)
                    - Extract information from web pages 
                    - Take screenshots of page elements when useful
                    - Provide concise summaries of web content using markdown
                    - Follow multi-step browsing sequences to complete tasks
                    
                Respond back with a status update on completing the commands.""",
                server_names=["playwright"],
            )

            st.session_state.llm = await st.session_state.browser_agent.attach_llm(
                GoogleAugmentedLLM
            )

            # Initialize agent and attach LLM
            await st.session_state.browser_agent.initialize()

            # List tools once
            logger = st.session_state.mcp_agent_app.logger
            tools = await st.session_state.browser_agent.list_tools()
            logger.info("Tools available:", data=tools)

            # Mark as initialized
            st.session_state.initialized = True
        except Exception as e:
            return f"Error during initialization: {str(e)}"
    return None


# Main function to run agent
async def run_mcp_agent(message):
    try:
        # Make sure agent is initialized
        error = await setup_agent()
        if error:
            return error

        # Generate response without recreating agents
        # Switch use_history to False to reduce the passed context
        result = await st.session_state.llm.generate_str(
            message=message,
            request_params=RequestParams(use_history=True, maxTokens=10000),
        )
        return result
    except Exception as e:
        return f"Error: {str(e)}"


# Defaults
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False
if "last_result" not in st.session_state:
    st.session_state.last_result = None


def start_run():
    st.session_state.is_processing = True


# Button (use a callback so the click just flips state)
st.button(
    "🚀 Run Command", type="primary", use_container_width=True, on_click=start_run
)

# If we’re in a processing run, do the work now
if st.session_state.is_processing:
    with st.spinner("Processing your request..."):
        result = st.session_state.loop.run_until_complete(run_mcp_agent(query))
    # persist result across the next rerun
    st.session_state.last_result = result
    # unlock the button and refresh UI
    st.session_state.is_processing = False
    st.rerun()

# Render the most recent result (after the rerun)
if st.session_state.last_result:
    with st.container():
        st.markdown("<div class='response-container'>", unsafe_allow_html=True)
        st.markdown("### Response")
        st.markdown(st.session_state.last_result, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
