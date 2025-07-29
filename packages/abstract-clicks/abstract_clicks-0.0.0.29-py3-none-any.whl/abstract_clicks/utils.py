import os
import time
import json,math
from typing import Any, Dict, List, Optional, Tuple
from abstract_utilities import SingletonMeta, os, safe_dump_to_file, safe_load_from_file
from pynput import mouse, keyboard
import time, json, sys, os
from random import uniform
# Lazy-loaded modules
auto_gui: Any = None
_user_input_window: Any = None




class getAutoGui:
    def __init__(self):
        
        self.py_auto_gui = None
    def import_auto_gui(self):
        import pyautogui
        return pyautogui
    def get_auto_gui(self):
        if self.py_auto_gui == None:
            self.py_auto_gui = self.import_auto_gui()
        return self.py_auto_gui
class getUserInput:
    def __init__(self):
        
        self.getUserInputwindow = None
    def user_input_window(self):
        from abstract_gui import getUserInputwindow
        return getUserInputwindow
    def get_user_input_window(self):
        if self.getUserInputwindow == None:
            self.getUserInputwindow = self.user_input_window()
        return self.getUserInputwindow


def get_auto_gui():
    auto_gui_mgr = getAutoGui()
    return auto_gui_mgr.get_auto_gui()
def get_user_input():
    user_input_mgr = getUserInput()
    return user_input_mgr.get_user_input_window()
def get_user_input_window():
    getUserInputwindow = get_user_input()
    prompt="please enter the event type"
    title="event type"
    exitcall, event_type = getUserInputwindow(prompt=prompt,
                                              title=title)

    return exitcall, event_type



# Path utilities
def abs_path(path: str) -> str:
    return os.path.abspath(path)


def abs_dir(path: str = __file__) -> str:
    return os.path.dirname(abs_path(path))


def get_rel_dir():
    rel_dir = os.getcwd()
    return rel_dir

def get_rel_path(path):
    rel_dir = get_rel_dir()
    return os.path.join(rel_dir, path)

def resolve_events_path(path, default=None):
    path = path or default or get_rel_path("session.json")
    dirname = os.path.dirname(path)
    if os.path.exists(path):
        return path
    dirname = os.path.dirname(path)
    if dirname and os.path.isdir(dirname):
        return path
    return get_rel_path(path)


# Time utilities
def now() -> float:
    return time.time()


def elapsed(start: float) -> float:
    return now() - start


