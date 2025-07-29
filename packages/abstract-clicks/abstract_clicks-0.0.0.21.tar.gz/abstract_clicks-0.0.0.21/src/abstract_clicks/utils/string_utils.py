from ..imports import *
def lower_dict_string(dict_obj,key):
    dict_obj[f"{key}_lower"] = str(dict_obj[key]).lower()
    return dict_obj
def if_in_string(string=None,comp_string=None,typ=None):
    typ = typ or '='
    if comp_string and string:
        if typ == '=':
            if string == comp_string:
                return True
        elif typ == '+':
             if comp_string in string:
                return True   
        elif typ == '-':
            if string in comp_string:
                return True    
    return False

def get_dict_coords(best_dict,monitor_info):
    if best_dict:
        best_dict = best_dict[0]
        x = best_dict['x'] + best_dict['width'] // 2
        y = best_dict['y'] + best_dict['height'] // 2
        # Adjust for monitor offset
        if monitor_info:
            x += monitor_info['left']
            y += monitor_info['top']
        # Move mouse
        pyautogui.moveTo(x, y, duration=0.5)  # Smooth movement over 0.5s
        return True
def get_best_screenshot_dict(screenshot_file,monitor_index):
    monitor_index = monitor_index or 1
    monitor_info = clipboard.screenshot_specific_screen(screenshot_file,monitor_index)
    if monitor_info:
        dicts = clipboard.perform_ocr(screenshot_file=file_path,confidence_threshold=60)#clipboard.perform_ocr(file_path)
        texts = [text.get('text') for text in dicts]
        closest_match = get_closest_match_from_list(comp_obj=comp,total_list=texts,case_sensative=False)
        best_dict = [item for item in dicts if item.get('text') == closest_match]
        result = get_dict_coords(best_dict,monitor_info)
        return result
