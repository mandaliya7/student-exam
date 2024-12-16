import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
from tkcalendar import DateEntry
import re
from cryptography.fernet import Fernet
import pandas as pd
import os
import subprocess

# Load or generate the encryption key
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return key

key = load_key()
cipher = Fernet(key)

# Path to the CSV file to store user data
csv_file_path = 'users.csv'

# Ensure CSV file exists
if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=['Username', 'Email', 'Date_of_Birth', 'Password'])
    df.to_csv(csv_file_path, index=False)

# Function to validate email
def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@gmail\.com$", email))

# Function to validate password
def validate_password(password):
    return bool(re.match(r"^[a-zA-Z0-9]{8,12}$", password))

# Function to encrypt password
def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

# Function to handle registration
def register_user():
    username = username_entry.get()
    email = email_entry.get()
    date_of_birth = dob_entry.get_date().strftime('%d/%m/%Y')
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Validate username
    if not username:
        messagebox.showerror("Error", "Username is required!")
        return

    # Validate email format
    if not validate_email(email):
        messagebox.showerror("Error", "Please enter a valid Gmail address!")
        return

    # Validate passwords
    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    # Validate password complexity
    if not validate_password(password):
        messagebox.showerror("Error", "Password must be 8-12 characters long and contain only letters and numbers.")
        return

    # Encrypt password
    encrypted_password = encrypt_password(password)

    # Store user data in CSV
    user_data = {
        'Username': username,
        'Email': email,
        'Date_of_Birth': date_of_birth,
        'Password': encrypted_password
    }

    df = pd.read_csv(csv_file_path)

    # Convert the user_data dictionary to a DataFrame and concatenate it
    new_user_df = pd.DataFrame([user_data])
    df = pd.concat([df, new_user_df], ignore_index=True)

    df.to_csv(csv_file_path, index=False)

    messagebox.showinfo("Success", "Registration successful! Redirecting to login...")

    # Redirect to login after successful registration
    window.destroy()  # Close the registration window
    subprocess.run(['python3', 'login.py'])  # Execute login.py script

# Function to open login window
def open_login():
    window.destroy()
    subprocess.run(['python3', 'login.py'])

# Function to stop the program
def close_program():
    window.quit()

# Function to animate footer text
def animate_footer_text():
    x1, y1, x2, y2 = footer_label.bbox("all")
    if x2 < 0 or y2 < 0:  # If the text has moved out of the screen
        x1 = window.winfo_width()  # Reset the text position to start from the right
    footer_label.move("all", -2, 0)  # Move the text left
    window.after(100, animate_footer_text)

# Create the GUI window
window = tk.Tk()
window.title("User Registration")

# Make the window full-screen and center it on the screen
window.attributes('-fullscreen', True)  # Full-screen for all platforms

# Create a gradient background
canvas = tk.Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight())
canvas.pack(fill='both', expand=True)

# Create the gradient effect
for i in range(window.winfo_screenheight()):
    blue = 255 - int(i / (window.winfo_screenheight() / 255))  # Ensure the blue value stays within 0-255
    color = "#%02x%02x%02x" % (0, blue, 255)
    canvas.create_line(0, i, window.winfo_screenwidth(), i, fill=color)

# Create a frame to contain all the fields and center it
frame = tk.Frame(canvas, bg='#ffffff', bd=10, relief='ridge')
frame.place(relx=0.5, rely=0.5, anchor='center')

# Add style for buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 16), padding=10, background="#2196F3", foreground="white")
style.map('TButton', background=[('active', '#1976D2')])

# Create labels and entry fields inside the form
title_label = tk.Label(frame, text="Student Registration", font=("Helvetica", 24), bg='white', fg='blue')
title_label.grid(row=0, columnspan=2, pady=20)

tk.Label(frame, text="Username:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
username_entry = tk.Entry(frame, font=("Helvetica", 14))
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Email (Gmail only):", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
email_entry = tk.Entry(frame, font=("Helvetica", 14))
email_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame, text="Date of Birth:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=5, sticky='e')
dob_entry = DateEntry(frame, date_pattern='dd/mm/yyyy', font=("Helvetica", 14))
dob_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame, text="Password:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=5, sticky='e')
password_entry = tk.Entry(frame, show="*", font=("Helvetica", 14))
password_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(frame, text="Confirm Password:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=5, column=0, padx=10, pady=5, sticky='e')
confirm_password_entry = tk.Entry(frame, show="*", font=("Helvetica", 14))
confirm_password_entry.grid(row=5, column=1, padx=10, pady=5)

# Register button
register_button = ttk.Button(frame, text="Register", command=register_user, style='TButton')
register_button.grid(row=6, columnspan=2, padx=10, pady=10)

# Login button
login_button = ttk.Button(frame, text="Login", command=open_login, style='TButton')
login_button.grid(row=7, columnspan=2, padx=10, pady=10)

# Close button
close_button = ttk.Button(frame, text="Close", command=close_program, style='TButton')
close_button.grid(row=8, columnspan=2, pady=10)

# Create a footer (placed at the bottom of the window)
footer_frame = tk.Frame(window, bg='#333')
footer_frame.pack(side=tk.BOTTOM, fill=tk.X)

footer_label = tk.Canvas(footer_frame, bg='#333', height=30)
footer_label.pack(fill=tk.X)

text_id = footer_label.create_text(0, 15, text="Created by Harsh Mandaliya", font=("Helvetica", 12), fill='white', anchor='w')
window.after(100, animate_footer_text)

# Start the GUI
window.mainloop()
