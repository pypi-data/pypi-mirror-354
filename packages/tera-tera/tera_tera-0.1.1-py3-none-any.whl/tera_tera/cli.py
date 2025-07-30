import argparse

import os
import random
import json
from datetime import date
from pathlib import Path
import platform
import subprocess

# Constants
IMAGE_FOLDER = str(Path(__file__).parent / "assets")
HISTORY_FILE = str(Path.home() / ".tera_tera.json")


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {"dates": {}, "last_shown": None}


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def open_image(path):
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    elif platform.system() == "Windows":
        os.startfile(path)
    else:  # Linux
        subprocess.run(["xdg-open", path])


def main(args):
    today_str = str(date.today())

    history = load_history()
    image_files = [
        f
        for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if not image_files:
        print("No image files found.")
        return

    if today_str in history["dates"]:
        chosen_image = history["dates"][today_str]
    else:
        last_shown = history.get("last_shown")
        available_images = [img for img in image_files if img != last_shown]

        if not available_images:
            available_images = image_files  # fallback if only one image

        chosen_image = random.choice(available_images)
        history["dates"][today_str] = chosen_image
        history["last_shown"] = chosen_image
        save_history(history)

    image_path = os.path.join(IMAGE_FOLDER, chosen_image)
    print(f"Showing: {chosen_image}")
    open_image(image_path)


def create_parser():
    parser = argparse.ArgumentParser(
        description="Tera tera app to do langar seva at various gurudwara's"
    )
    return parser


def cli():
    "Tera tera app to do langar seva at various gurudwara's"
    parser = create_parser()
    args = parser.parse_args()
    main(args)
