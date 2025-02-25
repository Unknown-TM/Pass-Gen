import random
import string
import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip  
import zxcvbn  

#  generate the password
def generate_password():

    service_name = service_name_entry.get()
    length = length_slider.get()
    include_lower = lower_var.get()
    include_upper = upper_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()

    if not (include_lower or include_upper or include_digits or include_special):
        messagebox.showwarning("Input Error", "Please select at least one password complexity option.")
        return
    all_characters = ""
    if include_lower:
        all_characters += string.ascii_lowercase
    if include_upper:
        all_characters += string.ascii_uppercase
    if include_digits:
        all_characters += string.digits
    if include_special:
        all_characters += string.punctuation.replace(' ', '')
    password = ''.join(random.choice(all_characters) for _ in range(length))

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_password_to_excel(service_name, password, timestamp)

    password_label.config(text=f"Generated Password: {password}")
    password_strength = check_password_strength(password)
    password_strength_label.config(text=f"Password Strength: {password_strength}")
    copy_button.config(state=tk.NORMAL)
    global generated_password
    generated_password = password
    security_tips_label.config(text="Security Tip: Use a password manager to store your passwords securely.")
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

def save_password_to_excel(service_name, password, timestamp):

    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'passwords.xlsx')

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Service', 'Password', 'Timestamp'])

    
    new_entry = pd.DataFrame([[service_name, password, timestamp]], columns=['Service', 'Password', 'Timestamp'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_excel(file_path, index=False)

def copy_password():
    global generated_password
    pyperclip.copy(generated_password)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

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

root = tk.Tk()
root.title("Password Generator")

service_name_label = tk.Label(root, text="Where are you using this password?")
service_name_label.pack(pady=5)

service_name_entry = tk.Entry(root, width=40)
service_name_entry.pack(pady=5)

length_label = tk.Label(root, text="Password Length")
length_label.pack(pady=5)

length_slider = tk.Scale(root, from_=16, to_=32, orient=tk.HORIZONTAL)
length_slider.set(16)
length_slider.pack(pady=5)

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

generate_button = tk.Button(root, text="Generate Password", command=generate_password, width=20)
generate_button.pack(pady=10)

password_label = tk.Label(root, text="Generated Password: ")
password_label.pack(pady=10)

password_strength_label = tk.Label(root, text="Password Strength: ")
password_strength_label.pack(pady=10)

copy_button = tk.Button(root, text="Copy Password", command=copy_password, width=20, state=tk.DISABLED)
copy_button.pack(pady=10)

security_tips_label = tk.Label(root, text="")
security_tips_label.pack(pady=5)

clear_button = tk.Button(root, text="Clear All", command=clear_all, width=20)
clear_button.pack(pady=10)

root.mainloop()
