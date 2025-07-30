# AI Planet 3D-2D Converter

A Streamlit application that allows users to upload 3D model files (like .step, .x_t) and convert them to 2D drawings using SolidWorks.

## Features

- Upload 3D model files (.step, .x_t, .stp, .igs, .iges, etc.)
- Automatic conversion to 2D drawings with multiple views (TOP, FRONT, ISOMETRIC)
- Display of conversion status and results

## Requirements

- Python 3.10+
- Streamlit
- aiohttp
- fastmcp
- pythonnet
- Access to SolidWorks API service

## Installation

Use `uv` to setup the environment and install dependencies
```bash
uv sync
```


## Usage

1. Start the MCP server in **sse** mode
   ```bash
   uv run mcp-server.py --sse
   ```

   The server will start at [http://localhost:10001](http://localhost:10001)

2. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open your web browser and navigate to the URL displayed in the terminal (usually http://localhost:8501)

4. Upload a 3D model file using the file uploader

5. Click the "Convert to 2D" button to start the conversion process

6. Wait for the conversion to complete and view the results

## Notes

- The application requires access to a running SolidWorks API service
- Ensure that the SolidWorks API service URL is correctly configured in the application
- The temporary uploaded files are stored in the `temp_uploads` directory
