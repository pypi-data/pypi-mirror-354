import tkinter as tk
from itertools import filterfalse
from tkinter import messagebox
import os
import json

CONFIG_FILE = "license_config.json"


def load_agreement_status():
    """Load the license agreement status from the config file."""
    if os.path.exists(CONFIG_FILE):
        if os.path.getsize(CONFIG_FILE) > 0:
            with open(CONFIG_FILE, "r") as file:
                config = json.load(file)
                return config.get("license_accepted")
        else:
            print("Config file is empty")
            return False
    else:
        print("Config file does not exist")
        return False

def save_agreement_status(agreed):
    """Save the license agreement status to the config file."""

    key_name  = "license_agreed"
    config_data = {
        "key_name" : key_name,
        "license_accepted" : agreed
    }

    if agreed:
        with open(CONFIG_FILE, "w") as config_text:
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

    if os.path.exists("../LICENSE"):
        license_file = open("../LICENSE", 'r')
        formal_license = license_file.read()
        text_widget.delete(1.0, tk.END)  # Clear previous content
        text_widget.insert(tk.END, formal_license)
    else:
        print("LICENSE file does not exist")
        return False

    if os.path.exists("../EULA"):
        eula_file = open("../EULA", 'r')
        eula_license = eula_file.read()
        text_widget.insert(tk.END, eula_license)
    else:
        print("EULA file does not exist")
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

