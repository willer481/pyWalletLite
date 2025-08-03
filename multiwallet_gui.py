import tkinter as tk
from tkinter import messagebox
import os
import json

class WalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("pyWalletLite")
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        self.show_login_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def get_wallet_path(self, username):
        return f"{username}_wallet.json"

    def is_valid_pin(self, pin):
        pin = pin.strip()
        return len(pin) == 4 and pin.isdigit()

    # 🔑 LOGIN SCREEN
    def show_login_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Username").pack()
        self.login_username_entry = tk.Entry(self.main_frame)
        self.login_username_entry.pack()

        tk.Label(self.main_frame, text="PIN").pack()
        self.login_pin_entry = tk.Entry(self.main_frame, show="*")
        self.login_pin_entry.pack()

        tk.Button(self.main_frame, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(self.main_frame, text="Sign Up", command=self.show_signup_screen).pack()

    def login_user(self):
        username = self.login_username_entry.get().strip()
        pin = self.login_pin_entry.get().strip()

        if not self.is_valid_pin(pin):
            messagebox.showerror("Invalid PIN", "PIN must be exactly 4 numeric digits.")
            return

        file_path = self.get_wallet_path(username)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            if data.get("pin") == pin:
                self.username = username
                self.wallet_data = data
                self.show_main_menu()
            else:
                messagebox.showerror("Error", "Incorrect PIN.")
        else:
            messagebox.showerror("Error", "User not found.")

    # ✨ SIGNUP SCREEN
    def show_signup_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Choose a Username").pack()
        self.signup_username_entry = tk.Entry(self.main_frame)
        self.signup_username_entry.pack()

        tk.Label(self.main_frame, text="Choose a 4-digit PIN").pack()
        self.signup_pin_entry = tk.Entry(self.main_frame, show="*")
        self.signup_pin_entry.pack()

        tk.Button(self.main_frame, text="Create Account", command=self.create_account).pack(pady=10)
        tk.Button(self.main_frame, text="Back to Login", command=self.show_login_screen).pack()

    def create_account(self):
        username = self.signup_username_entry.get().strip()
        pin = self.signup_pin_entry.get().strip()

        if not self.is_valid_pin(pin):
            messagebox.showerror("Invalid PIN", "PIN must be exactly 4 numeric digits.")
            return

        file_path = self.get_wallet_path(username)
        if os.path.exists(file_path):
            messagebox.showerror("Error", "Username already exists.")
        else:
            self.wallet_data = {"pin": pin, "balance": 0}
            self.username = username
            self.save_wallet()
            messagebox.showinfo("Success", "Account created!")
            self.show_main_menu()

    # 🏠 MAIN MENU
    def show_main_menu(self):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Welcome, {self.username}!").pack()
        tk.Label(self.main_frame, text=f"Balance: £{self.wallet_data['balance']:.2f}").pack()

        tk.Button(self.main_frame, text="Add Income", command=self.add_income).pack()
        tk.Button(self.main_frame, text="Add Expense", command=self.add_expense).pack()
        tk.Button(self.main_frame, text="Logout", command=self.show_login_screen).pack(pady=10)

    # 💰 INCOME / EXPENSE METHODS
    def add_income(self):
        amount = self.get_amount("Add Income")
        if amount is not None:
            self.wallet_data["balance"] += amount
            self.save_wallet()
            self.show_main_menu()

    def add_expense(self):
        amount = self.get_amount("Add Expense")
        if amount is not None:
            self.wallet_data["balance"] -= amount
            self.save_wallet()
            self.show_main_menu()

    # 📥 AMOUNT INPUT POPUP
    def get_amount(self, title):
        top = tk.Toplevel(self.root)
        top.title(title)
        tk.Label(top, text="Amount (£)").pack()
        entry = tk.Entry(top)
        entry.pack()
        result = []

        def submit():
            try:
                value = float(entry.get())
                result.append(value)
                top.destroy()
            except ValueError:
                messagebox.showerror("Invalid", "Please enter a valid number.")

        tk.Button(top, text="Submit", command=submit).pack()
        top.transient(self.root)
        top.grab_set()
        self.root.wait_window(top)
        return result[0] if result else None

    def save_wallet(self):
        file_path = self.get_wallet_path(self.username)
        with open(file_path, "w") as f:
            json.dump(self.wallet_data, f)

# 🚀 Launch the app
if __name__ == "__main__":
    root = tk.Tk()
    app = WalletApp(root)
    root.mainloop()