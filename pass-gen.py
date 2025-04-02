import random
import string
import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip  
import zxcvbn  
from supabase import create_client
import json
import hashlib
import threading
import logging  # Added logging import

# Configuration
CONFIG_FILE = "config.json"

# Supabase configuration - you need to replace these with your actual credentials
SUPABASE_URL = "https://your-project-url.supabase.co"  # Update this with your project URL
SUPABASE_KEY = "your-anon-key"  # Update this with your anon/public key

# Add table name as a constant
SUPABASE_TABLE_NAME = "passwords"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        
        # Set theme colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#4a6ea9"
        self.root.configure(bg=self.bg_color)
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize variables
        self.generated_password = ""
        self.setup_ui()
        
    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                config = {
                    "supabase_url": SUPABASE_URL,
                    "supabase_key": SUPABASE_KEY,
                    "default_length": 16,
                    "use_excel": True,
                    "use_supabase": False
                }
                self.save_config(config)
                return config
        except json.JSONDecodeError as e:  # Improved error handling
            logging.error(f"Error loading config: {e}")
            return {
                "supabase_url": SUPABASE_URL,
                "supabase_key": SUPABASE_KEY,
                "default_length": 16,
                "use_excel": True,
                "use_supabase": False
            }
    
    def save_config(self, config):
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            logging.info("Configuration saved successfully.")
        except Exception as e:
            logging.error(f"Error saving config: {e}")
    
    def setup_ui(self):
        # Create a main frame
        main_frame = tk.Frame(self.root, bg=self.bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Secure Password Generator", 
                               font=("Helvetica", 16, "bold"), bg=self.bg_color)
        title_label.pack(pady=(0, 15))
        
        # Service name frame
        service_frame = tk.Frame(main_frame, bg=self.bg_color)
        service_frame.pack(fill=tk.X, pady=5)
        
        service_name_label = tk.Label(service_frame, text="Service Name:", 
                                     bg=self.bg_color, anchor="w")
        service_name_label.pack(side=tk.LEFT)
        
        self.service_name_entry = tk.Entry(service_frame, width=30)
        self.service_name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Length frame
        length_frame = tk.Frame(main_frame, bg=self.bg_color)
        length_frame.pack(fill=tk.X, pady=5)
        
        length_label = tk.Label(length_frame, text="Password Length:", 
                               bg=self.bg_color, anchor="w")
        length_label.pack(side=tk.LEFT)
        
        self.length_value = tk.StringVar()
        self.length_value.set(str(self.config["default_length"]))
        
        self.length_slider = ttk.Scale(length_frame, from_=8, to=32, 
                                      orient=tk.HORIZONTAL, 
                                      command=self.update_length_label)
        self.length_slider.set(self.config["default_length"])
        self.length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        length_value_label = tk.Label(length_frame, textvariable=self.length_value, 
                                     width=3, bg=self.bg_color)
        length_value_label.pack(side=tk.RIGHT)
        
        # Character sets frame
        char_frame = tk.LabelFrame(main_frame, text="Password Complexity", 
                                  bg=self.bg_color, padx=10, pady=10)
        char_frame.pack(fill=tk.X, pady=10)
        
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        
        lower_check = tk.Checkbutton(char_frame, text="Lowercase (a-z)", 
                                    variable=self.lower_var, bg=self.bg_color)
        lower_check.grid(row=0, column=0, sticky="w")
        
        upper_check = tk.Checkbutton(char_frame, text="Uppercase (A-Z)", 
                                    variable=self.upper_var, bg=self.bg_color)
        upper_check.grid(row=0, column=1, sticky="w")
        
        digits_check = tk.Checkbutton(char_frame, text="Numbers (0-9)", 
                                     variable=self.digits_var, bg=self.bg_color)
        digits_check.grid(row=1, column=0, sticky="w")
        
        special_check = tk.Checkbutton(char_frame, text="Special (!@#$)", 
                                      variable=self.special_var, bg=self.bg_color)
        special_check.grid(row=1, column=1, sticky="w")
        
        # Storage options frame
        storage_frame = tk.LabelFrame(main_frame, text="Storage Options", 
                                     bg=self.bg_color, padx=10, pady=10)
        storage_frame.pack(fill=tk.X, pady=10)
        
        self.excel_var = tk.BooleanVar(value=self.config["use_excel"])
        self.supabase_var = tk.BooleanVar(value=self.config["use_supabase"])
        
        excel_check = tk.Checkbutton(storage_frame, text="Excel File", 
                                    variable=self.excel_var, bg=self.bg_color)
        excel_check.grid(row=0, column=0, sticky="w")
        
        supabase_check = tk.Checkbutton(storage_frame, text="Supabase (Cloud)", 
                                       variable=self.supabase_var, bg=self.bg_color)
        supabase_check.grid(row=0, column=1, sticky="w")
        
        # Configure Supabase button
        config_button = tk.Button(storage_frame, text="Configure Supabase", 
                                 command=self.configure_supabase)
        config_button.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Generate button
        generate_button = tk.Button(main_frame, text="Generate Password", 
                                   bg=self.accent_color, fg="white",
                                   command=self.generate_password, height=2)
        generate_button.pack(fill=tk.X, pady=10)
        
        # Password display
        password_frame = tk.Frame(main_frame, bg=self.bg_color, relief=tk.GROOVE, bd=1)
        password_frame.pack(fill=tk.X, pady=10)
        
        self.password_var = tk.StringVar()
        self.password_var.set("")
        
        self.password_label = tk.Entry(password_frame, textvariable=self.password_var, 
                                      font=("Courier", 12), bd=0, justify=tk.CENTER,
                                      state="readonly")
        self.password_label.pack(fill=tk.X, pady=10, padx=10)
        
        # Password strength
        self.strength_var = tk.StringVar()
        self.strength_var.set("")
        
        self.strength_label = tk.Label(main_frame, textvariable=self.strength_var,
                                      bg=self.bg_color, font=("Helvetica", 10, "bold"))
        self.strength_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        copy_button = tk.Button(buttons_frame, text="Copy to Clipboard", 
                               command=self.copy_password, width=15)
        copy_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = tk.Button(buttons_frame, text="Clear All", 
                                command=self.clear_all, width=15)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update_length_label(self, event=None):
        self.length_value.set(str(int(float(self.length_slider.get()))))
    
    def configure_supabase(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("Supabase Configuration")
        config_window.geometry("500x250")
        config_window.transient(self.root)
        config_window.grab_set()
        config_window.configure(bg=self.bg_color)
        
        # Add instructions
        instructions = tk.Label(config_window, text="Enter your Supabase project URL and anon/public key\n"
                              "You can find these in your Supabase project settings.",
                              bg=self.bg_color, wraplength=450)
        instructions.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        tk.Label(config_window, text="Supabase URL:", bg=self.bg_color).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        url_entry = tk.Entry(config_window, width=45)
        url_entry.grid(row=1, column=1, padx=10, pady=10)
        url_entry.insert(0, self.config.get("supabase_url", ""))
        
        tk.Label(config_window, text="Supabase Key:", bg=self.bg_color).grid(row=2, column=0, sticky="w", padx=10, pady=10)
        key_entry = tk.Entry(config_window, width=45)
        key_entry.grid(row=2, column=1, padx=10, pady=10)
        key_entry.insert(0, self.config.get("supabase_key", ""))
        
        def save_and_test():
            self.config["supabase_url"] = url_entry.get().strip()
            self.config["supabase_key"] = key_entry.get().strip()
            
            # Test the connection
            try:
                supabase = create_client(self.config["supabase_url"], self.config["supabase_key"])
                response = supabase.table(SUPABASE_TABLE_NAME).select("*").limit(1).execute()
                
                # If we get here, the connection was successful
                self.save_config(self.config)
                messagebox.showinfo("Success", "Supabase connection successful!")
                self.status_var.set("Supabase configuration saved and tested successfully")
                config_window.destroy()
                
            except Exception as e:
                messagebox.showerror("Connection Error", 
                                   f"Failed to connect to Supabase. Please check your credentials.\n\nError: {str(e)}")
        
        save_button = tk.Button(config_window, text="Save and Test Connection", 
                              command=save_and_test, bg=self.accent_color, fg="white")
        save_button.grid(row=3, column=0, columnspan=2, pady=20)
    
    def get_existing_passwords(self):
        # Get passwords from Excel
        passwords = []
        if self.excel_var.get():
            try:
                current_directory = os.path.dirname(os.path.realpath(__file__))
                file_path = os.path.join(current_directory, 'passwords.xlsx')
                
                if os.path.exists(file_path):
                    df = pd.read_excel(file_path)
                    if 'Password' in df.columns:
                        passwords.extend(df['Password'].tolist())
            except Exception as e:
                logging.error(f"Error reading existing passwords: {e}")
        
        # Get passwords from Supabase
        if self.supabase_var.get() and self.config.get("supabase_url") and self.config.get("supabase_key"):
            try:
                supabase = create_client(self.config["supabase_url"], self.config["supabase_key"])
                response = supabase.table("passwords").select("password").execute()
                if response.data:
                    passwords.extend([item.get("password") for item in response.data])
            except Exception as e:
                logging.error(f"Error fetching passwords from Supabase: {e}")
        
        return passwords
    
    def generate_password(self):
        service_name = self.service_name_entry.get()
        if not service_name:
            messagebox.showwarning("Input Error", "Please enter where you're using this password.")
            return
        
        length = int(float(self.length_slider.get()))
        include_lower = self.lower_var.get()
        include_upper = self.upper_var.get()
        include_digits = self.digits_var.get()
        include_special = self.special_var.get()
        
        if not (include_lower or include_upper or include_digits or include_special):
            messagebox.showwarning("Input Error", "Please select at least one password complexity option.")
            return
        
        # Start a loading indicator
        self.status_var.set("Generating password...")
        logging.info("Generating password for service: %s", service_name)
        
        # Perform the password generation in a separate thread
        threading.Thread(target=self._generate_password_thread, 
                        args=(service_name, length, include_lower, 
                             include_upper, include_digits, include_special)).start()
    
    def _generate_password_thread(self, service_name, length, include_lower, 
                                include_upper, include_digits, include_special):
        try:
            # Get list of existing passwords
            existing_passwords = self.get_existing_passwords()
            
            # Generate a unique password
            max_attempts = 100
            attempts = 0
            
            characters = []
            if include_lower:
                characters.append(string.ascii_lowercase)
            if include_upper:
                characters.append(string.ascii_uppercase)
            if include_digits:
                characters.append(string.digits)
            if include_special:
                characters.append(string.punctuation.replace(' ', ''))
            
            all_characters = ''.join(characters)
            
            password = None
            while attempts < max_attempts:
                # Ensure at least one character from each selected character set
                password_chars = []
                for char_set in characters:
                    password_chars.append(random.choice(char_set))
                
                # Fill the rest with random characters
                remaining_length = length - len(password_chars)
                password_chars.extend(random.choices(all_characters, k=remaining_length))
                
                # Shuffle the characters
                random.shuffle(password_chars)
                
                password = ''.join(password_chars)
                
                # Check if password is unique
                if password not in existing_passwords:
                    break
                
                attempts += 1
            
            if attempts == max_attempts:
                self.root.after(0, lambda: messagebox.showwarning("Generation Error", 
                          "Could not generate a unique password. Please try different parameters."))
                self.root.after(0, lambda: self.status_var.set("Failed to generate unique password"))
                logging.warning("Failed to generate a unique password after %d attempts.", max_attempts)
                return
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Save password according to selected options
            save_success = True
            
            if self.excel_var.get():
                excel_success = self.save_password_to_excel(service_name, password, timestamp)
                if not excel_success:
                    save_success = False
            
            if self.supabase_var.get():
                supabase_success = self.save_password_to_supabase(service_name, password, timestamp)
                if not supabase_success:
                    save_success = False
            
            # Update UI
            self.root.after(0, lambda: self.update_ui(password, save_success))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)}"))
            logging.error("Error during password generation: %s", str(e))
    
    def update_ui(self, password, save_success):
        self.generated_password = password
        self.password_var.set(password)
        
        # Update password strength
        strength = self.check_password_strength(password)
        self.strength_var.set(f"Strength: {strength}")
        
        # Set color based on strength
        if strength == "Weak":
            self.strength_label.config(fg="red")
        elif strength == "Medium":
            self.strength_label.config(fg="orange")
        elif strength == "Strong":
            self.strength_label.config(fg="green")
        elif strength == "Very Strong":
            self.strength_label.config(fg="dark green")
        
        if save_success:
            self.status_var.set("Password generated and saved successfully")
            logging.info("Password generated and saved successfully for service: %s", self.service_name_entry.get())
        else:
            self.status_var.set("Password generated but there were issues saving it")
            logging.warning("Password generated but there were issues saving it.")
    
    def check_password_strength(self, password):
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
    
    def save_password_to_excel(self, service_name, password, timestamp):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_directory, 'passwords.xlsx')
        
        try:
            # Check if the file exists first
            if os.path.exists(file_path):
                try:
                    df = pd.read_excel(file_path)
                except PermissionError:
                    self.root.after(0, lambda: messagebox.showerror("Error", 
                              "Cannot access passwords.xlsx. Make sure the file is not open in another program."))
                    return False
            else:
                df = pd.DataFrame(columns=['Service', 'Password', 'Timestamp'])
            
            new_entry = pd.DataFrame([[service_name, password, timestamp]], 
                                    columns=['Service', 'Password', 'Timestamp'])
            df = pd.concat([df, new_entry], ignore_index=True)
            
            try:
                df.to_excel(file_path, index=False)
                logging.info("Password saved to Excel successfully.")
                return True
            except PermissionError:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                          "Cannot save to passwords.xlsx. Make sure the file is not open in another program."))
                return False
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to save to Excel: {str(e)}"))
                logging.error("Failed to save to Excel: %s", str(e))
                return False
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Excel error: {str(e)}"))
            logging.error("Excel error: %s", str(e))
            return False
    
    def save_password_to_supabase(self, service_name, password, timestamp):
        if not self.config.get("supabase_url") or not self.config.get("supabase_key"):
            self.root.after(0, lambda: messagebox.showerror("Error", 
                      "Supabase not configured. Please configure Supabase first."))
            return False

        try:
            # Initialize Supabase client
            supabase = create_client(self.config["supabase_url"], self.config["supabase_key"])
            
            # Create a simplified data structure
            data = {
                "service": service_name,
                "password": password,
                "created_at": timestamp
            }
            
            try:
                # Insert data into Supabase
                response = supabase.table(SUPABASE_TABLE_NAME).insert(data).execute()
                
                if hasattr(response, 'data') and response.data:
                    logging.info("Password saved to Supabase successfully")
                    return True
                else:
                    error_msg = getattr(response, 'error', 'Unknown error occurred')
                    logging.error("Supabase Error: %s", error_msg)
                    self.root.after(0, lambda: messagebox.showerror("Supabase Error", 
                              f"Failed to save password: {error_msg}"))
                    return False
                    
            except Exception as e:
                error_msg = str(e)
                logging.error("Supabase insertion error: %s", error_msg)
                
                if "new row violates row-level security policy" in error_msg:
                    self.root.after(0, lambda: messagebox.showerror("Supabase Error", 
                            "Row Level Security (RLS) error. Please ensure:\n\n"
                            "1. RLS is disabled for the passwords table, or\n"
                            "2. You have proper insert policies configured\n\n"
                            "Go to Supabase Dashboard → Authentication → Policies to configure."))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Supabase Error", 
                              f"Failed to save password: {error_msg}"))
                return False
                
        except Exception as e:
            logging.error("Supabase connection error: %s", str(e))
            self.root.after(0, lambda: messagebox.showerror("Connection Error", 
                          f"Could not connect to Supabase. Please check your configuration and internet connection.\n\nError: {str(e)}"))
            return False
    
    def copy_password(self):
        if self.generated_password:
            pyperclip.copy(self.generated_password)
            self.status_var.set("Password copied to clipboard!")
            logging.info("Password copied to clipboard.")
        else:
            self.status_var.set("No password to copy")
            logging.warning("Attempted to copy but no password was generated.")
    
    def clear_all(self):
        self.service_name_entry.delete(0, tk.END)
        self.length_slider.set(self.config["default_length"])
        self.update_length_label()
        self.lower_var.set(True)
        self.upper_var.set(True)
        self.digits_var.set(True)
        self.special_var.set(True)
        self.password_var.set("")
        self.strength_var.set("")
        self.generated_password = ""
        self.status_var.set("Ready")
        logging.info("Cleared all fields.")

    def test_supabase_connection(self):
        try:
            supabase = create_client(self.config["supabase_url"], self.config["supabase_key"])
            response = supabase.table("passwords").select("*").execute()
            if response.data:
                logging.info("Successfully connected to Supabase.")
                return True
            else:
                logging.error("No data returned from Supabase.")
                return False
        except Exception as e:
            logging.error("Connection error: %s", str(e))
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
