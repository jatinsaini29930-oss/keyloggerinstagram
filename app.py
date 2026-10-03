import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime


LOG_FILE = Path("demo_keystrokes.txt")


class KeyLoggerDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Keylogger Demo")
        self.root.geometry("700x450")

        title = tk.Label(
            root,
            text="Safe Keylogger Simulator",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        info = tk.Label(
            root,
            text=(
                "Demo only — keystrokes are captured ONLY inside "
                "this text box."
            ),
            font=("Arial", 11)
        )
        info.pack(pady=5)

        self.status = tk.Label(
            root,
            text="Status: Recording",
            font=("Arial", 11)
        )
        self.status.pack(pady=5)

        self.textbox = tk.Text(
            root,
            height=12,
            width=75,
            font=("Consolas", 12)
        )
        self.textbox.pack(padx=20, pady=10)

        self.textbox.bind("<KeyPress>", self.record_key)

        buttons = tk.Frame(root)
        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="Save Log",
            command=self.save_log,
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons,
            text="Clear",
            command=self.clear_log,
            width=15
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            buttons,
            text="Exit",
            command=root.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=5)

    def record_key(self, event):
        # Intentionally limited to this application's Text widget.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if event.keysym == "space":
            key = "[SPACE]"
        elif event.keysym == "Return":
            key = "[ENTER]"
        elif event.keysym == "BackSpace":
            key = "[BACKSPACE]"
        elif len(event.char) == 1 and event.char.isprintable():
            key = event.char
        else:
            key = f"[{event.keysym}]"

        # Keep the demonstration visible in the app itself.
        self.status.config(
            text=f"Last key: {key}    Time: {timestamp}"
        )

    def save_log(self):
        content = self.textbox.get("1.0", tk.END).rstrip()

        if not content:
            messagebox.showinfo("Nothing to save", "The text box is empty.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(f"\n--- Demo session: {timestamp} ---\n")
            file.write(content)
            file.write("\n")

        messagebox.showinfo(
            "Saved",
            f"Demo text saved to:\n{LOG_FILE.resolve()}"
        )

    def clear_log(self):
        self.textbox.delete("1.0", tk.END)
        self.status.config(text="Status: Recording")


def main():
    root = tk.Tk()
    KeyLoggerDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
