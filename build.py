
import os
import sys
import shutil
import subprocess
import platform

def build_executable():
    """Build the executable using PyInstaller"""
    print("Starting build process...")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Define build options
    app_name = "Movie Awards Oracle"
    main_script = "src/main.py"
    
    # Create clean build directory
    if os.path.exists("build"):
        print("Cleaning build directory...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("Cleaning dist directory...")
        shutil.rmtree("dist")
    
    # Create PyInstaller command
    pyinstaller_options = [
        "--name", app_name,
        "--onefile",    # Single executable file
        "--windowed",   # No console window in Windows
        "--clean",      # Clean PyInstaller cache
    ]
    
    # Add Python source files
    python_files = [
        "src/main.py",
        "src/gui.py",
        "src/database.py",
        "src/models.py",
        "src/utils.py"
    ]
    
    for file in python_files:
        if os.path.exists(file):
            base_dir = os.path.dirname(file)
            pyinstaller_options.extend(["--add-data", f"{file}{os.pathsep}{base_dir}"])
    
    # Add icon if available
    icon_path = "oscar_icon.ico"
    if os.path.exists(icon_path):
        pyinstaller_options.extend(["--icon", icon_path])
    
    pyinstaller_options.append(main_script)
    
    # Run PyInstaller
    print("Running PyInstaller with options:", pyinstaller_options)
    subprocess.check_call([sys.executable, "-m", "PyInstaller"] + pyinstaller_options)
    
    print(f"Build completed. Executable created in dist/{app_name}")
    
    # Additional steps for different platforms
    if platform.system() == "Windows":
        print(f"Windows executable: dist/{app_name}.exe")
    elif platform.system() == "Darwin":
        print(f"macOS application: dist/{app_name}.app")
    else:
        print(f"Linux executable: dist/{app_name}")

if __name__ == "__main__":
    build_executable()
