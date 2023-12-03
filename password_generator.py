import tkinter as tk
from tkinter import messagebox, simpledialog
import string
import secrets
from cryptography.fernet import Fernet
import json
import os

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")

        self.special_characters = "!@#$%^&*()_-+=<>?/[]{}|"

        self.password_label = tk.Label(master, text="Generated Password:")
        self.password_label.pack()

        self.special_var = tk.IntVar()
        self.special_checkbox = tk.Checkbutton(master, text="Include Special Characters", variable=self.special_var)
        self.special_checkbox.pack()

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.save_button = tk.Button(master, text="Save Password", command=self.save_password)
        self.save_button.pack()

        self.generated_password = None

    def generate_password(self):
        include_special = bool(self.special_var.get())
        password_length = 12  # Adjust length as needed

        characters = string.ascii_letters + string.digits
        if include_special:
            characters += self.special_characters

        password = ''.join(secrets.choice(characters) for _ in range(password_length))

        self.password_label.config(text=f"Generated Password: {password}")
        self.generated_password = password

    def save_password(self):
        if not self.generated_password:
            messagebox.showwarning("Warning", "Generate a password first.")
            return

        password_file = "passwords.encrypted"

        try:
            with open(password_file, "rb") as file:
                passwords_data = file.read()
                if passwords_data:
                    key = self.get_password()
                    f = Fernet(key)
                    decrypted_passwords = f.decrypt(passwords_data)
                    passwords = json.loads(decrypted_passwords)
                else:
                    passwords = {}
        except (FileNotFoundError, json.JSONDecodeError):
            passwords = {}

        service_name = tk.simpledialog.askstring("Service", "Enter service name:")
        if service_name:
            passwords[service_name] = self.generated_password

            key = self.get_password()
            f = Fernet(key)
            encrypted_passwords = f.encrypt(json.dumps(passwords).encode())

            with open(password_file, "wb") as file:
                file.write(encrypted_passwords)
                messagebox.showinfo("Success", "Password saved successfully!")

    def get_password(self):
        password = simpledialog.askstring("Password", "Enter password for file:")
        key = Fernet.generate_key()

        if password:
            password_key = Fernet(key)
            encrypted_password = password_key.encrypt(password.encode())
            return encrypted_password
        else:
            messagebox.showwarning("Warning", "Password cannot be empty.")
            return b''

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()