import tkinter as tk
from tkinter import ttk  # Ensure ttk is imported here
from tkinter import messagebox
import pandas as pd
from cryptography.fernet import Fernet
import os
import subprocess  # For executing the exam.py script

# Load or generate the encryption key
def load_key():
    key_path = "secret.key"
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    return key

# Initialize the cipher
key = load_key()
cipher = Fernet(key)

# Path to the CSV file where user data is stored
csv_file_path = 'users.csv'

# Ensure CSV file exists
if not os.path.exists(csv_file_path):
    df = pd.DataFrame(columns=['Username', 'Password'])
    df.to_csv(csv_file_path, index=False)

# Function to decrypt the password
def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

# Function to stop the program
def close_program():
    window.quit()

# Function to open registration window
def open_registration():
    window.destroy()
    subprocess.run(['python3', 'registration.py'])

# Function to handle user login
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        messagebox.showerror("Error", "User database not found!")
        return

    # Read the CSV file to get user data
    df = pd.read_csv(csv_file_path)

    # Check if the username exists
    user_row = df[df['Username'] == username]

    if user_row.empty:
        messagebox.showerror("Error", "Username or password are incorrect!")
        return

    # Get the encrypted password
    encrypted_password = user_row.iloc[0]['Password']

    # Decrypt the password
    try:
        decrypted_password = decrypt_password(encrypted_password)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while decrypting the password: {str(e)}")
        return

    # Check if the password matches
    if password == decrypted_password:
        messagebox.showinfo("Success", "Login successful!")
        window.destroy()  # Close the login window
        subprocess.run(['python3', 'exam.py', username])  # Execute exam.py script with the username
    else:
        messagebox.showerror("Error", "Username or password are incorrect!")

# Function for animations
def jingle_animation(widget):
    def animate():
        current_color = widget.cget("foreground")
        next_color = "red" if current_color == "blue" else "blue"
        widget.config(foreground=next_color)
        window.after(500, animate)  # Change color every 500ms
    animate()

# Create the GUI window
window = tk.Tk()
window.title("Student Login")

# Make the window full-screen
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

# Create labels and entry fields
title_label = tk.Label(frame, text="Student Login", font=("Helvetica", 24), bg='white', fg='blue')
title_label.grid(row=0, columnspan=2, pady=20)
jingle_animation(title_label)

tk.Label(frame, text="Username:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5, sticky='e')
username_entry = tk.Entry(frame, font=("Helvetica", 14))
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Password:", bg='white', fg='blue', font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5, sticky='e')
password_entry = tk.Entry(frame, show="*", font=("Helvetica", 14))
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Style for buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 14), padding=10, background="#2196F3", foreground="white")
style.map('TButton', background=[('active', '#1976D2')])

# Login button
login_button = ttk.Button(frame, text="Login", command=login_user, style='TButton')
login_button.grid(row=3, columnspan=2, padx=10, pady=10)

# Back button
back_button = ttk.Button(frame, text="Back", command=open_registration, style='TButton')
back_button.grid(row=4, columnspan=2, padx=10, pady=10)

# Close button
close_button = ttk.Button(frame, text="Close", command=close_program, style='TButton')
close_button.grid(row=5, columnspan=2, pady=10)

# Start the GUI
window.mainloop()
