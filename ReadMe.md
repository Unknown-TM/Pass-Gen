Password Generator 

A Python-based password generator that allows users to create strong, secure, and customizable passwords. The application features options for password length, character complexity, and stores the generated passwords in an Excel file for future reference.

created by: **Unknown-TM**

Features:

- Customizable Password Length: Choose a length between 16 and 32 characters for the generated password.
- Character Complexity: Select to include lowercase letters, uppercase letters, digits, and special characters.
- Password Strength Evaluation: Displays the strength of the generated password (Weak, Medium, Strong, Very Strong).
- Clipboard Copy: Copy the generated password directly to the clipboard for easy use.
- Password History: All generated passwords, along with the service name and timestamp, are saved in an Excel file for future reference.
- Security Tips: Displays tips for better password management after generating a password.

Requirements:

This project requires the following Python libraries:

- pyperclip — For copying passwords to the clipboard.
- zxcvbn — For evaluating password strength.
- pandas — For storing password history in an Excel file.
- openpyxl — For working with Excel files.

You can install all required dependencies by running:

pip install -r requirements.txt

Dependencies:

- pyperclip
- zxcvbn
- pandas
- openpyxl

Usage:

1. Run the script using Python:

   python pass-gen.py

2. The graphical user interface will appear.

3. Click Generate Password to generate a new password.

4. The generated password will appear on the screen along with its strength.

5. Use the Copy Password button to copy the generated password to your clipboard.

6. The password, service name, and timestamp are saved in an Excel file (passwords.xlsx) for future reference.

7. To clear the fields and start again, click Clear All.

Example:

Where are you using this password? -> "Email"
Password Length: 16
Include lowercase, uppercase, digits, and special characters.
Generate Password -> "a5B#2gH9&@jL"
Password Strength: Strong

Excel Storage:

The generated passwords are stored in an Excel file named passwords.xlsx. This file is saved in the same directory as the script. The following data is stored for each password:

- Service: The service or platform (e.g., "Email").
- Password: The generated password.
- Timestamp: The date and time when the password was generated.

Contributing:

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to your branch (git push origin feature-branch).
5. Open a pull request.

Acknowledgements:

- zxcvbn: A library for password strength estimation. https://github.com/dropbox/zxcvbn
- pyperclip: A library for clipboard functionality. https://github.com/asweigart/pyperclip
- pandas: A powerful data manipulation and analysis library. https://pandas.pydata.org/
- openpyxl: A library for reading and writing Excel files. https://openpyxl.readthedocs.io/

