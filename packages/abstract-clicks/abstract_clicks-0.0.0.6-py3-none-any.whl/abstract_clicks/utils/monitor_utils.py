from ..imports import *
def screenshot_specific_screen(output_file=None):
    """Capture a screenshot of a specific monitor."""
    try:
        with mss.mss() as sct:
            
                
                if monitor_index < 1 or monitor_index >= len(monitors):
                    print(f"Invalid monitor index: {monitor_index}. Available monitors: {len(monitors)-1}")
                    continue
                monitor = monitors[
                    monitor_index
                    ]
                
                sct_img = sct.grab(
                    monitor
                    )
                
                img = Image.frombytes(
                    "RGB",
                    sct_img.size,
                    sct_img.rgb
                    )
                output_file = output_file or os.path.join(
                    os.getcwd(),
                    f'screen_{monitor_index}.png'
                    )
                
                img.save(
                    output_file
                    )
                print(
                    f"Saved screenshot of monitor {monitor_index} to: {output_file}"
                    )
                return output_file
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

   
def highlight_text_on_screenshot(screenshot_path=None, bbox={},
                                 highlight_color=(
                                     0,
                                     255,
                                     0
                                     ),
                                 thickness=2,
                                 output_path=None
                                 ):
    """
    Displays a screenshot with a highlighted rectangle around the target text.

    :param screenshot_path: Path to the screenshot image file.
    :param bbox: A dict containing 'x', 'y', 'width', 'height' keys for the text bounding box.
    :param highlight_color: Tuple for the rectangle color in BGR (default green).
    :param thickness: Line thickness of the rectangle.
    :param output_path: If provided, saves the highlighted image to this path.
    """
    # Load image
    if not os.path.isfile(screenshot_path):
        screenshot_specific_screen(output_file=screenshot_path)
    img = cv2.imread(screenshot_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image at {screenshot_path}")

    # Coordinates for rectangle
    x, y = bbox['x'], bbox['y']
    w, h = bbox['width'], bbox['height']
    start_point = (x, y)
    end_point = (x + w, y + h)

    # Draw rectangle
    cv2.rectangle(img, start_point, end_point, highlight_color, thickness)

    # Convert BGR to RGB for matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Display with matplotlib
    plt.figure(figsize=(8, 6))
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.title('Highlighted Text')
    plt.show()

    # Optionally save
    if output_path:
        cv2.imwrite(output_path, img)

def get_monitor_texts_with_highlight(comp,screenshot_file,monitor_index):
    
    
        monitor_info = clipboard.screenshot_specific_screen(screenshot_file,
                                                            monitor_index)
        if monitor_info:
            dicts = clipboard.perform_ocr(screenshot_file=screenshot_file, confidence_threshold=60)
            texts = [text.get('text') for text in dicts]
            closest_match = get_closest_match_from_list(comp_obj=comp, total_list=texts, case_sensative=False)
            best_dicts = [item for item in dicts if item.get('text') == closest_match]
            if best_dicts:
                best = best_dicts[0]
                # Adjust for monitor offset
                best['x'] += monitor_info['left']
                best['y'] += monitor_info['top']
                # Highlight instead of moving mouse
                highlight_text_on_screenshot(screenshot_file, best)
                return True
    return False
def get_all_monitor_texts_with_highlight(comp,screenshot_file)
    monitors = sct.monitors
    for monitor_index,monitor in enumerate(sct.monitors):
        get_monitor_texts_with_highlight(comp,screenshot_file,monitor_index)
