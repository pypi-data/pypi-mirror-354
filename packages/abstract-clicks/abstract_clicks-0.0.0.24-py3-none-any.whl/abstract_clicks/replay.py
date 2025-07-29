from pynput import mouse, keyboard
import time,json,sys,os
from abstract_utilities import safe_load_from_file
import pyautogui
# ——— Globals ———
def get_abs_file():
    return os.path.abspath(__file__)
def get_abs_dir():
    abs_file = get_abs_file()
    return os.path.dirname(abs_file)
def get_abs_path(path):
    abs_dir = get_abs_dir()
    return os.path.join(abs_dir,path)
def get_rel_dir():
    rel_dir = os.getcwd()
    return rel_dir
def get_rel_path(path):
    rel_dir = get_abs_dir()
    return os.path.join(rel_dir,path)

def get_events_path(path=None,default=None):
    path = path or default or "session.json"
    if os.path.exists(path):
        return path
    dirname = os.path.dirname(path)
    if dirname and os.path.isdir(dirname):
        return path
    return get_rel_path(path)
def get_time():
    return time.time()
def get_time_span(start_time):
    time_span = get_time() - start_time
    return time_span
def replay_actions(event_type,
                   _stop_replay=False,
                   refresh=False,
                   events_path=None,
                   all_events=None,
                   start_time=None):
    # load recorded events
    events_path = get_events_path(path=events_path)
    events_record = safe_load_from_file(events_path)
    events = events_record.get(event_type, [])
   
    # flag to tell us to stop early
    _stop_replay = False

    # define the on_press callback for replay
    def _on_press(key):
        if key == keyboard.Key.esc:
            _stop_replay = True
            # stop this listener
            return False

    # start listening for Esc in the background
    listener = keyboard.Listener(on_press=_on_press)
    listener.start()

    start_ts = time.time()
    for e in events:
        # if Esc was pressed, break out
        if _stop_replay:
            print("Replay aborted by user (Esc pressed).")
            break

        # wait until it's time for this event
        delay = e["time"] - (time.time() - start_ts)
        if delay > 0:
            time.sleep(delay)

        et = e["type"]
        if et == "mouse_move":
            pyautogui.moveTo(e["x"], e["y"])
        elif et == "mouse_click":
            btn = e.get("button", "left")
            if e["pressed"]:
                pyautogui.mouseDown(e["x"], e["y"], button=btn)
            else:
                pyautogui.mouseUp(e["x"], e["y"], button=btn)
        elif et == "mouse_scroll":
            pyautogui.scroll(e["dy"], x=e["x"], y=e["y"])
        elif et == "key_press":
            pyautogui.keyDown(e["key"])
        elif et == "key_release":
            pyautogui.keyUp(e["key"])
    return _stop_replay
