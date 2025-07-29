from .. imports import *
class WindowManager(metaclass=SingletonMeta):
    def __init__(self):
        
        if not hasattr(self, 'initialized'):
            self.initialized = True
    def screenshot_specific_screen(self, output_file="new_screen.png", monitor_index=1):
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

    def get_window_monitor(self, window_id):
        """Determine which monitor a window resides in based on its position."""
        try:
            # Get window geometry using xdotool
            result = subprocess.run(
                ['xdotool', 'getwindowgeometry', window_id],
                capture_output=True, text=True
            )
            output = result.stdout
            # Parse position (e.g., "Position: 1920,100")
            position_line = [line for line in output.split('\n') if 'Position' in line][0]
            x, y = map(int, position_line.split(': ')[1].split(' ')[0].split(','))

            # Get monitor information using mss
            with mss.mss() as sct:
                monitors = sct.monitors[1:]  # Skip monitor 0 (combined desktop)
                for index, monitor in enumerate(monitors, 1):
                    left = monitor['left']
                    top = monitor['top']
                    right = left + monitor['width']
                    bottom = top + monitor['height']
                    # Check if window's top-left corner is within monitor bounds
                    if left <= x < right and top <= y < bottom:
                        print(f"Window {window_id} is on monitor {index}: {monitor}")
                        return index, monitor
                print(f"Window {window_id} not found on any monitor.")
                return None, None
        except Exception as e:
            print(f"Error determining monitor for window {window_id}: {e}")
            return None, None

    def switch_window(self, window_title="My Permanent Tab"):
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
            return None
        try:
            time.sleep(1)
            # Search for windows with partial title match
            result = subprocess.run(
                ['xdotool', 'search', '--name', window_title],
                capture_output=True, text=True
            )
            window_ids = result.stdout.strip().split()
            if not window_ids:
                print(f"No window found with title containing: {window_title}")
                return None
            print("Available window IDs:", window_ids)
            for wid in window_ids:
                title = subprocess.run(
                    ['xdotool', 'getwindowname', wid],
                    capture_output=True, text=True
                ).stdout.strip()
                if window_title.lower() in title.lower():
                    # Determine which monitor the window is on
                    monitor_index, monitor = self.get_window_monitor(wid)
                    if monitor_index is not None:
                        # Move to monitor 1 (example: adjust coordinates based on monitor 1)
                        monitor_x, monitor_y = monitor['left'], monitor['top']
                        subprocess.run(['xdotool', 'windowmove', wid, str(monitor_x), '0'])
                        subprocess.run(['xdotool', 'windowactivate', wid])
                        print(f"Switched and moved window {wid} to monitor {monitor_index}: {window_title}")
                        time.sleep(0.5)
                        return wid
            print(f"No window found with title containing: {window_title}")
            return None
        except Exception as e:
            print(f"Error switching window with xdotool: {e}")
            return None
def get_window_mgr():
    window_mgr = WindowManager()
    return window_mgr
window_mgr = get_window_mgr()
def get_switch_window(window_title="My Permanent Tab"):
    return window_mgr.switch_window(window_title=window_title)
def get_screenshot_specific_screen(output_file="new_screen.png",
                                   monitor_index=1):
    return window_mgr.screenshot_specific_screen(output_file=output_file,
                                                      monitor_index=monitor_index)
def get_window_monitor(window_id=1):
    return window_mgr.get_window_monitor(window_id)
