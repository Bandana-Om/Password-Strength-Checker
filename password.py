import random
import re
import string
import tkinter as tk
from tkinter import ttk


def evaluate_password(password):
    """Return a score, label, color, and feedback for the given password."""
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        feedback.append("Use at least 12 characters for a stronger password.")
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one number.")

    if re.search(r"[!@#$%^&*()_+\-={}\[\]:;]", password):
        score += 1
    else:
        feedback.append("Include at least one special character.")

    if re.search(r"(.)\\1\\1", password):
        feedback.append("Avoid repeated characters in a row.")

    if password.lower() in {"password", "123456", "qwerty", "admin"}:
        feedback.append("Avoid common passwords.")

    if score <= 3:
        label = "Weak"
        color = "#CE0C0C"
    elif score <= 5:
        label = "Medium"
        color = "#f59e0b"
    else:
        label = "Strong"
        color = "#10b981"

    percentage = min(100, score * 20)
    return {
        "score": score,
        "label": label,
        "color": color,
        "percentage": percentage,
        "feedback": feedback if feedback else ["Excellent password strength!"],
    }


def update_strength(*args):
    """Refresh the strength meter, label, and feedback while typing."""
    password = entry_password.get()
    result = evaluate_password(password)

    progress_bar["value"] = result["percentage"]
    strength_label.config(text=result["label"], foreground=result["color"])
    strength_label.config(font=("Segoe UI", 12, "bold"))

    if not password:
        progress_bar["value"] = 0
        feedback_text.delete("1.0", tk.END)
        feedback_text.insert(tk.END, "Start typing to evaluate your password.")
        return

    feedback_text.delete("1.0", tk.END)
    for line in result["feedback"]:
        feedback_text.insert(tk.END, f"• {line}\n")


def toggle_visibility():
    """Show or hide the password text."""
    if show_var.get():
        entry_password.config(show="")
    else:
        entry_password.config(show="•")


def generate_password():
    """Create a strong password and insert it into the field."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = "".join(random.choice(alphabet) for _ in range(14))
        if evaluate_password(password)["label"] == "Strong":
            break
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    update_strength()


# Build the main window
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("520x480")
root.configure(bg="#0f172a")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background="#0f172a")
style.configure("TLabel", background="#0f172a", foreground="#e2e8f0")
style.configure("TButton", padding=6)
style.configure("Accent.TButton", background="#2563eb", foreground="white")

# Main card container
main_frame = ttk.Frame(root, padding=24)
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="Password Strength Checker", font=("Segoe UI", 20, "bold"))
title_label.pack(anchor=tk.W, pady=(0, 8))

subtitle = ttk.Label(main_frame, text="Create a secure password with live feedback and guidance.", font=("Segoe UI", 10))
subtitle.pack(anchor=tk.W, pady=(0, 16))

# Password entry row
entry_frame = ttk.Frame(main_frame)
entry_frame.pack(fill=tk.X, pady=(0, 10))

entry_password = tk.Entry(entry_frame, font=("Segoe UI", 13), bd=0, highlightthickness=1, relief="solid", bg="#111827", fg="#f9fafb", insertbackground="#f9fafb")
entry_password.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
entry_password.bind("<KeyRelease>", update_strength)

show_var = tk.BooleanVar(value=False)
show_button = ttk.Checkbutton(entry_frame, text="Show", variable=show_var, command=toggle_visibility)
show_button.pack(side=tk.LEFT, padx=(8, 0))

# Strength meter
meter_frame = ttk.Frame(main_frame)
meter_frame.pack(fill=tk.X, pady=(8, 4))

strength_label = ttk.Label(meter_frame, text="Waiting for input", font=("Segoe UI", 12, "bold"))
strength_label.pack(anchor=tk.W)

progress_bar = ttk.Progressbar(meter_frame, orient=tk.HORIZONTAL, length=430, mode="determinate", maximum=100)
progress_bar.pack(fill=tk.X, pady=(6, 0))

# Feedback box
feedback_label = ttk.Label(main_frame, text="Detailed Feedback", font=("Segoe UI", 11, "bold"))
feedback_label.pack(anchor=tk.W, pady=(14, 6))

feedback_text = tk.Text(main_frame, height=8, width=50, bg="#111827", fg="#e5e7eb", bd=0, highlightthickness=1, relief="solid")
feedback_text.pack(fill=tk.BOTH, expand=True)
feedback_text.configure(font=("Segoe UI", 10))
feedback_text.insert(tk.END, "Start typing to evaluate your password.")
feedback_text.config(state=tk.DISABLED)

# Action buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=(12, 0))

generate_button = ttk.Button(button_frame, text="Generate Password", command=generate_password)
generate_button.pack(side=tk.LEFT)

root.mainloop()


