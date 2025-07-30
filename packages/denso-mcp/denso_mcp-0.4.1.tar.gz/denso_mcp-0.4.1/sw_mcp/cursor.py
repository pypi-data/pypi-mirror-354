import time
import tkinter as tk
from pathlib import Path
from threading import Thread
from typing_extensions import Self

import keyboard
import pyautogui
from PIL import Image, ImageGrab

# For Windows-specific window handling
try:
    import win32con
    import win32gui
    import win32ui
    import win32com.client

    WINDOWS_SUPPORT = True
except ImportError:
    WINDOWS_SUPPORT = False
    print(
        "Windows-specific features require PyWin32. Install with: pip install pywin32"
    )


class CursorManager:
    """
    A class that manages cursor operations using pyautogui.
    Provides methods for common mouse actions like clicking, moving, and dragging.
    """

    manager: Self = None

    @classmethod
    def get_manager(cls):
        manager = CursorManager()
        if not cls.manager:
            cls.manager = manager

        return cls.manager

    def __init__(self, speed=0.5):
        """
        Initialize the CursorManager.

        Args:
            speed (float): The duration of mouse movements in seconds (default: 0.5)
        """
        self.speed = speed
        # Get screen dimensions for bounds checking
        self.screen_width, self.screen_height = pyautogui.size()

        # directory for storing screenshots
        self.save_path = Path.cwd() / "tmp" / "screenshots"
        self.save_path.mkdir(parents=True, exist_ok=True)

    def mouse_down(self, x: int, y: int):
        pyautogui.mouseDown(x, y)

    def mouse_up(self, x: int, y: int):
        pyautogui.mouseUp()

    def move(self, x, y, duration=None):
        """
        Move the cursor to the specified coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            duration (float, optional): Override the default movement speed

        Returns:
            tuple: The new cursor position (x, y)
        """
        # Ensure coordinates are within screen bounds
        x = max(0, min(x, self.screen_width - 1))
        y = max(0, min(y, self.screen_height - 1))

        pyautogui.moveTo(x, y, duration or self.speed)
        return (x, y)

    def click(self, x=None, y=None, button="left", clicks=1, interval=0.0):
        """
        Click at the specified position or current position.

        Args:
            x (int, optional): X coordinate (uses current position if None)
            y (int, optional): Y coordinate (uses current position if None)
            button (str): Mouse button to click ('left', 'middle', 'right')
            clicks (int): Number of clicks
            interval (float): Time between clicks in seconds

        Returns:
            tuple: The cursor position after clicking
        """
        if x is not None and y is not None:
            self.move(x, y)

        pyautogui.click(button=button, clicks=clicks, interval=interval)
        return pyautogui.position()

    def double_click(self, x=None, y=None):
        """
        Double-click at the specified position or current position.

        Args:
            x (int, optional): X coordinate (uses current position if None)
            y (int, optional): Y coordinate (uses current position if None)

        Returns:
            tuple: The cursor position after double-clicking
        """
        return self.click(x, y, clicks=2)

    def right_click(self, x=None, y=None):
        """
        Right-click at the specified position or current position.

        Args:
            x (int, optional): X coordinate (uses current position if None)
            y (int, optional): Y coordinate (uses current position if None)

        Returns:
            tuple: The cursor position after right-clicking
        """
        return self.click(x, y, button="right")

    def drag(self, start_x, start_y, end_x, end_y, button="left", duration=None):
        """
        Drag from start coordinates to end coordinates.

        Args:
            start_x (int): Starting X coordinate
            start_y (int): Starting Y coordinate
            end_x (int): Ending X coordinate
            end_y (int): Ending Y coordinate
            button (str): Mouse button to use for dragging ('left', 'middle', 'right')
            duration (float, optional): Override the default movement speed

        Returns:
            tuple: The cursor position after dragging
        """
        # Move to start position
        self.move(start_x, start_y)

        # Ensure coordinates are within screen bounds
        end_x = max(0, min(end_x, self.screen_width - 1))
        end_y = max(0, min(end_y, self.screen_height - 1))

        # Perform drag operation
        pyautogui.dragTo(end_x, end_y, duration or self.speed, button=button)
        return (end_x, end_y)

    def select_region(self, start_x, start_y, end_x, end_y):
        """
        Select a rectangular region by dragging from one corner to another.

        Args:
            start_x (int): X coordinate of the starting corner
            start_y (int): Y coordinate of the starting corner
            end_x (int): X coordinate of the ending corner
            end_y (int): Y coordinate of the ending corner

        Returns:
            dict: A dictionary containing the region coordinates and dimensions
                  {
                      'top_left': (min_x, min_y),
                      'bottom_right': (max_x, max_y),
                      'width': width,
                      'height': height,
                      'area': area
                  }
        """
        # Perform the drag operation to select the region
        self.drag(start_x, start_y, end_x, end_y)

        # Calculate the region properties
        min_x = min(start_x, end_x)
        max_x = max(start_x, end_x)
        min_y = min(start_y, end_y)
        max_y = max(start_y, end_y)

        width = max_x - min_x
        height = max_y - min_y
        area = width * height

        # Return a dictionary with region information
        return {
            "top_left": (min_x, min_y),
            "bottom_right": (max_x, max_y),
            "width": width,
            "height": height,
            "area": area,
        }

    def screenshot_selected_region(
        self, start_x: float, start_y: float, end_x: float, end_y: float, filename: str
    ):
        """
        Select a region by dragging and take a screenshot of it.

        Args:
            start_x (int): X coordinate of the starting corner
            start_y (int): Y coordinate of the starting corner
            end_x (int): X coordinate of the ending corner
            end_y (int): Y coordinate of the ending corner
            filename (str, optional): The name of the screenshot file
            save_path (str, optional): The directory to save the screenshot

        Returns:
            tuple: (Image object, full path to saved file)
        """
        # Select the region
        region_info = self.select_region(start_x, start_y, end_x, end_y)

        # Extract region coordinates
        left, top = region_info["top_left"]
        width = region_info["width"]
        height = region_info["height"]

        # Take screenshot of the selected region
        return self.take_screenshot(
            region=(left, top, width, height), filename=filename
        )

    def get_current_position(self):
        """
        Get the current cursor position.

        Returns:
            tuple: The current (x, y) position of the cursor
        """
        return pyautogui.position()

    def position_tracker(self, duration=10, interval=0.1):
        """
        Track and print cursor position for a specified duration.
        Press Ctrl+C to stop tracking early.

        Args:
            duration (float): How long to track the position in seconds (default: 10)
            interval (float): How often to update the position in seconds (default: 0.1)

        Returns:
            list: List of recorded positions [(x1, y1, time1), (x2, y2, time2), ...]
        """
        positions = []
        start_time = time.time()
        end_time = start_time + duration

        print(
            "Move your cursor to the desired location. Press Ctrl+C to stop tracking."
        )
        print("Tracking cursor position...")

        try:
            while time.time() < end_time:
                x, y = self.get_current_position()
                elapsed = time.time() - start_time
                positions.append((x, y, elapsed))
                print(f"Position: ({x}, {y}) at {elapsed:.2f}s")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nTracking stopped by user.")

        print(f"Final position: {positions[-1][0:2]}")
        return positions

    def coordinate_picker(self):
        """
        Open a simple GUI that shows the coordinates under the cursor.
        Press 'c' to copy the current coordinates to clipboard.
        Press 'q' to quit.

        Returns:
            tuple: The last captured (x, y) position
        """
        result = {"position": None}

        def update_label():
            while running[0]:
                x, y = pyautogui.position()
                label_var.set(f"X: {x}, Y: {y}")
                if keyboard.is_pressed("c"):
                    root.clipboard_clear()
                    root.clipboard_append(f"{x}, {y}")
                    result["position"] = (x, y)
                    status_var.set(f"Copied ({x}, {y}) to clipboard!")
                    time.sleep(0.5)  # Prevent multiple copies
                if keyboard.is_pressed("q"):
                    running[0] = False
                    root.destroy()
                time.sleep(0.1)

        # Create the GUI
        root = tk.Tk()
        root.title("Coordinate Picker")
        root.geometry("300x100")
        root.attributes("-topmost", True)  # Keep window on top

        label_var = tk.StringVar()
        label = tk.Label(root, textvariable=label_var, font=("Arial", 16))
        label.pack(pady=10)

        status_var = tk.StringVar()
        status_var.set("Press 'c' to copy coordinates. Press 'q' to quit.")
        status = tk.Label(root, textvariable=status_var)
        status.pack(pady=5)

        running = [True]

        # Start the update thread
        update_thread = Thread(target=update_label)
        update_thread.daemon = True
        update_thread.start()

        # Run the GUI
        root.mainloop()

        return result["position"]

    def find_image_on_screen(self, image_path, confidence=0.9, grayscale=False):
        """
        Find an image on the screen and return its center coordinates.
        Useful for finding buttons or UI elements.

        Args:
            image_path (str): Path to the image file to find
            confidence (float): Matching confidence threshold (0-1, default: 0.9)
            grayscale (bool): Whether to use grayscale matching for better performance (default: False)

        Returns:
            tuple or None: Center coordinates (x, y) of the found image, or None if not found
        """
        try:
            # Find the image on screen
            location = pyautogui.locateOnScreen(
                image_path, confidence=confidence, grayscale=grayscale
            )

            if location:
                # Calculate center point of the found image
                center_x = location.left + location.width // 2
                center_y = location.top + location.height // 2
                print(f"Found image at center coordinates: ({center_x}, {center_y})")
                return (center_x, center_y)
            else:
                print(f"Image '{image_path}' not found on screen.")
                return None
        except Exception as e:
            print(f"Error finding image: {e}")
            return None

    def take_screenshot(self, region: tuple[int, int, int, int], filename: str = None):
        """
        Take a screenshot of the entire screen or a specific region.

        Args:
            region (tuple[float, float, float, float]): The region to capture as (left, top, width, height).
                                    If None, captures the entire screen.
            filename (str): The name of the screenshot file.
                                    If None, generates a timestamp-based filename.
            save_path (str): The directory to save the screenshot.
                                    If None, saves to the current directory.

        Returns:
            tuple: (Image object, full path to saved file)
        """
        # Generate filename with timestamp if not provided
        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        # Ensure filename has .png extension
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filename += ".png"

        # Create full path
        full_path = str(self.save_path / filename)

        # Take screenshot
        if region is None:
            # Capture entire screen
            screenshot = pyautogui.screenshot()
        else:
            # Capture specified region
            left, top, width, height = region
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # Save the screenshot
        screenshot.save(full_path)

        print(f"Screenshot saved to: {full_path}")
        return screenshot.tobytes(), full_path

    def list_window_names(self):
        """
        List all visible window names to help identify the target window.

        Returns:
            list: List of tuples containing (window handle, window title)
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return []

        window_list = []

        def enum_windows_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if window_text:
                    results.append((hwnd, window_text))
            return True

        win32gui.EnumWindows(enum_windows_callback, window_list)
        return sorted(window_list, key=lambda x: x[1].lower())

    def find_window(self) -> tuple[int, str]:
        """
        Find a window by a substring in its title.

        Args:
            title_substring (str): Substring to search for in window titles

        Returns:
            tuple or None: (hwnd, full_title) of the first matching window, or None if not found
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return None

        title_substring = "SOLIDWORKS Premium"

        windows = self.list_window_names()
        matches = [window for window in windows if title_substring in window[1]]

        if matches:
            return matches[0]
        return None

    def screenshot_window(
        self,
        include_border: bool = True,
        filename: str = None,
    ):
        """
        Take a screenshot of a specific application window.

        Args:
            window_title (str, optional): Substring of the window title to capture
            include_border (bool): Whether to include window borders
            filename (str, optional): The name of the screenshot file
            save_path (str, optional): The directory to save the screenshot

        Returns:
            tuple: (Image object, full path to saved file)
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return None, None

        # take focus
        self.focus_window()

        hwnd, _ = self.find_window()

        # Get window dimensions
        try:
            # Get the window rectangle
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top

            if not include_border:
                # Get the client area (without borders)
                client_rect = win32gui.GetClientRect(hwnd)
                client_left, client_top, client_right, client_bottom = client_rect
                client_width = client_right - client_left
                client_height = client_bottom - client_top

                # Adjust for borders and title bar
                border_width = (width - client_width) // 2
                title_height = height - client_height - border_width

                left += border_width
                top += title_height
                width = client_width
                height = client_height
        except Exception as e:
            print(f"Error getting window dimensions: {e}")
            return None, None

        try:
            # Method 1: Use PyWin32 for a more direct capture (Windows only)
            # Create device contexts
            window_dc = win32gui.GetWindowDC(hwnd)
            dc_obj = win32ui.CreateDCFromHandle(window_dc)
            compat_dc = dc_obj.CreateCompatibleDC()

            # Create bitmap object
            bitmap = win32ui.CreateBitmap()
            bitmap.CreateCompatibleBitmap(dc_obj, width, height)
            compat_dc.SelectObject(bitmap)

            # Copy screen to bitmap
            compat_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)

            # Convert bitmap to PIL Image
            bmp_info = bitmap.GetInfo()
            bmp_bits = bitmap.GetBitmapBits(True)
            screenshot = Image.frombuffer(
                "RGB",
                (bmp_info["bmWidth"], bmp_info["bmHeight"]),
                bmp_bits,
                "raw",
                "BGRX",
                0,
                1,
            )

            # Clean up resources
            compat_dc.DeleteDC()
            dc_obj.DeleteDC()
            win32gui.ReleaseDC(hwnd, window_dc)

        except Exception as e:
            print(f"Error capturing window with PyWin32: {e}")
            print("Falling back to ImageGrab method...")

            # Method 2: Fallback to PIL's ImageGrab (less precise but more compatible)
            try:
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.2)  # Give window time to come to foreground
                screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
            except Exception as e2:
                print(f"Error capturing window with ImageGrab: {e2}")
                return None, None

        # Generate filename
        if filename is None:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            window_name = win32gui.GetWindowText(hwnd).replace(" ", "_")[:30]
            filename = f"window_{window_name}_{timestamp}.png"

        # Ensure filename has .png extension
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filename += ".png"

        full_path = str(self.save_path / filename)
        screenshot.save(full_path)

        print(f"Window screenshot saved to: {full_path}")
        return screenshot.tobytes(), full_path

    def get_target_application_positions(self):
        """
        Get the position and dimensions of a specific application window.
        Useful for targeting mouse actions within an application.

        Args:
            window_title (str, optional): Substring of the window title
            hwnd (int, optional): Window handle (if known)

        Returns:
            dict: Window information with positions and dimensions
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return None

        try:
            hwnd, _ = self.find_window()
            # Get window dimensions
            window_rect = win32gui.GetWindowRect(hwnd)
            left, top, right, bottom = window_rect
            width = right - left
            height = bottom - top

            # Get client area (without borders)
            client_rect = win32gui.GetClientRect(hwnd)
            client_left, client_top, client_right, client_bottom = client_rect
            client_width = client_right - client_left
            client_height = client_bottom - client_top

            # Calculate border and title bar sizes
            border_width = (width - client_width) // 2
            title_height = height - client_height - border_width

            # Calculate client area position in screen coordinates
            client_left_screen = left + border_width
            client_top_screen = top + title_height

            return {
                "window": {
                    "handle": hwnd,
                    "title": win32gui.GetWindowText(hwnd),
                    "left": left,
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "width": width,
                    "height": height,
                    "center": (left + width // 2, top + height // 2),
                },
                "client_area": {
                    "left": client_left_screen,
                    "top": client_top_screen,
                    "right": client_left_screen + client_width,
                    "bottom": client_top_screen + client_height,
                    "width": client_width,
                    "height": client_height,
                    "center": (
                        client_left_screen + client_width // 2,
                        client_top_screen + client_height // 2,
                    ),
                },
            }
        except Exception as e:
            print(f"Error getting window information: {e}")
            return None

    def click_relative_to_window(
        self,
        window_title=None,
        hwnd=None,
        x_offset=0,
        y_offset=0,
        client_area=True,
        button="left",
        clicks=1,
    ):
        """
        Click at a position relative to a specific window.

        Args:
            window_title (str, optional): Substring of the window title
            hwnd (int, optional): Window handle (if known)
            x_offset (int): X offset from the window's left edge (or client area left edge)
            y_offset (int): Y offset from the window's top edge (or client area top edge)
            client_area (bool): If True, positions are relative to client area, otherwise to window frame
            button (str): Mouse button to click ('left', 'middle', 'right')
            clicks (int): Number of clicks

        Returns:
            tuple: The cursor position after clicking
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return None

        # Get window information
        window_info = self.get_target_application_positions(window_title, hwnd)
        if not window_info:
            return None

        # Calculate absolute position
        if client_area:
            x = window_info["client_area"]["left"] + x_offset
            y = window_info["client_area"]["top"] + y_offset
        else:
            x = window_info["window"]["left"] + x_offset
            y = window_info["window"]["top"] + y_offset

        # Bring window to foreground
        win32gui.SetForegroundWindow(window_info["window"]["handle"])
        time.sleep(0.2)  # Give window time to come to foreground

        # Move and click
        return self.click(x, y, button=button, clicks=clicks)

    def maximize_window(self):
        """
        Maximize a window.

        Returns:
            bool: True if successful, False otherwise
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return False

        hwnd, _ = self.find_window()
        try:

            # Maximize window
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            print(f"Window '{win32gui.GetWindowText(hwnd)}' maximized.")
            return True
        except Exception as e:
            print(f"Error maximizing window: {e}")
            return False

    def focus_window(self):
        """
        Bring a window to the front/foreground.

        Returns:
            bool: True if successful, False otherwise
        """
        if not WINDOWS_SUPPORT:
            print("This feature requires PyWin32 on Windows.")
            return False

        try:
            # Find window by title if hwnd not provided
            hwnd, _ = self.find_window()

            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys("%")

            win32gui.SetForegroundWindow(hwnd)

            window_title = win32gui.GetWindowText(hwnd)
            print(f"Window '{window_title}' brought to front.")
            return True

        except Exception as e:
            print(f"Error bringing window to front: {e}")
            return False

    def keyboard_shortcut(self, shortcut: list[str]):
        """
        Execute a keyboard shortcut, optionally targeting a specific window.

        Args:
            shortcut (str): Shortcut in format like "ctrl+c", "alt+f4", "ctrl+shift+esc"
            target_window (str, optional): Window title to target the shortcut at

        Returns:
            bool: True if successful
        """
        try:
            # Focus target window if specified
            self.focus_window()

            # Execute the hotkey
            pyautogui.hotkey(*shortcut)
            print(f"Pressed {shortcut} in window")

            return True
        except Exception as e:
            print(f"Error executing keyboard shortcut: {e}")
            return False

    @property
    def current_position(self):
        return self.get_current_position()


get_manager = CursorManager.get_manager