class EventsRecorder(metaclass=SingletonMeta):
    """
    Singleton for recording and replaying mouse/keyboard events.
    """

    def __init__(
        self,
        events_path: Optional[str] = None,
        start_time: Optional[float] = None,
        refresh: bool = False
    ):
        if refresh:
            self.initialized = False

        if not getattr(self, 'initialized', False):
            self.initialized = True
            self.events_path = resolve_events_path(events_path)
            self.start_time = start_time or now()
            self.events: List[Dict[str, Any]] = []
            self.all_events: Dict[str, List[Dict[str, Any]]] = {}
            self.mouse_listener: Optional[mouse.Listener] = None
            self.keyboard_listener: Optional[keyboard.Listener] = None
            self.default_events_path = os.path.join(abs_dir(),'default_events.json')
    def record_event(self, evt_type: str, **data) -> None:
        self.events.append({
            "time": elapsed(self.start_time),
            "type": evt_type,
            **data
        })

    # Mouse callbacks
    def on_move(self, x: int, y: int) -> None:
        self.record_event("mouse_move", x=x, y=y)

    def on_click(
        self, x: int, y: int, button: Any, pressed: bool
    ) -> None:
        self.record_event(
            "mouse_click",
            x=x,
            y=y,
            button=button.name,
            pressed=pressed
        )

    def on_scroll(
        self, x: int, y: int, dx: int, dy: int
    ) -> None:
        self.record_event("mouse_scroll", x=x, y=y, dx=dx, dy=dy)

    # Keyboard callbacks
    def on_press(self, key: Any) -> None:
        try:
            k = key.char
        except AttributeError:
            k = str(key)
        self.record_event("key_press", key=k)

    def on_release(self, key: Any) -> Optional[List[Dict[str, Any]]]:
        try:
            k = key.char
        except AttributeError:
            k = str(key)
        self.record_event("key_release", key=k)
        if key == keyboard.Key.esc:
            # Save under 'default'
            self.all_events['default'] = self.events
            safe_dump_to_file(self.all_events, self.default_events_path)
            print(f"Saved {len(self.events)} events under 'default' to {self.events_path}")
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            if self.mouse_listener:
                self.mouse_listener.stop()
            return self.events

    def _ensure_listeners(self) -> None:
        if not self.mouse_listener:
            self.mouse_listener = mouse.Listener(
                on_move=self.on_move,
                on_click=self.on_click,
                on_scroll=self.on_scroll
            )
            self.mouse_listener.start()
        if not self.keyboard_listener:
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            self.keyboard_listener.start()

    def start_recording(self) -> str:
        print("⏺️ Recording... Press Esc to stop and save.")
        self.start_time = now()
        self.events.clear()
        self._ensure_listeners()
        while (
            self.mouse_listener and self.mouse_listener.running and
            self.keyboard_listener and self.keyboard_listener.running
        ):
            time.sleep(0.1)
        return self.default_events_path


    def _preprocess_events(self, events: List[Dict], speed_factor: float, min_move_distance: float) -> List[Dict]:
        """Preprocess events to set target times and filter small mouse movements."""
        processed_events = []
        last_x, last_y = None, None

        for e in events:
            # Create a copy of the event with adjusted target time
            event = e.copy()
            event['target_time'] = e['time'] / speed_factor
            
            # Filter mouse_move events based on distance
            if event['type'] == 'mouse_move':
                x, y = event['x'], event['y']
                event['x'] = uniform(x*.995, x*1.005)
                event['y'] = uniform(y*.995, y*1.005)
                if last_x is not None and last_y is not None:
                    distance = math.sqrt((event['x'] - last_x)**2 + (event['y'] - last_y)**2)
                    if distance < uniform(min_move_distance*.995, min_move_distance*1.005):
                        continue
                last_x, last_y = x, y
            elif event['type'] in ['mouse_click', 'mouse_scroll']:
                last_x, last_y = event.get('x'), event.get('y')

            processed_events.append(event)

        return processed_events
    def replay(self, event_type: str, speed_factor: float = 11.0, min_move_distance: float = 50) -> None:
        records = safe_load_from_file(self.events_path) or {}
        events = records.get(event_type, [])

        if not events:
            print(f"No events found for event_type '{event_type}' in {self.events_path}")
            return

        # Preprocess events to set target times and filter movements
        processed_events = self._preprocess_events(events, speed_factor, min_move_distance)
        print(f"Replaying {len(processed_events)} events (filtered from {len(events)})")

        stop_flag = False
        def on_abort(key: Any) -> bool:
            nonlocal stop_flag
            if key == keyboard.Key.esc:
                stop_flag = True
                return False
            return True

        abort_listener = keyboard.Listener(on_press=on_abort)
        abort_listener.start()

        gui = get_auto_gui()
        start_ts = now()

        for e in processed_events:
            if stop_flag:
                print("Replay aborted.")
                break

            # Wait until the target time is reached
            target_time = e['target_time']
            elapsed = now() - start_ts
            delay = target_time - elapsed

            if delay > 0:
                time.sleep(delay)

            et = e['type']
            if et == 'mouse_move':
                gui.moveTo(e['x'], e['y'])
            elif et == 'mouse_click':
                if e['pressed']:
                    gui.mouseDown(
                        e['x'], e['y'], button=e.get('button', 'left')
                    )
                else:
                    gui.mouseUp(
                        e['x'], e['y'], button=e.get('button', 'left')
                    )
            elif et == 'mouse_scroll':
                gui.scroll(
                    e.get('dy', 0), x=e.get('x', 0), y=e.get('y', 0)
                )
            elif et == 'key_press':
                gui.keyDown(e['key'])
            elif et == 'key_release':
                gui.keyUp(e['key'])

        abort_listener.stop()
        abort_listener.join()
        if not stop_flag:
            print("Replay finished.")


# Module API

def update_events_record(events_path,default_path):
    event_typ,exit_call = get_user_input_window()
    input(event_typ)
    if not os.path.isfile(events_path):
        safe_dump_to_file(data={}, file_path=events_path)
    events_record = safe_load_from_file(events_path) or {}
    default_events_record = safe_load_from_file(default_path) or {}
    events_record[event_typ or "default"] = default_events_record.get("default")
    input(events_path)
    safe_dump_to_file(data=events_record, file_path=events_path)
    return exit_call,events_record
def record_session(
    events_file: Optional[str] = None
) -> str:
    """
    Record events, then prompt for an event type and save mapping.
    """
    rec = EventsRecorder(events_path=events_file, refresh=True)
    default_path = rec.start_recording()
    exit_call,events_record = update_events_record(rec.events_path,default_path)
    return exit_call,events_record


def replay_session(
    event_type: str,
    events_file: Optional[str] = None
) -> None:
    rec = EventsRecorder(events_path=events_file)
    rec.replay(event_type)


