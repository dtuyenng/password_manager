import sys
import os

def get_resource_path(filename):
    # If the script is running in a PyInstaller bundle
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def get_save_path(filename):
    # Always save to the script directory, not to the temporary PyInstaller directory
    print(f"Local directory: {os.path.join(os.path.dirname(__file__), filename)}")
    return os.path.join(os.path.dirname(__file__), filename)


def show_paths():
    print(f"resource path: {get_resource_path("data.bin")}")
    print(f"save path: {get_save_path("data.bin")}")
    if get_save_path("data.bin") == get_resource_path("data.bin"):
        print("Same Path")
    else:
        print("Different Path")
