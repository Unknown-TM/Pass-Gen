# Password Generator 🔐

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python-based password generator that creates strong, secure, and customizable passwords. The application features options for password length, character complexity, and stores the generated passwords in an Excel file for future reference.

Created by: **Unknown-TM**

## 🚀 Features

- **Customizable Password Length:** Choose a length between 16 and 32 characters
- **Character Complexity:** Include:
  - Lowercase letters
  - Uppercase letters
  - Digits
  - Special characters
- **Password Strength Evaluation:** Real-time strength assessment (Weak, Medium, Strong, Very Strong)
- **Clipboard Integration:** One-click password copying
- **Password History:** Excel-based storage with service name and timestamp
- **Security Tips:** Helpful password management guidelines

## 📋 Requirements

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Required Libraries
- `pyperclip` - Clipboard functionality
- `zxcvbn` - Password strength evaluation
- `pandas` - Excel file handling
- `openpyxl` - Excel file support

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Unknown-TM/Pass-Gen.git
   cd Pass-Gen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Launch the application:
   ```bash
   python pass-gen.py
   ```

2. Use the GUI to:
   - Set password length (16-32 characters)
   - Select character types
   - Generate password
   - Copy password to clipboard
   - View password strength
   - Save password with service name

### Example Usage
```
Service: Email
Password Length: 16
Included: [✓] lowercase [✓] uppercase [✓] digits [✓] special
Generated: a5B#2gH9&@jL$mK3
Strength: Strong
```

## 📊 Password Storage

### Local Storage (Excel)
Passwords are stored locally in `passwords.xlsx` with:
- Service name
- Generated password
- Timestamp

### Cloud Storage (Supabase)
The application also supports secure cloud storage using Supabase:

#### Features
- **Real-time Sync:** Passwords sync across devices
- **Encrypted Storage:** Passwords are encrypted before storage
- **Access Control:** Role-based access control
- **Backup:** Automatic cloud backup of passwords

#### Security Measures
- End-to-end encryption for password storage
- Row Level Security (RLS) policies
- Automatic session management
- API key authentication

#### Setup Requirements
1. Create a Supabase account
2. Set environment variables:
   ```bash
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```

#### Switching Storage Modes
Toggle between local and cloud storage using:
```bash
python pass-gen.py --storage=supabase  # For cloud storage
python pass-gen.py --storage=local     # For local storage
```

## 🔒 Security

- Passwords are generated using Python's secure random number generator
- The application never transmits passwords over the network
- Local storage only - passwords are saved on your device
- Regular security updates and maintenance

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [zxcvbn](https://github.com/dropbox/zxcvbn) - Password strength estimation
- [pyperclip](https://github.com/asweigart/pyperclip) - Clipboard functionality
- [pandas](https://pandas.pydata.org/) - Data manipulation library
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel file handling

