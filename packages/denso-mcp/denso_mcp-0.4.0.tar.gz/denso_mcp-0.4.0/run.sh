# setup .venv and install dependencies
uv sync

# Start the MCP server
echo "Starting MCP server"
uv run mcp-server.py &

# Run the Streamlit app
echo "Starting Streamlit server"
uv run streamlit run streamlit_app.py
