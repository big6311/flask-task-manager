# simple_ui.py

CORRECT_USERNAME = "admin"
CORRECT_PASSWORD = "python123"

print("=== Login Screen ===")

username = input("Enter username: ")
password = input("Enter password: ")

if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
    print("Login successful! ")
else:
    print("Login failed. ")

        
