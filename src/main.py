
import tkinter as tk
import sys
import os
import traceback

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
        from tkinter import messagebox
        messagebox.showerror(
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
    
    # Add the current directory to Python path to ensure modules can be found
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Now import the GUI module
    try:
        from gui import OscarsAppGUI
    except ImportError as e:
        print(f"Error importing GUI module: {e}")
        if hasattr(sys, '_MEIPASS'):
            print(f"MEIPASS directory contents: {os.listdir(sys._MEIPASS)}")
        sys.exit(1)
    
    # Create the main window
    root = tk.Tk()
    root.title("Movie Awards Oracle")
    
    # Set app icon
    try:
        icon_path = resource_path("oscar_icon.ico")
        root.iconbitmap(icon_path)
        print(f"Icon loaded from: {icon_path}")
    except Exception as e:
        print(f"Failed to load icon: {e}")
        # Continue without the icon
        pass
    
    # Create the app GUI
    try:
        app = OscarsAppGUI(root)
    except Exception as e:
        print(f"Error creating GUI: {e}")
        traceback.print_exc()
        sys.exit(1)
    
    # Start the main event loop
    try:
        root.mainloop()
    except Exception as e:
        print(f"Error in main loop: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
