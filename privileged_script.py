import os
import ctypes
import sys

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin privileges: {e}")
        return False

def write_to_protected_directory():
    """Write a file to a protected directory (requires admin privileges)."""
    protected_dir = os.path.join(os.environ["SystemRoot"], "Temp")
    file_path = os.path.join(protected_dir, "admin_test.txt")
    
    try:
        # Ensure the directory exists
        if not os.path.exists(protected_dir):
            print(f"Directory does not exist: {protected_dir}")
            return
        
        # Write to the file
        with open(file_path, "w") as f:
            f.write("This file was created with administrator privileges.\n")
        print(f"File written successfully: {file_path}")
    except PermissionError:
        print("Error: Permission denied. Run the script as an administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

def run_as_admin():
    """Re-launch the script with administrator privileges."""
    try:
        # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"Failed to re-launch with admin privileges: {e}")

if __name__ == "__main__":
    if is_admin():
        # If running with admin privileges, write to the protected directory
        write_to_protected_directory()
    else:
        # If not running with admin privileges, re-launch the script
        print("Script is not running with administrator privileges. Re-launching...")
        run_as_admin()