import random
import string
import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip  # To copy to clipboard
import zxcvbn  # For password strength checking

# Function to generate the password
def generate_password():
    # Get the service name from the entry widget
    service_name = service_name_entry.get()
    
    # Get the length from the slider
    length = length_slider.get()

    # Get the options for complexity
    include_lower = lower_var.get()
    include_upper = upper_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()

    # Ensure at least one complexity option is selected
    if not (include_lower or include_upper or include_digits or include_special):
        messagebox.showwarning("Input Error", "Please select at least one password complexity option.")
        return

    # Define the character set based on the selected complexity options
    all_characters = ""
    if include_lower:
        all_characters += string.ascii_lowercase
    if include_upper:
        all_characters += string.ascii_uppercase
    if include_digits:
        all_characters += string.digits
    if include_special:
        all_characters += string.punctuation.replace(' ', '')

    # Generate the password using random choices
    password = ''.join(random.choice(all_characters) for _ in range(length))

    # Record the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Save the password, service name, and timestamp to Excel
    save_password_to_excel(service_name, password, timestamp)

    # Display the generated password and strength
    password_label.config(text=f"Generated Password: {password}")
    password_strength = check_password_strength(password)
    password_strength_label.config(text=f"Password Strength: {password_strength}")

    # Enable the "Copy Password" button after the password is generated
    copy_button.config(state=tk.NORMAL)

    # Store the password in a global variable to be copied later
    global generated_password
    generated_password = password

    # Display security tips
    security_tips_label.config(text="Security Tip: Use a password manager to store your passwords securely.")

# Function to check password strength
def check_password_strength(password):
    strength = zxcvbn.zxcvbn(password)
    score = strength['score']
    if score == 0:
        return "Weak"
    elif score == 1:
        return "Medium"
    elif score == 2:
        return "Strong"
    elif score == 3:
        return "Very Strong"
    return "Unknown"

# Function to save password, service name, and timestamp to Excel
def save_password_to_excel(service_name, password, timestamp):
    # Get the current directory where the script is located
    current_directory = os.path.dirname(os.path.realpath(__file__))
    
    # Define the file path (save in the same directory as the script)
    file_path = os.path.join(current_directory, 'passwords.xlsx')

    # Check if the file exists
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame with headers
        df = pd.DataFrame(columns=['Service', 'Password', 'Timestamp'])

    # Add the new entry (service name, password, and timestamp) to the DataFrame
    new_entry = pd.DataFrame([[service_name, password, timestamp]], columns=['Service', 'Password', 'Timestamp'])
    df = pd.concat([df, new_entry], ignore_index=True)

    # Save the updated DataFrame to Excel
    df.to_excel(file_path, index=False)

# Function to copy the password to the clipboard
def copy_password():
    global generated_password
    pyperclip.copy(generated_password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Function to clear all fields
def clear_all():
    service_name_entry.delete(0, tk.END)
    length_slider.set(16)
    lower_var.set(True)
    upper_var.set(True)
    digits_var.set(True)
    special_var.set(True)
    password_label.config(text="Generated Password: ")
    password_strength_label.config(text="Password Strength: ")
    copy_button.config(state=tk.DISABLED)
    security_tips_label.config(text="")

# Set up the Tkinter UI
root = tk.Tk()
root.title("Password Generator")

# Label and entry for the service name
service_name_label = tk.Label(root, text="Where are you using this password?")
service_name_label.pack(pady=5)

service_name_entry = tk.Entry(root, width=40)
service_name_entry.pack(pady=5)

# Label for password length slider
length_label = tk.Label(root, text="Password Length")
length_label.pack(pady=5)

# Slider for password length (16-32 characters)
length_slider = tk.Scale(root, from_=16, to_=32, orient=tk.HORIZONTAL)
length_slider.set(16)
length_slider.pack(pady=5)

# Checkboxes for password complexity options
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

lower_check = tk.Checkbutton(root, text="Include lowercase letters", variable=lower_var)
lower_check.pack()

upper_check = tk.Checkbutton(root, text="Include uppercase letters", variable=upper_var)
upper_check.pack()

digits_check = tk.Checkbutton(root, text="Include digits", variable=digits_var)
digits_check.pack()

special_check = tk.Checkbutton(root, text="Include special characters", variable=special_var)
special_check.pack()

# Button to generate the password
generate_button = tk.Button(root, text="Generate Password", command=generate_password, width=20)
generate_button.pack(pady=10)

# Label to display the generated password
password_label = tk.Label(root, text="Generated Password: ")
password_label.pack(pady=10)

# Label to display password strength
password_strength_label = tk.Label(root, text="Password Strength: ")
password_strength_label.pack(pady=10)

# Button to copy the password to clipboard (disabled initially)
copy_button = tk.Button(root, text="Copy Password", command=copy_password, width=20, state=tk.DISABLED)
copy_button.pack(pady=10)

# Label to display security tips
security_tips_label = tk.Label(root, text="")
security_tips_label.pack(pady=5)

# Button to clear all fields
clear_button = tk.Button(root, text="Clear All", command=clear_all, width=20)
clear_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
