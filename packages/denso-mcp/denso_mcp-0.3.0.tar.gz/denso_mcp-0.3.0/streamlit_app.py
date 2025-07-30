import asyncio
import logging
import os
import sys
import warnings
from contextlib import asynccontextmanager

import boto3
import streamlit as st
from agno.agent import Agent
from agno.models.aws import Claude
from agno.tools.mcp import MCPTools
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession
from mcp.client.stdio import stdio_client

from sw_mcp.utils import parse_mcp_servers_from_config

# Suppress ResourceWarning for unclosed transports
warnings.filterwarnings(
    "ignore", category=ResourceWarning, message="unclosed transport"
)

# Ensure we use the correct event loop policy on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server_configs = parse_mcp_servers_from_config()

os.environ["AZURE_OPENAI_API_KEY"] = "ab75735c129449b78343771a136adb54"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://admins.openai.azure.com/"

os.environ["AWS_ACCESS_KEY_ID"] = "AKIASD2D73VC4RHXAOPO"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
os.environ["AWS_REGION"] = "ap-northeast-1"


def init_session_state():
    """Initialize Streamlit session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "running" not in st.session_state:
        st.session_state.running = []
    if "current_iteration" not in st.session_state:
        st.session_state.current_iteration = []


def display_chat_messages():
    """Display chat messages in the Streamlit interface"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# Agent functions
async def create_mcp_agent(session):
    """Create and configure MCP Agent"""
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()

    # llm  = AzureOpenAI(id="gpt-4o",azure_deployment="gpt-4o",api_version="2023-05-15")
    llm = Claude(id="anthropic.claude-3-5-sonnet-20240620-v1:0")

    return Agent(
        model=llm,
        tools=[mcp_tools],
        instructions="Based on given input, use the MCP tool.",
        markdown=True,
        show_tool_calls=True,
    )


@asynccontextmanager
async def managed_stdio_client(server_params):
    """Context manager that ensures proper cleanup of stdio client"""
    read, write = None, None
    process = None

    try:
        # Create the stdio client
        async with stdio_client(server_params) as (r, w):
            read, write = r, w
            # Store the process reference if available
            if hasattr(write, "_transport") and hasattr(write._transport, "_proc"):
                process = write._transport._proc

            yield read, write

    except Exception as e:
        logger.error(f"Error in stdio client: {e}")
        raise
    finally:
        # Ensure proper cleanup
        try:
            # Close the streams if they exist
            if write and hasattr(write, "close"):
                write.close()
            if read and hasattr(read, "close"):
                read.close()

            # Give the process a moment to clean up
            await asyncio.sleep(0.1)

            # Terminate the process if it's still running
            if process:
                try:
                    process.terminate()
                    # Wait for process to terminate
                    await asyncio.wait_for(
                        asyncio.create_task(process.wait()), timeout=2.0
                    )
                except asyncio.TimeoutError:
                    # Force kill if it doesn't terminate gracefully
                    process.kill()
                except Exception:
                    pass

        except Exception as cleanup_error:
            logger.debug(f"Cleanup error (can be ignored): {cleanup_error}")


st.set_page_config(page_title="Claude Chat with MCP", page_icon="🤖", layout="wide")

st.title("🤖 Claude Chat with MCP Server")
st.markdown(
    "Chat with Claude using Model Context Protocol (MCP) for enhanced capabilities"
)

# Initialize session state
init_session_state()

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    st.subheader("Claude Desktop MCP Servers")

    delay_between_calls = st.sidebar.slider(
        "⏱️ Delay Between Calls (seconds)",
        min_value=3,
        max_value=30,
        value=8,
        help="Delay to prevent API rate limiting",
    )

    max_iterations = st.sidebar.slider(
        "🔄 Max Iterations",
        min_value=10,
        max_value=100,
        value=50,
        help="Maximum number of iterations to prevent infinite loops",
    )

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


async def run_agent_async(
    message: str,
    status_container,
    progress_bar,
):
    """Run the agent with async loop"""

    try:
        server_params = server_configs["solidworks"]

        sc = {
            "transport": "stdio",
            "command": server_params.command,
            "args": server_params.args,
            "env": server_params.env,
        }

        client = MultiServerMCPClient({"solidworks": sc})
        tools = await client.get_tools()

        chat_agent = ChatBedrock(
            model_name="anthropic.claude-3-5-sonnet-20240620-v1:0",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region=os.getenv("AWS_REGION"),
        )

        agent = create_react_agent(chat_agent, tools)

        current_message = message
        conversation_count = 0

        while conversation_count < max_iterations and st.session_state.running:
            conversation_count += 1
            st.session_state.current_iteration = conversation_count

            # Update progress
            progress = conversation_count / max_iterations
            progress_bar.progress(progress)

            try:
                # response = agent.run(current_message, stream=False)
                response = agent.invoke(
                    {"messages": [{"role": "user", "content": current_message}]}
                )

                logger.info(response)

                has_tool_calls = hasattr(response, "tool_calls") and response.tool_calls

                if not has_tool_calls:
                    status_container.markdown(
                        """
                    <div class="success-box">
                        ✅ <strong>Agent indicates the task is complete!</strong>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                    break

                current_message = """
                Continue building the next components of the screw tightening machine.
                If you haven't finished all components yet, please continue creating them.
                Work systematically until the entire machine assembly is complete.
                """

                # Countdown delay
                if conversation_count < max_iterations and st.session_state.running:
                    for i in range(delay_between_calls, 0, -1):
                        if not st.session_state.running:
                            break
                        status_container.markdown(
                            f"""
                        <div class="countdown">
                            ⏳ Next iteration in {i} seconds...
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )
                        await asyncio.sleep(1)

            except Exception as e:
                error_msg = f"❌ Error in iteration {conversation_count}: {str(e)}"
                status_container.markdown(
                    f"""
                <div class="error-box">
                    {error_msg}
                </div>
                """,
                    unsafe_allow_html=True,
                )
                break

        if conversation_count >= max_iterations:
            status_container.markdown(
                f"""
            <div class="error-box">
                ⚠️ <strong>Reached maximum iterations ({max_iterations})</strong><br>
                Stopping to prevent infinite loop.
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Final status
        progress_bar.progress(1.0)
        status_container.markdown(
            """
        <div class="success-box">
            🎉 <strong>MCP Agent session completed!</strong>
        </div>
        """,
            unsafe_allow_html=True,
        )

    except Exception as e:
        status_container.markdown(
            f"""
        <div class="error-box">
            ❌ <strong>Fatal Error:</strong> {str(e)}
        </div>
        """,
            unsafe_allow_html=True,
        )
    finally:
        st.session_state.running = False
        # Add a small delay to ensure cleanup happens properly
        await asyncio.sleep(0.2)


def run_agent_sync(message: str, status_container, progress_bar):
    """Sync wrapper for the async agent function"""
    asyncio.run(run_agent_async(message, status_container, progress_bar))


try:
    # Create containers for dynamic updates
    status_container = st.empty()
    progress_bar = st.progress(0, "Initializing...")

    # Display existing messages
    display_chat_messages()

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Run async handler
        prompt = (
            f"""{prompt}\n print "terminate" when you are done and not calling tool."""
        )

        run_agent_sync(prompt, status_container, progress_bar)

except Exception as e:
    logger.exception(e)
