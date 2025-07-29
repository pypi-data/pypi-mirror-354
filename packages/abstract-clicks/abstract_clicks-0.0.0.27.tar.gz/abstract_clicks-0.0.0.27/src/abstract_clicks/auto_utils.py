from src import *
clipboard = get_clipboard()
#monitors = get_monitors()
#for monitor_index,monitor in  enumerate(monitors):

AUTO_DICTS = {
    "prompt":{"text":
              ['ask',' ','anything'],
              "image":[],
              "functions":
              [get_paste_in_prompt]
              },
    "enter":{"text":
             [],
             "image":
             ["/home/computron/Pictures/Screenshots/Screenshot from 2025-06-09 06-37-25.png"],
             "functions":
             [get_html_inspect]
             },
    "inspect":{"text":
               ['ask',' ','anything'],"image":[],
               "functions":
               [get_html_inspect]
               }
    }


def get_browser_tab_and_index(url,title):
    get_open_browser_tab(url=url, title=title)
    wid,monitor_index = get_switch_window(window_title=title)
    return wid,monitor_index
def get_gpt_browser():
    wid,monitor_index = get_browser_tab_and_index(url='https://chatgpt.com',
                          title="chatgpt")
    return wid,monitor_index
def get_all_pointer_functions():
    for key,auto_dict in auto_dicts.items():
def get_pointer_function(key=None,
                         text=None,
                         image=None,
                         functions=None,
                         index=None,
                         output_file=None):
    if key:
        audo_dict = AUTO_DICTS.get(key)
    if audo_dict:
        text = auto_dict.get('text',[])
        target_image = auto_dict.get('image',[])
        functions = auto_dict.get('functions',[])
    target_text = text or []
    target_image = target_image or []
    functions = functions or []
    monitor_index = index or 1
    output_file = output_file or 'snapshot.png'
    scnShtMgr = screenshotManager(output_file=output_file,
                                  monitor_index=monitor_index,
                                  functions=functions,
                                  target_image=target_image,
                                  target_text=target_text)

    

    

