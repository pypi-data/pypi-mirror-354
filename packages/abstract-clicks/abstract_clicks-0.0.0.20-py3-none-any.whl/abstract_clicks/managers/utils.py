from ..imports import *
from ..managers.clipboardManager import get_open_browser_tab
def switch_window(window_title="My Permanent Tab"):
    """Switch to a window by partial title match (Linux with xdotool)."""
    get_open_browser_tab(url='https://chatgpt.com', title="chatgpt")
    if platform.system() != 'Linux':
        # Fallback to Alt+Tab for non-Linux
        modifier = 'command' if platform.system() == 'Darwin' else 'alt'
        try:
            get_auto_gui().keyDown(modifier)
            time.sleep(0.1)
            get_auto_gui().press('tab')
            time.sleep(0.1)
            get_auto_gui().keyUp(modifier)
            print("Switched to first window (non-Linux fallback)")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error switching window: {e}")
        return

    try:
        # Find window ID by partial title match
        result = subprocess.run(
            ['xdotool', 'search', '--name', window_title],
            capture_output=True, text=True
        )
        window_ids = result.stdout.strip().split()
        
        if not window_ids:
            print(f"No window found with title containing: {window_title}")
            return
        
        # Activate the first matching window
        subprocess.run(['xdotool', 'activate', window_ids[0]])
        print(f"Switched to window with title containing: {window_title}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error switching window with xdotool: {e}")
