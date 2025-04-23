
import tkinter as tk
import sys
import os
import traceback

from gui import OscarsAppGUI

def resource_path(relative_path):
    """Get absolute path to resource for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"Error: {error_msg}")
    
    # Show error in messagebox if GUI is initialized
    try:
        tk.messagebox.showerror(
            "Application Error", 
            f"An unexpected error occurred:\n\n{exc_value}\n\nPlease report this issue."
        )
    except:
        pass
    
    # Default exception handling
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def main():
    """Main entry point for the application"""
    # Set exception handler
    sys.excepthook = handle_exception
    
    # Create the main window
    root = tk.Tk()
    
    # Set app icon
    try:
        root.iconbitmap(resource_path("oscar_icon.ico"))
    except:
        # If icon not found, continue without it
        pass
    
    # Create the app GUI
    app = OscarsAppGUI(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
