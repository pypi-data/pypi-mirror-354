import tkinter as tk
from tkinter import messagebox
import json
import importlib.resources
from pathlib import Path

from myApp.test_display import display_me

APP_DIR = Path.home() / ".radis-app"
APP_DIR.mkdir(exist_ok=True)
USER_CONFIG_PATH = APP_DIR / "license_config.json"


def ensure_user_config():
    if not USER_CONFIG_PATH.exists():
        # Load default config from package and copy it
        default_config_path = importlib.resources.files("myApp.data").joinpath("license_config.json")
        default_data = json.loads(default_config_path.read_text(encoding="utf-8"))
        with USER_CONFIG_PATH.open("w", encoding="utf-8") as file:
            json.dump(default_data, file, indent=2)


def update_user_config(new_data: dict):
    ensure_user_config()
    with USER_CONFIG_PATH.open("w", encoding="utf-8") as file:
        json.dump(new_data, file, indent=2)


def load_agreement_status():
    """Load the license agreement status from the config file."""
    try:
        # Check if file exists
        ensure_user_config()
        with open(USER_CONFIG_PATH, "r", encoding="utf-8") as config_file:
            content = config_file.read()
            if content:
                config = json.loads(content)
                return config.get("license_accepted")
            else:
                print("Config file is empty")
                return False

        # config_file = importlib.resources.files("myApp.data").joinpath("license_config.json")
        # if config_file.is_file():
        #     # Read content
        #     with importlib.resources.files("myApp.data").joinpath("license_config.json").open("r") as CONFIG_FILE:
        #         content = config_file.read_text(encoding="utf-8").strip()
        #         if content:
        #             config = json.load(CONFIG_FILE)
        #             return config.get("license_accepted")
        #         else:
        #             print("Config file is empty.")
        #             return False
        # else:
        #     print("config.json does not exist in the package.")
        #     return False

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
        update_user_config(config_data)

        # with importlib.resources.files("myApp").joinpath("config.json").open("r") as config_text:
        #     json.dump(config_data, config_text, indent=2)

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


def simple_gui(name, display_text):
    root = tk.Tk()
    root.title(name)
    root.geometry("500x400")

    # Screen display
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill="both", expand=True)

    text_widget = tk.Text(frame, wrap="word", height=18)
    text_widget.delete(1.0, tk.END)  # Clear previous content
    text_widget.insert(tk.END, display_text)

    def ok_pressed():
        text_widget.delete(1.0, tk.END)  # Clear previous content
        text_widget.insert(tk.END, "Goodbye! :)")

    def exit_pressed():
        messagebox.showinfo("Sad Times", ";(")
        exit(0)

    text_widget.config(state="normal")
    text_widget.pack(expand=True, fill="both")

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="OK", command=ok_pressed, width=12).pack(side="left", padx=10)
    tk.Button(button_frame, text="Exit", command=exit_pressed, width=12).pack(side="left", padx=10)

    root.mainloop()


def main():
    if show_eula_gui():
        display_text = display_me()
        simple_gui("Hello World!", display_text)



# file = load_license()
# print(file)

