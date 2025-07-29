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
def get_manager_defs(file_path):
    texts = read_From_file(file_path):
    from abstract_utilities import eatAll
    all_funcs = []
    for text in texts.split('def ')[1:]:
        title_spl = text.split('(')
        func_name = title_spl[0]
        variables = title_spl[1].split(')')[0].replace('\n','').split(',')
        variables = [eatAll(str(variable),['',' ','\n','\t']) for variable in variables]
        kwargs={}
        for i,variable in enumerate(variables):
            
            key = variable.split('=')[0].split(':')[0]
            if key != 'self':
                value = variable.split(':')[0].split('=')[-1]
                if key == value:
                    value == None
                    kwargs[key]=value
        var_strings=[]
        var_strings2=[]
        
        for key,value in kwargs.items():
            key=eatAll(key,['',' ','\n','\t'])
            value=eatAll(value,['',' ','\n','\t'])
            var_strings.append(f"{key}={value}")
            var_strings2.append(f"{key}={key}")
        var_string = f"({','.join(variables)})"
        var_strings2 = f"({','.join(var_strings2)})"
        all_funcs.append(f"""def {func_name}{var_string}:
        return clipboard.{func_name}{var_strings2}""")
    return '\n\n'.join(all_funcs)
