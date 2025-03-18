import random
import string
import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
import pyperclip  
import zxcvbn  
from supabase import create_client  # Added for Supabase integration

# Supabase configuration - you need to replace these with your actual credentials
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_API_KEY"

# Initialize Supabase client
def init_supabase():
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase: {e}")
        return None

# Function to get existing passwords from the Excel file
def get_existing_passwords():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, 'passwords.xlsx')
    
    try:
        df = pd.read_excel(file_path)
        return df['Password'].tolist()
    except FileNotFoundError:
        return []

# Function to save password to Supabase
def save_password_to_supabase(service_name, password, timestamp):
    supabase = init_supabase()
    if not supabase:
        messagebox.showerror("Error", "Could not connect to Supabase. Password saved to Excel only.")
        return False
    
    try:
        data = {
            "service": service_name,
            "password": password,
            "created_at": timestamp
        }
        supabase.table("passwords").insert(data).execute()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save to Supabase: {str(e)}")
        return False

#  generate the password
def generate_password():
    service_name = service_name_entry.get()
    if not service_name:
        messagebox.showwarning("Input Error", "Please enter where you're using this password.")
        return
        
    length = length_slider.get()
    include_lower = lower_var.get()
    include_upper = upper_var.get()
    include_digits = digits_var.get()
    include_special = special_var.get()

    if not (include_lower or include_upper or include_digits or include_special):
        messagebox.showwarning("Input Error", "Please select at least one password complexity option.")
        return
    
    # Get list of existing passwords
    existing_passwords = get_existing_passwords()
    
    # Generate a unique password
    max_attempts = 100  # Prevent infinite loop in extreme cases
    attempts = 0
    
    while attempts < max_attempts:
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
        
        # Check if password is unique
        if password not in existing_passwords:
            break
            
        attempts += 1
    
    if attempts == max_attempts:
        messagebox.showwarning("Generation Error", "Could not generate a unique password. Please try different parameters.")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Ask where to save the password
    save_location_window = tk.Toplevel(root)
    save_location_window.title("Save Location")
    save_location_window.geometry("300x150")
    save_location_window.transient(root)
    save_location_window.grab_set()
    
    tk.Label(save_location_window, text="Where do you want to save this password?").pack(pady=10)
    
    save_excel_var = tk.BooleanVar(value=True)
    save_supabase_var = tk.BooleanVar(value=False)
    
    tk.Checkbutton(save_location_window, text="Save to Excel", variable=save_excel_var).pack(anchor="w", padx=20)
    tk.Checkbutton(save_location_window, text="Save to Supabase", variable=save_supabase_var).pack(anchor="w", padx=20)
    
    def on_save_confirm():
        save_excel = save_excel_var.get()
        save_supabase = save_supabase_var.get()
        
        if not (save_excel or save_supabase):
            messagebox.showwarning("Input Error", "Please select at least one save location.")
            return
        
        if save_excel:
            save_password_to_excel(service_name, password, timestamp)
        
        if save_supabase:
            save_password_to_supabase(service_name, password, timestamp)
        
        save_location_window.destroy()
        
        # Update UI after saving
        password_label.config(text=f"Generated Password: {password}")
        password_strength = check_password_strength(password)
        password_strength_label.config(text=f"Password Strength: {password_strength}")
        copy_button.config(state=tk.NORMAL)
        global generated_password
        generated_password = password
        security_tips_label.config(text="Security Tip: Use a password manager to store your passwords securely.")
    
    tk.Button(save_location_window, text="Save", command=on_save_confirm, width=10).pack(pady=10)

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
