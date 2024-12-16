import tkinter as tk
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk  # Ensure Pillow is installed with pip install Pillow

# Function to open registration.py
def open_registration():
    window.destroy()
    subprocess.run(['python3', 'registration.py'])

# Function to stop the program
def close_program():
    window.quit()

# Function to open login.py
def open_login():
    window.destroy()
    subprocess.run(['python3', 'login.py'])

# Create the GUI window
window = tk.Tk()
window.title("Welcome")

# Make the window full-screen and center it on the screen
window.attributes('-fullscreen', True)  # Full-screen for all platforms

# Add style for buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10, background="#2196F3", foreground="white")
style.map('TButton', background=[('active', '#1976D2')])

# Create a navigation bar
nav_frame = tk.Frame(window, bg='#2196F3', height=60)
nav_frame.pack(fill='x')

# Create buttons on the navigation bar
nav_title = tk.Label(nav_frame, text="EXAM", font=("Helvetica", 16), bg='#2196F3', fg='white')
nav_title.pack(side=tk.LEFT, padx=10, pady=10)

register_nav_button = ttk.Button(nav_frame, text="Register", command=open_registration, style='TButton')
register_nav_button.pack(side=tk.RIGHT, padx=10, pady=10)

login_nav_button = ttk.Button(nav_frame, text="Login", command=open_login, style='TButton')
login_nav_button.pack(side=tk.RIGHT, padx=10, pady=10)

close_nav_button = ttk.Button(nav_frame, text="Close", command=close_program, style='TButton')
close_nav_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a frame for the title
title_frame = tk.Frame(window, bg='#333')
title_frame.pack(fill='x')

# Create title label
title_label = tk.Label(title_frame, text="Welcome to Our EXAM", font=("Helvetica", 24), bg='#333', fg='white', pady=20)
title_label.pack()

# Create a frame to contain the images and center it
image_frame = tk.Frame(window, bg='#f0f0f0')
image_frame.place(relx=0.5, rely=0.5, anchor='center')

# Load and set full-screen image
def load_fullscreen_image(path):
    img = Image.open(path)
    img = img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)
    return ImageTk.PhotoImage(img)

image_fullscreen = load_fullscreen_image("1.jpg")

# Display full-screen image
image_label = tk.Label(window, image=image_fullscreen)
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bring navigation and title frames to the front
nav_frame.lift()
title_frame.lift()

# Create a footer
footer_frame = tk.Frame(window, bg='#333')
footer_frame.pack(fill='x', side='bottom')

footer_label = tk.Label(footer_frame, text="Created by Harsh Mandaliya", font=("Helvetica", 12), bg='#333', fg='white', pady=10)
footer_label.pack()

# Bring footer frame to the front
footer_frame.lift()

# Start the GUI
window.mainloop()
