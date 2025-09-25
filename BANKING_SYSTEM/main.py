import json
import os
import hashlib
import getpass
from colorama import Fore, Style, init
from datetime import datetime, timedelta
import csv

# Initialize colorama
init(autoreset=True)

class PyBankSystem:
    def __init__(self):
        self.data_file = "bank_data.json"
        self.users = {}
        self.current_user = None
        self.load_data()

    def load_data(self):
        """Load user data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.users = json.load(f)
                print(Fore.GREEN + "✅ Data loaded successfully!")
            except Exception as e:
                print(Fore.RED + f"❌ Error loading data: {e}")
                self.users = {}
        else:
            print(Fore.YELLOW + "📝 No existing data found. Starting fresh!")

    def save_data(self):
        """Save user data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.users, f, indent=2, default=str)
            print(Fore.GREEN + "✅ Data saved successfully!")
        except Exception as e:
            print(Fore.RED + f"❌ Error saving data: {e}")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_account(self):
        """Create a new user account"""
        print(Fore.CYAN + "\n🆕 CREATE NEW ACCOUNT")
        print("=" * 30)
        
        while True:
            username = input(Fore.YELLOW + "Enter username: ").strip()
            if not username:
                print(Fore.RED + "❌ Username cannot be empty!")
                continue
            if username in self.users:
                print(Fore.RED + "❌ Username already exists!")
                continue
            break

        full_name = input(Fore.YELLOW + "Enter full name: ").strip()
        while not full_name:
            print(Fore.RED + "❌ Name cannot be empty!")
            full_name = input(Fore.YELLOW + "Enter full name: ").strip()

        while True:
            password = getpass.getpass(Fore.YELLOW + "Enter password: ")
            if len(password) < 6:
                print(Fore.RED + "❌ Password must be at least 6 characters!")
                continue
            confirm_password = getpass.getpass(Fore.YELLOW + "Confirm password: ")
            if password != confirm_password:
                print(Fore.RED + "❌ Passwords don't match!")
                continue
            break

        account_number = f"ACC{len(self.users) + 1:06d}"
        
        self.users[username] = {
            'full_name': full_name,
            'password_hash': self.hash_password(password),
            'account_number': account_number,
            'balance': 0.0,
            'transactions': [],
            'created_date': datetime.now().isoformat()
        }

        self.save_data()
        print(Fore.GREEN + f"✅ Account created successfully!")
        print(Fore.CYAN + f"👤 Name: {full_name}")
        print(Fore.CYAN + f"🆔 Account Number: {account_number}")
        print(Fore.CYAN + f"👤 Username: {username}")

    def login(self):
        """User login"""
        print(Fore.CYAN + "\n🔐 LOGIN")
        print("=" * 20)
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            username = input(Fore.YELLOW + "Username: ").strip()
            password = getpass.getpass(Fore.YELLOW + "Password: ")
            
            if username in self.users:
                if self.users[username]['password_hash'] == self.hash_password(password):
                    self.current_user = username
                    print(Fore.GREEN + f"✅ Welcome back, {self.users[username]['full_name']}!")
                    return True
                else:
                    attempts += 1
                    remaining = max_attempts - attempts
                    if remaining > 0:
                        print(Fore.RED + f"❌ Invalid password! {remaining} attempts remaining.")
                    else:
                        print(Fore.RED + "❌ Account locked due to multiple failed attempts!")
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(Fore.RED + f"❌ User not found! {remaining} attempts remaining.")
                else:
                    print(Fore.RED + "❌ Login blocked due to multiple failed attempts!")
        
        return False

    def get_user_data(self):
        """Get current user's data"""
        return self.users[self.current_user]

    def add_transaction(self, transaction_type, amount, description, balance_after):
        """Add transaction to user's history"""
        transaction = {
            'timestamp': datetime.now().isoformat(),
            'type': transaction_type,
            'amount': amount,
            'description': description,
            'balance_after': balance_after
        }
        self.users[self.current_user]['transactions'].append(transaction)

    def balance(self):
        """Display current balance"""
        user_data = self.get_user_data()
        print(Fore.CYAN + f"\n💰 ACCOUNT BALANCE")
        print("=" * 25)
        print(Fore.CYAN + f"👤 Account Holder: {user_data['full_name']}")
        print(Fore.CYAN + f"🆔 Account Number: {user_data['account_number']}")
        print(Fore.CYAN + f"💵 Current Balance: ₹{user_data['balance']:.2f}")
        print()
        
        # Add balance check to transaction history
        self.add_transaction("BALANCE_INQUIRY", 0, "Balance inquiry", user_data['balance'])

    def withdraw(self):
        """Withdraw money"""
        user_data = self.get_user_data()
        try:
            amount = float(input(Fore.YELLOW + "Enter amount to withdraw: ₹"))
            if amount > user_data['balance']:
                print(Fore.RED + "❌ Insufficient funds!")
                print(Fore.CYAN + f"Available balance: ₹{user_data['balance']:.2f}")
            elif amount <= 0:
                print(Fore.RED + "❌ Invalid withdrawal amount!")
            else:
                description = input(Fore.YELLOW + "Enter description (optional): ").strip()
                if not description:
                    description = "Cash withdrawal"
                
                self.users[self.current_user]['balance'] -= amount
                new_balance = self.users[self.current_user]['balance']
                
                print(Fore.GREEN + f"✅ Withdrawal successful!")
                print(Fore.CYAN + f"💵 Amount withdrawn: ₹{amount:.2f}")
                print(Fore.CYAN + f"💰 New balance: ₹{new_balance:.2f}")
                
                self.add_transaction("WITHDRAWAL", -amount, description, new_balance)
                self.save_data()
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter a number.")

    def deposit(self):
        """Deposit money"""
        user_data = self.get_user_data()
        try:
            amount = float(input(Fore.YELLOW + "Enter amount to deposit: ₹"))
            if amount > 0:
                description = input(Fore.YELLOW + "Enter description (optional): ").strip()
                if not description:
                    description = "Cash deposit"
                
                self.users[self.current_user]['balance'] += amount
                new_balance = self.users[self.current_user]['balance']
                
                print(Fore.GREEN + f"✅ Deposit successful!")
                print(Fore.CYAN + f"💵 Amount deposited: ₹{amount:.2f}")
                print(Fore.CYAN + f"💰 New balance: ₹{new_balance:.2f}")
                
                self.add_transaction("DEPOSIT", amount, description, new_balance)
                self.save_data()
            else:
                print(Fore.RED + "❌ Invalid deposit amount!")
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter a number.")

    def transfer(self):
        """Transfer money to another account"""
        user_data = self.get_user_data()
        
        # Find recipient by account number
        recipient_acc = input(Fore.YELLOW + "Enter recipient account number: ").strip()
        recipient = None
        recipient_username = None
        
        for username, data in self.users.items():
            if data['account_number'] == recipient_acc:
                recipient = data
                recipient_username = username
                break
        
        if not recipient:
            print(Fore.RED + "❌ Recipient account not found!")
            return
        
        if recipient_acc == user_data['account_number']:
            print(Fore.RED + "❌ Cannot transfer to your own account!")
            return
        
        try:
            amount = float(input(Fore.YELLOW + "Enter amount to transfer: ₹"))
            if amount > user_data['balance']:
                print(Fore.RED + "❌ Insufficient funds!")
                print(Fore.CYAN + f"Available balance: ₹{user_data['balance']:.2f}")
            elif amount <= 0:
                print(Fore.RED + "❌ Invalid transfer amount!")
            else:
                description = input(Fore.YELLOW + "Enter description (optional): ").strip()
                if not description:
                    description = f"Transfer to {recipient['full_name']}"
                
                # Deduct from sender
                self.users[self.current_user]['balance'] -= amount
                sender_new_balance = self.users[self.current_user]['balance']
                
                # Add to recipient
                self.users[recipient_username]['balance'] += amount
                recipient_new_balance = self.users[recipient_username]['balance']
                
                print(Fore.GREEN + f"✅ Transfer successful!")
                print(Fore.CYAN + f"💵 Amount transferred: ₹{amount:.2f}")
                print(Fore.CYAN + f"👤 To: {recipient['full_name']}")
                print(Fore.CYAN + f"🆔 Account: {recipient_acc}")
                print(Fore.CYAN + f"💰 Your new balance: ₹{sender_new_balance:.2f}")
                
                # Record transaction for sender
                self.add_transaction("TRANSFER_OUT", -amount, f"Transfer to {recipient['full_name']} - {description}", sender_new_balance)
                
                # Record transaction for recipient
                recipient_transaction = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'TRANSFER_IN',
                    'amount': amount,
                    'description': f"Transfer from {user_data['full_name']} - {description}",
                    'balance_after': recipient_new_balance
                }
                self.users[recipient_username]['transactions'].append(recipient_transaction)
                
                self.save_data()
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter a number.")

    def mini_statement(self):
        """Show recent transactions"""
        user_data = self.get_user_data()
        transactions = user_data['transactions']
        
        print(Fore.MAGENTA + "\n📜 MINI STATEMENT (Last 10 Transactions)")
        print("=" * 50)
        
        if not transactions:
            print(Fore.YELLOW + "No transactions yet.")
        else:
            recent_transactions = transactions[-10:]
            for i, t in enumerate(reversed(recent_transactions), 1):
                timestamp = datetime.fromisoformat(t['timestamp'])
                amount_color = Fore.GREEN if t['amount'] >= 0 else Fore.RED
                amount_symbol = "+" if t['amount'] >= 0 else ""
                
                print(f"{i:2d}. {timestamp.strftime('%d-%m-%Y %H:%M')}")
                print(f"    Type: {t['type']}")
                print(f"    Amount: {amount_color}{amount_symbol}₹{abs(t['amount']):.2f}")
                print(f"    Description: {t['description']}")
                print(f"    Balance: ₹{t['balance_after']:.2f}")
                print("-" * 40)

    def full_statement(self):
        """Show all transactions"""
        user_data = self.get_user_data()
        transactions = user_data['transactions']
        
        print(Fore.MAGENTA + "\n📜 FULL TRANSACTION HISTORY")
        print("=" * 40)
        
        if not transactions:
            print(Fore.YELLOW + "No transactions yet.")
            return
        
        print(f"Total transactions: {len(transactions)}")
        print("-" * 60)
        
        for i, t in enumerate(transactions, 1):
            timestamp = datetime.fromisoformat(t['timestamp'])
            amount_color = Fore.GREEN if t['amount'] >= 0 else Fore.RED
            amount_symbol = "+" if t['amount'] >= 0 else ""
            
            print(f"{i:3d}. {timestamp.strftime('%d-%m-%Y %H:%M:%S')}")
            print(f"     Type: {t['type']}")
            print(f"     Amount: {amount_color}{amount_symbol}₹{abs(t['amount']):.2f}")
            print(f"     Description: {t['description']}")
            print(f"     Balance: ₹{t['balance_after']:.2f}")
            print("-" * 50)

    def export_transactions(self):
        """Export transaction history to CSV"""
        user_data = self.get_user_data()
        transactions = user_data['transactions']
        
        if not transactions:
            print(Fore.YELLOW + "No transactions to export!")
            return
        
        filename = f"{user_data['account_number']}_transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Date', 'Time', 'Type', 'Amount', 'Description', 'Balance After']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write account info
                csvfile.write(f"# Account Holder: {user_data['full_name']}\n")
                csvfile.write(f"# Account Number: {user_data['account_number']}\n")
                csvfile.write(f"# Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                csvfile.write(f"# Total Transactions: {len(transactions)}\n\n")
                
                # Write transactions
                for t in transactions:
                    timestamp = datetime.fromisoformat(t['timestamp'])
                    writer.writerow({
                        'Date': timestamp.strftime('%Y-%m-%d'),
                        'Time': timestamp.strftime('%H:%M:%S'),
                        'Type': t['type'],
                        'Amount': t['amount'],
                        'Description': t['description'],
                        'Balance After': t['balance_after']
                    })
            
            print(Fore.GREEN + f"✅ Transactions exported successfully!")
            print(Fore.CYAN + f"📄 File: {filename}")
            print(Fore.CYAN + f"📊 Total transactions: {len(transactions)}")
            
        except Exception as e:
            print(Fore.RED + f"❌ Error exporting transactions: {e}")

    def interest_calculator(self):
        """Calculate simple and compound interest"""
        user_data = self.get_user_data()
        current_balance = user_data['balance']
        
        print(Fore.CYAN + "\n💰 INTEREST CALCULATOR")
        print("=" * 30)
        print(Fore.CYAN + f"Current Balance: ₹{current_balance:.2f}")
        
        try:
            principal = float(input(Fore.YELLOW + f"Enter principal amount (default ₹{current_balance:.2f}): ") or current_balance)
            years = float(input(Fore.YELLOW + "Enter time period (years): "))
            rate = float(input(Fore.YELLOW + "Enter annual interest rate (%): "))
            
            # Simple Interest
            simple_interest = (principal * rate * years) / 100
            simple_total = principal + simple_interest
            
            # Compound Interest (compounded annually)
            compound_total = principal * ((1 + rate/100) ** years)
            compound_interest = compound_total - principal
            
            print(Fore.MAGENTA + "\n📊 INTEREST CALCULATION RESULTS")
            print("=" * 40)
            print(Fore.CYAN + f"💰 Principal Amount: ₹{principal:.2f}")
            print(Fore.CYAN + f"📅 Time Period: {years} years")
            print(Fore.CYAN + f"📈 Interest Rate: {rate}% per annum")
            print()
            print(Fore.YELLOW + "SIMPLE INTEREST:")
            print(Fore.GREEN + f"  Interest Amount: ₹{simple_interest:.2f}")
            print(Fore.GREEN + f"  Total Amount: ₹{simple_total:.2f}")
            print()
            print(Fore.YELLOW + "COMPOUND INTEREST (Annual):")
            print(Fore.GREEN + f"  Interest Amount: ₹{compound_interest:.2f}")
            print(Fore.GREEN + f"  Total Amount: ₹{compound_total:.2f}")
            print()
            print(Fore.CYAN + f"💡 Compound interest advantage: ₹{compound_interest - simple_interest:.2f}")
            
        except ValueError:
            print(Fore.RED + "❌ Invalid input! Please enter valid numbers.")

    def account_summary(self):
        """Show detailed account summary"""
        user_data = self.get_user_data()
        transactions = user_data['transactions']
        
        print(Fore.CYAN + "\n📋 ACCOUNT SUMMARY")
        print("=" * 30)
        print(Fore.CYAN + f"👤 Name: {user_data['full_name']}")
        print(Fore.CYAN + f"🆔 Account Number: {user_data['account_number']}")
        print(Fore.CYAN + f"📅 Account Created: {datetime.fromisoformat(user_data['created_date']).strftime('%d-%m-%Y')}")
        print(Fore.CYAN + f"💰 Current Balance: ₹{user_data['balance']:.2f}")
        print(Fore.CYAN + f"📊 Total Transactions: {len(transactions)}")
        
        if transactions:
            # Calculate transaction statistics
            deposits = [t for t in transactions if t['type'] in ['DEPOSIT', 'TRANSFER_IN']]
            withdrawals = [t for t in transactions if t['type'] in ['WITHDRAWAL', 'TRANSFER_OUT']]
            
            total_deposits = sum(t['amount'] for t in deposits)
            total_withdrawals = sum(abs(t['amount']) for t in withdrawals)
            
            print(Fore.GREEN + f"💸 Total Deposits: ₹{total_deposits:.2f}")
            print(Fore.RED + f"💳 Total Withdrawals: ₹{total_withdrawals:.2f}")
            
            # Last transaction
            last_transaction = transactions[-1]
            last_date = datetime.fromisoformat(last_transaction['timestamp'])
            print(Fore.YELLOW + f"🕒 Last Transaction: {last_date.strftime('%d-%m-%Y %H:%M')}")

    def main_menu(self):
        """Main banking menu"""
        user_data = self.get_user_data()
        
        while True:
            print(Fore.CYAN + f"\n══════════════════════════════════")
            print(Fore.CYAN + f"   ✨ PyBank - Welcome {user_data['full_name'][:20]} ✨")
            print(Fore.CYAN + f"══════════════════════════════════")
            print("1️⃣   Display Balance")
            print("2️⃣   Withdraw Money")
            print("3️⃣   Deposit Money")
            print("4️⃣   Transfer Money")
            print("5️⃣   Mini Statement")
            print("6️⃣   Full Transaction History")
            print("7️⃣   Interest Calculator")
            print("8️⃣   Account Summary")
            print("9️⃣   Export Transactions")
            print("🔟  Change Password")
            print("0️⃣   Logout")
            print("══════════════════════════════════")

            choice = input(Fore.YELLOW + "Enter your choice (0-10): ").strip()

            if choice == '1':
                self.balance()
            elif choice == '2':
                self.withdraw()
            elif choice == '3':
                self.deposit()
            elif choice == '4':
                self.transfer()
            elif choice == '5':
                self.mini_statement()
            elif choice == '6':
                self.full_statement()
            elif choice == '7':
                self.interest_calculator()
            elif choice == '8':
                self.account_summary()
            elif choice == '9':
                self.export_transactions()
            elif choice == '10':
                self.change_password()
            elif choice == '0':
                confirm = input(Fore.YELLOW + "Are you sure you want to logout? (y/n): ").lower()
                if confirm == 'y':
                    print(Fore.GREEN + f"👋 Goodbye, {user_data['full_name']}! Thank you for using PyBank!")
                    self.current_user = None
                    break
            else:
                print(Fore.RED + "❌ Invalid choice! Please try again.")

    def change_password(self):
        """Change user password"""
        print(Fore.CYAN + "\n🔐 CHANGE PASSWORD")
        print("=" * 25)
        
        current_password = getpass.getpass(Fore.YELLOW + "Enter current password: ")
        
        if self.users[self.current_user]['password_hash'] != self.hash_password(current_password):
            print(Fore.RED + "❌ Incorrect current password!")
            return
        
        while True:
            new_password = getpass.getpass(Fore.YELLOW + "Enter new password: ")
            if len(new_password) < 6:
                print(Fore.RED + "❌ Password must be at least 6 characters!")
                continue
            confirm_password = getpass.getpass(Fore.YELLOW + "Confirm new password: ")
            if new_password != confirm_password:
                print(Fore.RED + "❌ Passwords don't match!")
                continue
            break
        
        self.users[self.current_user]['password_hash'] = self.hash_password(new_password)
        self.save_data()
        print(Fore.GREEN + "✅ Password changed successfully!")

    def run(self):
        """Main application loop"""
        print(Fore.CYAN + "══════════════════════════════════")
        print(Fore.CYAN + "    ✨ Welcome to Enhanced PyBank ✨")
        print(Fore.CYAN + "         Your Digital Banking Solution")
        print(Fore.CYAN + "══════════════════════════════════")
        
        while True:
            if not self.current_user:
                print(Fore.CYAN + "\n🏦 MAIN MENU")
                print("=" * 15)
                print("1️⃣  Login")
                print("2️⃣  Create New Account")
                print("3️⃣  Exit")
                print("=" * 15)
                
                choice = input(Fore.YELLOW + "Choose an option: ").strip()
                
                if choice == '1':
                    if self.login():
                        self.main_menu()
                elif choice == '2':
                    self.create_account()
                elif choice == '3':
                    confirm = input(Fore.YELLOW + "Are you sure you want to exit? (y/n): ").lower()
                    if confirm == 'y':
                        print(Fore.GREEN + "👋 Thank you for using PyBank! Have a great day!")
                        break
                else:
                    print(Fore.RED + "❌ Invalid choice! Please enter 1, 2, or 3.")
            else:
                self.main_menu()

if __name__ == '__main__':
    try:
        bank_system = PyBankSystem()
        bank_system.run()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n👋 Thank you for using PyBank! Goodbye!")
    except Exception as e:
        print(Fore.RED + f"\n❌ An error occurred: {e}")
        print(Fore.YELLOW + "Please contact support if the problem persists.")
