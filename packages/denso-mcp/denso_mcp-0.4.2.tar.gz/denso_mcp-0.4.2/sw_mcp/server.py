import logging
import queue
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Literal, Optional

import clr
import pyautogui
from fastmcp import FastMCP
from pydantic import BaseModel, Field

from sw_mcp.llm import get_llm
from sw_mcp.cursor import get_manager
from sw_mcp.solidworks import PaperSize
from sw_mcp.solidworks import SolidWorks as CSolidWorks
from sw_mcp.solidworks import ViewType
from sw_mcp.utils import get_solidworks_install_path

# Add SolidWorks references
sys.path.append(get_solidworks_install_path())
clr.AddReference("SolidWorks.Interop.sldworks")
clr.AddReference("SolidWorks.Interop.swconst")

import SolidWorks.Interop.swconst as swconst  # type: ignore

# Import SolidWorks types
from SolidWorks.Interop.sldworks import (
    IFeature,
    IModelDoc2,
    IPartDoc,
    ISldWorks,
    ModelDoc2,
    SldWorks,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("SW-MCPServer")

# Global variable to store the SolidWorks application instance
sw_app = CSolidWorks()
image_queue = queue.Queue[str]()


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[Dict[str, Any]]:
    """Manage the lifecycle of the MCP server"""
    try:
        logger.info("SolidWorksMCP server starting up")
        yield {}
    finally:
        # Clean up resources when shutting down
        global sw_app
        if sw_app is not None:
            logger.info("Closing SolidWorks on shutdown")
            try:
                # Try to close SolidWorks cleanly if possible
                await disconnect_from_solidworks()
            except:
                logger.warning("Could not cleanly exit SolidWorks")


mcp = FastMCP(
    "SolidWorksMCP",
    lifespan=server_lifespan,
    port=10001,
)


@mcp.tool(
    name="connect_to_solidworks",
    description="Establish a connection to SolidWorks application",
)
async def connect_to_solidworks(visible: bool = True) -> Dict[str, Any]:
    """Connect to SolidWorks application"""
    global sw_app

    try:
        cursor = get_manager()
        if sw_app.app is not None:
            sw_app.app.Visible = True
            return {
                "success": True,
                "message": "Already connected to SolidWorks",
                "status": "already_connected",
            }

        logger.info("Creating new SolidWorks application instance")
        sw_app = CSolidWorks()
        sw_app.connect()
        sw_app.app.Visible = visible

        cursor.focus_window()
        cursor.maximize_window()

        return {
            "success": True,
            "message": f"Connected to SolidWorks",
            "status": "connected",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to connect to SolidWorks: {str(e)}",
        }


@mcp.tool(
    name="disconnect_from_solidworks", description="Close the SolidWorks application"
)
async def disconnect_from_solidworks() -> Dict[str, Any]:
    """Disconnect from SolidWorks application"""
    global sw_app

    if sw_app is None:
        return {
            "success": True,
            "message": "Not connected to SolidWorks",
            "status": "already_disconnected",
        }

    try:
        sw_app.disconnect()
        return {
            "success": True,
            "message": "SolidWorks closed successfully",
            "status": "disconnected",
        }
    except Exception as e:
        return {"success": False, "message": f"Error closing SolidWorks: {str(e)}"}


# Define some example endpoints
@mcp.tool(name="open_document", description="Open a STEP file")
async def open_document(file_path: str) -> Dict[str, Any]:
    """Open a SolidWorks document"""
    global sw_app

    cursor = get_manager()
    cursor.focus_window()

    # Constants for document types
    # 1 = swDocPART, 2 = swDocASSEMBLY, 3 = swDocDRAWING
    try:
        return sw_app.open_file(file_path)
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@mcp.tool(
    name="save_document", description="Save the active document to a specified path"
)
async def save_document(file_path: str) -> Dict[str, Any]:
    """Save the active document to a specified path"""
    global sw_app

    try:
        active_doc = sw_app.get_active_doc()
        if not active_doc:
            return {"success": False, "message": "No active document"}

        # Save the document
        result = sw_app.save_model_doc(file_path, active_doc)

        if result:
            return {"success": True, "message": f"Document saved to {file_path}"}
        else:
            return {"success": False, "message": "Failed to save document"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


class CreateDrawingModel(BaseModel):
    width: float = Field(
        default=0.5,
        description="width of the sheet (in meters) if paper_size is user defined",
    )
    height: float = Field(
        default=0.5,
        description="height of the sheet (in meters) if paper_size is user defined",
    )
    paper_size: PaperSize = Field(
        default="A3",
        description="type of paper, if user defined width and height must also be defined",
    )


@mcp.tool(name="create_drawing", description="Create a new drawing document")
def create_drawing(data: CreateDrawingModel):
    global sw_app

    try:
        cursor = get_manager()
        # Create a new drawing document
        print(data)
        # paper = PaperSize[data.paper_size]
        cursor.focus_window()
        sw_app.create_drawing(data.paper_size, data.width, data.height)

        return {"success": True, "message": "Drawing document created"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


class AddViewModel(BaseModel):
    x: float = Field(
        ..., description="position of the view along x-axis (in meters). Eg. 0.2"
    )
    y: float = Field(
        ..., description="position of the view along y-axis (in meters). Eg. 0.3"
    )
    z: float = Field(
        ..., description="position of the view along z-axis (in meters). #g. 0.12"
    )
    view_type: ViewType = Field(
        ..., description="Type of model view to add to the drawing sheet"
    )


@mcp.tool(name="add_view", description="Add a view to the drawing document")
def add_view(data: AddViewModel) -> Dict[str, Any]:
    """
    Add a view to the drawing document along with dimension annotations using auto dimensioning

    Caution:
    dimension annotations are added outside the view, so add some distance between the views for the dimension annotations
    """
    global sw_app

    cursor = get_manager()
    cursor.focus_window()

    try:
        # Add the view to the drawing document
        sw_app.add_view(data.view_type, data.x, data.y, data.z)
        return {"success": True, "message": "View added to drawing document"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


class TakeScreenshot(BaseModel):
    start_x: int = Field(..., description="Start of the region selection X-axis")
    start_y: int = Field(..., description="Start of the region selection Y-axis")
    width: int = Field(..., description="Width of the region")
    height: int = Field(..., description="Height of the region")


@mcp.tool(name="take_screenshot", description="Take a screenshot of the whole screen")
def take_screenshot(data: TakeScreenshot):
    """Takes screenshot of the screen and returns the image path"""
    global image_queue

    cursor = get_manager()
    cursor.focus_window()

    region = (data.start_x, data.start_y, data.width, data.height)
    _, file_path = cursor.take_screenshot(region)

    image_queue.put_nowait(file_path)

    # return dict(status=True, data=dict(file_path=file_path))
    return file_path


@mcp.tool(name="take_screenshot_region", description="Take a screenshot of a region")
def take_screenshot_region(data: TakeScreenshot):
    """Take a screenshot of a region and return the image path"""
    global image_queue

    cursor = get_manager()
    cursor.focus_window()

    region = (data.start_x, data.start_y, data.width, data.height)
    _, file_path = cursor.take_screenshot(region)

    image_queue.put_nowait(file_path)

    # return dict(status=True, data=dict(file_path=file_path))
    return file_path


@mcp.tool(
    name="find_image_on_screen",
    description="Find the location of an image on the screen",
)
def find_image_on_screen():
    cursor = get_manager()
    cursor.focus_window()
    global image_queue

    if not image_queue.empty():
        file_path = image_queue.get_nowait()
    else:
        return dict(status=False, message="no screenshot found")

    pos = cursor.find_image_on_screen(file_path)
    if pos:
        return dict(status=True, data=dict(pos_x=pos[0], pos_y=pos[1]), message="Found")

    return dict(status=False, message="Not found on this screen")


class MoveCursorAndClick(BaseModel):
    x: float = Field(..., description="X position")
    y: float = Field(..., description="Y position")
    n_clicks: int = Field(0, description="number of clicks to simulate (default=0)")


@mcp.tool(
    name="move_cursor_and_click",
    description="move cursor to a position and simulate a click",
)
def move_cursor_and_click(data: MoveCursorAndClick):
    """Move the cursor and simulate a click"""
    cursor = get_manager()
    cursor.focus_window()

    nx, ny = cursor.move(data.x, data.y)
    cursor.click(nx, ny, clicks=data.n_clicks)

    return dict(status=True, new_position=dict(x=nx, y=ny))


@mcp.tool(
    name="take_solidworks_window_screenshot",
    description="Take a screenshot of the SOLIDWORKS application window",
)
def take_solidworks_window_screenshot():
    """
    Take a screenshot of the SOLIDWORKS application window.
    """

    global image_queue

    cursor = get_manager()
    cursor.focus_window()
    img, file_path = cursor.screenshot_window()
    image_queue.put_nowait(file_path)

    if img is None:
        return dict(
            success=False, message="Failed to take SOLIDWORKS window screenshot"
        )
    # return dict(success=True, data=dict(file_path=file_path))
    return file_path


@mcp.tool(name="analyze_image", description="Analyze the image for the given target")
def analyze_image(target: str):
    """
    Analyzed the screenshot for the given target
    """

    global image_queue

    if image_queue.empty():
        return "no screenshots in the queue. take one"

    image_path = image_queue.get_nowait()

    llm = get_llm()

    prompt = f"""
    You are an expert in analyzing 2D engineering drawings, especially those generated using SolidWorks.
    You are given an image of a 2D drawing. Your task is to carefully inspect the image and determine whether it meets the specified requirement.

    Requirement:
    {target}

    Be specific and concise in your analysis. If an issue is detected, explain what and where it is in the drawing.
    """

    response = llm(prompt, image_path)
    return response.text


OrientationType = Literal["top", "front", "back", "bottom", "left", "right"]


class ChangeModelView(BaseModel):
    orientation: OrientationType = Field(..., description="Orientation of the model")


@mcp.tool(name="change_model_view", description="Change model's view angle")
def change_model_view(data: ChangeModelView):

    keyboard_shortcut: dict[OrientationType, list[str]] = {
        "front": ["ctrl", "1"],
        "back": ["ctrl", "2"],
        "left": ["ctrl", "3"],
        "right": ["ctrl", "4"],
        "top": ["ctrl", "5"],
        "bottom": ["ctrl", "6"],
    }

    cursor = get_manager()
    orientation = data.orientation
    return {"status": cursor.keyboard_shortcut(keyboard_shortcut[orientation])}


@mcp.tool(name="auto_arrange_dimensions", description="Auto arrange view dimensions")
def auto_arrange_dimensions():
    """Auto arrange view dimensions if some/all dimensions are selected"""

    global sw_app

    cursor = get_manager()
    cursor.focus_window()

    # Select all entities
    doc_ext = ModelDoc2(sw_app.draw_doc).Extension
    doc_ext.SelectAll()
    time.sleep(2)

    # hit ctrl to bring up the option
    pyautogui.hotkey("ctrl")

    # hover over the option
    failed = False
    try:
        auto_arrange_path = str(Path.cwd() / "images" / "auto-arrange.png")
        x, y = cursor.find_image_on_screen(auto_arrange_path)
        cursor.move(x, y)
    except:
        failed = True
        x, y = cursor.get_current_position()
        cursor.move(x + 50, y - 10)

    # perform auto arrange
    try:
        auto_arrange_option_path = str(
            Path.cwd() / "images" / "auto-arrange-option.png"
        )
        x, y = cursor.find_image_on_screen(auto_arrange_option_path)
        cursor.move(x, y)
        cursor.click()
    except:
        # alternative way
        x, y = cursor.get_current_position()
        cursor.move(x + 5, y - 50)
        cursor.click()

    pyautogui.hotkey("esc")


@mcp.tool(name="drag_view_start", description="start dragging drawing view")
def drag_view_start(x: int, y: int):
    """
    start dragging view with alt+mouse1 pressed
    """
    cursor = get_manager()
    cursor.focus_window()

    cursor.mouse_down(x, y)
    pyautogui.keyDown("alt")


@mcp.tool(name="drag_view_end", description="stop dragging drawing view")
def drag_view_end(x: int, y: int):
    """
    release the view
    """
    cursor = get_manager()
    cursor.focus_window()

    cursor.mouse_up(x, y)
    pyautogui.keyUp("alt")


@mcp.tool(name="mouse_drag_start", description="start dragging mouse cursor")
def mouse_drag_start(x: int, y: int):
    cursor = get_manager()
    cursor.focus_window()

    cursor.mouse_down(x, y)


@mcp.tool(name="mouse_drag_end", description="end dragging mouse cursor")
def mouse_drag_end(x: int, y: int):
    cursor = get_manager()
    cursor.mouse_up(x, y)


@mcp.tool(
    name="fetch_sheet_bounds", description="fetch the corner locations of the sheet"
)
def fetch_sheet_bounds():
    """
    Fetch the four corner locations of the sheet
    """
    return {
        "top-left": (625, 66),
        "top-right": (2386, 66),
        "bottom-left": (625, 1289),
        "bottom-right": (2386, 1289),
    }


SheetSize = Literal["A0", "A1", "A2", "A3", "A4"]


class FetchSheetSize(BaseModel):
    selected_drawing_sheet_size: SheetSize = Field(..., description="size of the sheet")


@mcp.tool(
    name="fetch_sheet_size", description="width and height of the sheet in meters"
)
def fetch_sheet_size(data: FetchSheetSize):
    """
    Fetch sheet size in meters (height x width)
    A0 -> 841 mm x 1189 mm
    A1 -> 594 mm x 841 mm
    A2 -> 420 mm x 594 mm
    A3 -> 297 mm x 420 mm
    A4 -> 210 mm x 297 mm
    """

    # Convert mm to meters (1 mm = 0.001 m)
    sheet_sizes: dict[SheetSize, tuple[float, float]] = {
        "A0": (1.189, 0.841),
        "A1": (0.841, 0.594),
        "A2": (0.594, 0.420),
        "A3": (0.420, 0.297),
        "A4": (0.297, 0.210),
    }

    width, height = sheet_sizes[data.selected_drawing_sheet_size]
    return {"width": width, "height": height}


# resources
# Basic dynamic resource returning a string
@mcp.resource(
    uri="resource://latest-screenshot",
    name="LastScreenshotTakenByLLM",
    description="Fetches the last screenshot taken by LLM",
    mime_type="image/png",
)
def get_screenshot() -> str:
    """Fetches the last screenshot taken by LLM."""

    global image_queue

    if image_queue.empty():
        return None

    file_path = image_queue.get_nowait()
    with open(file_path, "rb") as f:
        bytes_content = f.read()

    return bytes_content


# System Prompt
@mcp.prompt()
def ask_about_topic(topic: str) -> str:
    """System prompt for LLM."""
    return f"Use only the tools you have been provided and use screenshots to know where and how much to move the cursor. {topic}"


from mcp.server.fastmcp.prompts import base


@mcp.prompt()
def follow_prompt_instruct(topic: str) -> str:
    """System prompt constructor for instructing the LLM on a given topic.

    This function generates a system prompt that provides instructions to the LLM
    on how to handle a specific topic. It ensures the LLM uses the provided tools
    correctly and pays attention to visual elements when manipulating the interface.

    Args:
        topic (str): The specific subject or task the LLM should address.
    """
    return f"""
    Please assist with the following task related to: {topic}
    
    IMPORTANT INSTRUCTIONS:
    1. Use ONLY the tools you have been explicitly provided with in this session
    2. When interacting with the UI:
        - The origin of the drawing sheet is on the bottom-left corner
        - All the positions you specify for adding views should be in meters and relative to the origin in the bounds of the sheet size
        - Use screenshots to identify element positions
        - Use multiple screenshots to confirm positions
        - Note precise cursor movement requirements
        - Pay attention to visual feedback after actions
    3. Follow step-by-step reasoning when approaching the task
    4. If you encounter limitations, explain them clearly

    Sheet Sizes: (height x width)
    A0 -> 0.841 m x 1.189 m
    A1 -> 0.594 m x 0.841 m
    A2 -> 0.420 m x 0.594 m
    A3 -> 0.297 m x 0.420 m
    A4 -> 0.210 m x 0.297 m
    
    Begin by analyzing the requirements for: {topic}
    """


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]
