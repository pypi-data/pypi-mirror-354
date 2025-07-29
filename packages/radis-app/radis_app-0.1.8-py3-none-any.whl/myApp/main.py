import tkinter as tk
from fileinput import filename
from itertools import filterfalse
from tkinter import messagebox
import os
import json
import importlib.resources



def load_agreement_status():
    """Load the license agreement status from the config file."""
    try:
        # Check if file exists
        config_file = importlib.resources.files("myApp").joinpath("config.json")
        if config_file.is_file():
            # Read content
            with importlib.resources.files("myApp").joinpath("config.json").open("r") as CONFIG_FILE:
                content = config_file.read_text(encoding="utf-8").strip()
                if content:
                    config = json.load(CONFIG_FILE)
                    return config.get("license_accepted")
                else:
                    print("Config file is empty.")
                    return False
        else:
            print("config.json does not exist in the package.")
            return False

    except FileNotFoundError:
        print("config.json not found.")
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def save_agreement_status(agreed):
    """Save the license agreement status to the config file."""

    key_name  = "license_agreed"
    config_data = {
        "key_name" : key_name,
        "license_accepted" : agreed
    }

    if agreed:
        with importlib.resources.files("myApp").joinpath("config.json").open("r") as config_text:
            json.dump(config_data, config_text, indent=2)

    # with open(CONFIG_FILE) as f:
    #     print(f.read())


def show_eula_gui():
    """Display the EULA GUI and record the user's response."""

    # If the user has already agreed, don't show the EULA again
    if load_agreement_status():
        print("License already agreed")
        return True

    root = tk.Tk()
    root.title("License Agreement")
    root.geometry("500x400")

    agreed = tk.BooleanVar(value=False)  # ✅ Move this AFTER tk.Tk()

    def on_agree():
        save_agreement_status(True)
        agreed.set(True)
        root.destroy()

    def on_disagree():
        messagebox.showinfo("Agreement Required", "You must agree to the license to use this software.")
        save_agreement_status(False)
        root.destroy()
        exit(0)

    # Screen display
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    text_widget = tk.Text(frame, wrap="word", height=18)

    #ANOTHER DISPLAY - ALSO GOOD
    # text_widget = tk.Text(root, wrap="word", width=40, height=10)
    # text_widget.pack(pady=10)

    license_file = importlib.resources.files("myApp.data").joinpath("LICENSE")
    if license_file.is_file():
        license_file = license_file.open("r", encoding="utf-8")
        formal_license = license_file.read()
        text_widget.delete(1.0, tk.END)  # Clear previous content
        text_widget.insert(tk.END, formal_license)

    else:
        print("LICENSE file does not exist.")
        return False

# This is how to get the file for packages
#        with importlib.resources.files("myApp.data").joinpath("LICENSE").open("r") as license_file:

    eula_file = importlib.resources.files("myApp.data").joinpath("EULA")
    if eula_file.is_file():
        eula_file = eula_file.open("r", encoding="utf-8")
        eula_license = eula_file.read()
        text_widget.delete(1.0, tk.END)  # Clear previous content
        text_widget.insert(tk.END, formal_license)

    else:
        print("EULA file does not exist.")
        return False


    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both")

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="I Agree", command=on_agree, width=12).pack(side="left", padx=10)
    tk.Button(button_frame, text="I Do Not Agree", command=on_disagree, width=18).pack(side="left")

    root.mainloop()

    return agreed.get()


def main():
    show_eula_gui()

main()

# file = load_license()
# print(file)

