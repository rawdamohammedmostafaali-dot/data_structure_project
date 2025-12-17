import json
from datetime import datetime, timedelta

# ---------------- File Handling ----------------
def load_data(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

donors = load_data("donors.json")
recipients = load_data("recipients.json")
blood_stock = load_data("blood_stock.json")


# ---------------- Validation ----------------
def is_safe_donor(donor):
    age = donor["age"]
    last_donation = datetime.strptime(donor["last_donation"], "%Y-%m-%d")
    safe_date = datetime.now() - timedelta(days=90)

    if age < 17 or age > 60:
        return False
    if last_donation > safe_date:
        return False
    if donor["disease"] != "no":
        return False
    if donor["other_problem"] != "no":
        return False
    return True


# ---------------- Donor ----------------
def donor_register():
    donor_id = input("ID: ")
    donors[donor_id] = {
        "name": input("Name: "),
        "mail": input("Email: "),
        "password": input("Password: "),
        "age": int(input("Age: ")),
        "gender": input("Gender: "),
        "blood": input("Blood Type: "),
        "disease": input("Any disease? (yes/no): "),
        "other_problem": input("Other disease or medicine? (yes/no): "),
        "last_donation": input("Last donation date (YYYY-MM-DD): ")
    }
    save_data("donors.json", donors)
    print("✅ Donor Registered Successfully")

def donor_login():
    donor_id = input("ID: ")
    password = input("Password: ")
    if donor_id in donors and donors[donor_id]["password"] == password:
        return donor_id
    print("❌ Invalid Login")
    return None

def donation_request(donor_id):
    donor = donors[donor_id]
    if is_safe_donor(donor):
        blood = donor["blood"]
        blood_stock[blood] = blood_stock.get(blood, 0) + 1
        donor["last_donation"] = datetime.now().strftime("%Y-%m-%d")
        save_data("blood_stock.json", blood_stock)
        save_data("donors.json", donors)
        print("🩸 Donation Accepted")
    else:
        print("❌ Donation Rejected (Not Safe Donor)")


# ---------------- Recipient ----------------
def recipient_register():
    rid = input("ID: ")
    recipients[rid] = {
        "name": input("Name: "),
        "mail": input("Email: "),
        "password": input("Password: "),
        "age": int(input("Age: ")),
        "gender": input("Gender: "),
        "blood": input("Blood Type Needed: "),
        "hospital": input("Hospital: "),
        "doctor": input("Doctor Name: ")
    }
    save_data("recipients.json", recipients)
    print("✅ Recipient Registered")

def recipient_login():
    rid = input("ID: ")
    password = input("Password: ")
    if rid in recipients and recipients[rid]["password"] == password:
        return rid
    print("❌ Invalid Login")
    return None

def search_blood():
    blood = input("Blood Type: ")
    print("Available Quantity:", blood_stock.get(blood, 0))


# ---------------- Admin ----------------
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Display Donors")
        print("2. Display Recipients")
        print("3. Display Blood Stock")
        print("4. Update Blood Stock")
        print("5. Exit")

        ch = input("Choice: ")
        if ch == "1":
            print(json.dumps(donors, indent=4))
        elif ch == "2":
            print(json.dumps(recipients, indent=4))
        elif ch == "3":
            print(json.dumps(blood_stock, indent=4))
        elif ch == "4":
            blood = input("Blood Type: ")
            qty = int(input("Quantity: "))
            blood_stock[blood] = qty
            save_data("blood_stock.json", blood_stock)
        elif ch == "5":
            break


# ---------------- Main ----------------
def main():
    while True:
        print("\n🩸 Blood Bank Management System")
        print("1. Donor")
        print("2. Recipient")
        print("3. Admin")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            print("1. Register\n2. Login")
            c = input("Choose: ")
            if c == "1":
                donor_register()
            elif c == "2":
                did = donor_login()
                if did:
                    donation_request(did)

        elif choice == "2":
            print("1. Register\n2. Login")
            c = input("Choose: ")
            if c == "1":
                recipient_register()
            elif c == "2":
                rid = recipient_login()
                if rid:
                    search_blood()

        elif choice == "3":
            admin_menu()

        elif choice == "4":
            print("Goodbye 👋")
            break

main()

