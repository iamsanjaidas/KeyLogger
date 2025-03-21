Stealth Keylogger with Admin Privilege Check

This project consists of two Python scripts:

  Stealth Keylogger: A script that logs key presses to a file (keylog.txt) and runs in the background with a hidden console.

  Admin Privilege Check: A script that checks for administrator privileges and writes a test file to a protected directory (C:\Windows\Temp).

The scripts are designed for educational purposes only and should only be used in environments where you have explicit permission to run them.
Features

  Stealth Keylogger:

    Logs key presses to a file (keylog.txt).

    Hides the console window.

    Adds itself to Windows startup for persistence.

    Uses a low-level keyboard hook to capture key presses.

  Admin Privilege Check:

    Checks if the script is running with administrator privileges.

    Writes a test file to a protected directory (C:\Windows\Temp).

    Re-launches itself with administrator privileges if necessary.

Requirements

    Python 3.x

    Windows OS

    Libraries: ctypes, os, sys, time, datetime, winreg

Installation

    Clone or download the repository.

    Install the required libraries:
        pip install pyinstaller

Usage

    Stealth Keylogger:
        Run the script:
            python stealth_keylogger.py

        The script will:

            Hide the console window.

            Add itself to Windows startup.

            Log key presses to keylog.txt.

    Admin Privilege Check:

        Run the script:
            python admin_check.py

        The script will:

            Check for administrator privileges.

            Write a test file to C:\Windows\Temp if running as admin.

            Re-launch itself with admin privileges if necessary.
