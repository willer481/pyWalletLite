import tkinter as tk
from tkinter import messagebox, simpledialog
import json
from pin_utils import set_pin, load_pin

wallet = {
    "balance": 0.0,
    "goal": 100.0,
    "transactions": []
}

def load_wallet(filename="wallet.json"):
    global wallet
    try:
        with open(filename, "r") as f:
            wallet = json.load(f)
    except FileNotFoundError:
        pass

def save_wallet(filename="wallet.json"):
    with open(filename, "w") as f:
        json.dump(wallet, f)

def unlock_wallet():
    stored_pin = load_pin()
    if stored_pin is None:
        set_pin()
        save_wallet()
        launch_wallet()
    else:
        pin_window = tk.Tk()
        pin_window.title("🔐 Unlock PyWallet")

        tk.Label(pin_window, text="Enter your PIN:").pack(pady=5)
        pin_entry = tk.Entry(pin_window, show="*", width=20)
        pin_entry.pack(pady=5)

        def verify_pin():
            if pin_entry.get() == stored_pin:
                pin_window.destroy()
                launch_wallet()
            else:
                messagebox.showerror("Wrong PIN", "❌ Incorrect PIN!")

        tk.Button(pin_window, text="Login", command=verify_pin).pack(pady=5)
        pin_window.mainloop()

def launch_wallet():
    root = tk.Tk()
    root.title("🐍 PyWallet Lite")

    def update_display():
        balance_var.set(f"£{wallet['balance']:.2f}")
        goal_var.set(f"£{wallet['goal']:.2f}")
        progress = (wallet["balance"] / wallet["goal"]) * 100 if wallet["goal"] else 0
        progress_var.set(f"{progress:.1f}%")
        tx_list.delete(0, tk.END)
        for amt, reason in wallet["transactions"]:
            tx_list.insert(tk.END, f"£{amt:.2f} – {reason}")

    def add_tx():
        try:
            amount = float(simpledialog.askstring("Add Transaction", "Amount (£):"))
            reason = simpledialog.askstring("Add Transaction", "Reason:")
            wallet["balance"] += amount
            wallet["transactions"].append((amount, reason))
            save_wallet()
            update_display()
        except:
            messagebox.showerror("Error", "❌ Enter a valid amount.")

    def set_new_goal():
        try:
            new_goal = float(simpledialog.askstring("Set Goal", "New savings goal (£):"))
            wallet["goal"] = new_goal
            save_wallet()
            update_display()
        except:
            messagebox.showerror("Error", "❌ Enter a valid number.")

    # 💡 UI Elements
    balance_var = tk.StringVar()
    goal_var = tk.StringVar()
    progress_var = tk.StringVar()

    tk.Label(root, text="💰 Balance:").pack()
    tk.Label(root, textvariable=balance_var, font=("Arial", 14)).pack()

    tk.Label(root, text="🎯 Goal:").pack()
    tk.Label(root, textvariable=goal_var, font=("Arial", 14)).pack()

    tk.Label(root, text="📊 Progress:").pack()
    tk.Label(root, textvariable=progress_var, font=("Arial", 14)).pack(pady=10)

    tk.Button(root, text="➕ Add Transaction", width=25, command=add_tx).pack(pady=3)
    tk.Button(root, text="🎯 Set New Goal", width=25, command=set_new_goal).pack(pady=3)
    tk.Button(root, text="📂 Save Wallet", width=25, command=save_wallet).pack(pady=3)
    tk.Button(root, text="🚪 Exit", width=25, command=root.destroy).pack(pady=3)

    tk.Label(root, text="\n📜 Transaction History").pack()
    tx_list = tk.Listbox(root, width=50)
    tx_list.pack()

    update_display()
    root.mainloop()

# 🚀 Start App
load_wallet()
unlock_wallet()
