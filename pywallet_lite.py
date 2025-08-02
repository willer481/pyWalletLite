import sys
import json

wallet = {
    "balance": 0.0,
    "goal": 100.0,
    "transactions": []
}

def add_transaction():
    try:
        amount = float(input("Amount (£): "))
        reason = input("Reason: ")
        wallet["balance"] += amount
        wallet["transactions"].append((amount, reason))
        print(f"✅ Added £{amount:.2f} for '{reason}'")
    except ValueError:
        print("❌ Please enter a valid number.")

def view_balance():
    print(f"\n💰 Balance: £{wallet['balance']:.2f}\n")

def set_goal():
    try:
        new_goal = float(input("New savings goal (£): "))
        wallet["goal"] = new_goal
        print(f"🎯 Goal updated: £{new_goal:.2f}")
    except ValueError:
        print("❌ Please enter a valid number.")

def progress_report():
    percent = (wallet["balance"] / wallet["goal"]) * 100 if wallet["goal"] else 0
    print(f"\n📊 Progress: {percent:.1f}% of £{wallet['goal']:.2f}\n")

def save_wallet(filename="wallet.json"):
    with open(filename, "w") as f:
        json.dump(wallet, f)
    print("💾 Wallet saved!")

def load_wallet(filename="wallet.json"):
    global wallet
    try:
        with open(filename, "r") as f:
            wallet = json.load(f)
        print("📂 Wallet loaded!")
    except FileNotFoundError:
        print("⚠️ No saved wallet found. Starting fresh.")

def view_transactions():
    print("\n📜 Transaction History:")
    if not wallet["transactions"]:
        print("No transactions yet.")
    else:
        for i, (amount, reason) in enumerate(wallet["transactions"], start=1):
            print(f"{i}. £{amount:.2f} – {reason}")
    print()


load_wallet()

def main_menu():
    while True:
        print("""
╔═══════════════════════════╗
║      🐍 PyWallet Lite      ║
╠═══════════════════════════╣
║ 1. Add Transaction        ║
║ 2. View Balance           ║
║ 3. Set Savings Goal       ║
║ 4. Show Progress Report   ║
║ 5. Exit                   ║
║ 6. View Transactions      ║
╚═══════════════════════════╝
        """)
        choice = input("Choose an option (1-5): ")
        if choice == '1':
            add_transaction()
            save_wallet()
        elif choice == '2':
            view_balance()
        elif choice == '3':
            set_goal()
            save_wallet()
        elif choice == '4':
            progress_report()
        elif choice == '5':
            print("👋 Exiting PyWallet. Keep saving smart!")
            sys.exit()
        elif choice == '6':
            view_transactions()
        else:
            print("❌ Invalid choice. Try again.\n")

main_menu()
