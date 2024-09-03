import pyautogui
import Quartz
from AppKit import NSScreen

def get_displays():
    return [screen.frame() for screen in NSScreen.screens()]

def get_all_visible_windows():
    windows = []
    for window in Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID):
        if window.get('kCGWindowLayer') == 0 and window.get('kCGWindowOwnerName') != 'Window Server':  # Exclude the desktop window
            windows.append(window)
    return windows

def rotate_windows():
    displays = get_displays()
    windows = get_all_visible_windows()

    # Create a map from current display to the next one (circular)
    num_displays = len(displays)
    next_display_map = {i: (i + 1) % num_displays for i in range(num_displays)}

    for window in windows:
        window_rect = window['kCGWindowBounds']
        window_center = (window_rect['X'] + window_rect['Width'] / 2, window_rect['Y'] + window_rect['Height'] / 2)

        # Find which display this window is currently on
        current_display_index = None
        for i, display in enumerate(displays):
            if (display.origin.x <= window_center[0] <= display.origin.x + display.size.width) and (display.origin.y <= window_center[1] <= display.origin.y + display.size.height):
                current_display_index = i
                break

        if current_display_index is None:
            continue  # Skip if we can't determine the display

        # Determine the target display
        target_display_index = next_display_map[current_display_index]
        target_display = displays[target_display_index]

        # Calculate the new position on the target display
        new_x = target_display.origin.x + (window_rect['Width'] / 2)
        new_y = target_display.origin.y + (window_rect['Height'] / 2)

        # Move the window using pyautogui
        pyautogui.moveTo(window_rect['X'], window_rect['Y'])
        pyautogui.dragTo(new_x, new_y, duration=1)  # Duration is the time taken for the move


if __name__ == "__main__":
    rotate_windows()
