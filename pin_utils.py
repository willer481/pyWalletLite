def load_pin(filename="pin.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)["pin"]
    except FileNotFoundError:
        return None

def set_pin(filename="pin.json"):
    pin = input("🔐 Set a 4-digit PIN: ")
    with open(filename, "w") as f:
        json.dump({"pin": pin}, f)
    print("✅ PIN saved!")
