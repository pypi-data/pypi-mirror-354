from .utils import *
from watchdog.events import FileSystemEventHandler
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, target_path, callback):
        super().__init__()
        self.target_path = target_path
        self.callback = callback

    def on_modified(self, event):
        if event.src_path == self.target_path:
            print(f"Detected change in {event.src_path}")
            self.callback(event.src_path)
class ClipboardManager:
    def __init__(self):
        self.last_program_copy = None
        self.monitor_thread = None
        self.running = False
        self.clip = pyperclip
    def custom_copy(self,
                    text):
        """Wrap pyperclip.copy to track program-initiated copies."""
        custom_copy(text,clip=pyperclip)
        self.last_program_copy = text
        print(f"Program copied: {text}")

    def custom_paste(self,
                     file_path=None):
        """Perform a paste action using keyboard automation and save clipboard to a file."""
        # Perform the paste action
        file_path = file_path or "/home/computron/Documents/cheatgpt/outputs/output.html"
        paste_modifier()
        paste_to_file(file_path=file_path,clip=self.clip)
    def screenshot_specific_screen(self,
                                   output_file="new_screen.png",
                                   monitor_index=1):
        """Capture a screenshot of a specific monitor."""
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                if monitor_index < 1 or monitor_index >= len(monitors):
                    print(f"Invalid monitor index: {monitor_index}. Available monitors: {len(monitors)-1}")
                    return None
                monitor = monitors[monitor_index]
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                img.save(output_file)
                print(f"Saved screenshot of monitor {monitor_index} to: {output_file}")
                return monitor  # Return monitor info for coordinate adjustment
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None
    def switch_window(self,
                      window_title="My Permanent Tab"):
        """Switch to a window by partial title match (Linux with xdotool)."""
        if platform.system() != 'Linux':
            modifier = 'command' if platform.system() == 'Darwin' else 'alt'
            try:
                pyautogui.keyDown(modifier)
                time.sleep(0.1)
                pyautogui.press('tab')
                time.sleep(0.1)
                pyautogui.keyUp(modifier)
                print("Switched to first window (non-Linux fallback)")
                time.sleep(0.5)
            except Exception as e:
                print(f"Error switching window: {e}")
            return
        try:
            result = subprocess.run(
                ['xdotool', 'search', '--name', window_title],
                capture_output=True, text=True
            )
            window_ids = result.stdout.strip().split()
            if not window_ids:
                print(f"No window found with title containing: {window_title}")
                return
            subprocess.run(
                [
                    'xdotool',
                    'activate',
                    window_ids[0]
                    ]
                )
            print(f"Switched to window with title containing: {window_title}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error switching window with xdotool: {e}")
    def open_browser_tab(self, title="My Permanent Tab"):
        """Create and open a browser tab with a permanent title."""
        # Create HTML file with fixed title
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
            <p>This is a programmatically opened tab with a permanent title.</p>
        </body>
        </html>
        """
        
        # Save HTML file
        try:
            with open(self.html_file_path, 'w') as f:
                f.write(html_content)
            print(f"Saved HTML file: {self.html_file_path}")
        except Exception as e:
            print(f"Error saving HTML file: {e}")
            return

        # Open in default browser
        try:
            webbrowser.open(f"file://{self.html_file_path}")
            print(f"Opened browser tab with title: {title}")
        except Exception as e:
            print(f"Error opening browser: {e}")
    def monitor_clipboard(self,
                          interval=0.5):
        """Monitor clipboard, ignoring program's own copies."""
        last_content = pyperclip.paste()
        while self.running:
            try:
                current_content = pyperclip.paste()
                if current_content != last_content and current_content != self.last_program_copy:
                    print("External clipboard change detected! New content:", current_content)
                    last_content = current_content
                time.sleep(interval)
            except Exception as e:
                print(f"Error accessing clipboard: {e}")
                time.sleep(interval)

    def start_monitoring(self):
        """Start clipboard monitoring in a separate thread."""
        if not self.monitor_thread:
            self.running = True
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self.monitor_thread.start()
            print("Started clipboard monitoring...")

    def stop_monitoring(self):
        """Stop clipboard monitoring."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
            self.monitor_thread = None
        print("Stopped clipboard monitoring.")

    def screenshot_specific_screen(self,
                                   output_file="new_screen.png",
                                   monitor_index=1):
        """Capture a screenshot of a specific monitor."""
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                if monitor_index < 1 or monitor_index >= len(monitors):
                    print(f"Invalid monitor index: {monitor_index}. Available monitors: {len(monitors)-1}")
                    return None
                monitor = monitors[monitor_index]
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
                img.save(output_file)
                print(f"Saved screenshot of monitor {monitor_index} to: {output_file}")
                return monitor  # Return monitor info for coordinate adjustment
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None

    def perform_ocr(self,
                    screenshot_file="new_screen.png",
                    confidence_threshold=60):
        """Perform OCR on a screenshot and return extracted text with coordinates."""
        self.extracted_texts = perform_ocr(screenshot_file=screenshot_file,
                                           confidence_threshold=confidence_threshold)
        return self.extracted_texts
    def move_mouse_to_text(self,
                           extracted_texts,
                           monitor_info,
                           text_index=0,
                           target_text=None):
        """Move the mouse to the center of a text box from OCR results."""
        bool_response = move_mouse_to_text(extracted_texts=extracted_texts,
                       monitor_info=monitor_info,
                       text_index=text_index,
                       target_text=target_text)
        return nbool_response
