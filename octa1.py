import datetime

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.balance = 0
        self.transaction_history = []

    def add_transaction(self, transaction_type, amount):
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'date': datetime.datetime.now()
        }
        self.transaction_history.append(transaction)

class ATM:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id, pin):
        if user_id in self.users:
            print(f"User ID {user_id} already exists.")
        else:
            self.users[user_id] = User(user_id, pin)
            print(f"User {user_id} added successfully.")

    def authenticate(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            return user
        else:
            return None

    def transaction_history(self, user):
        print("Transaction History:")
        for transaction in user.transaction_history:
            print(f"{transaction['date']} - {transaction['type']}: ${transaction['amount']}")

    def withdraw(self, user, amount):
        if user.balance >= amount:
            user.balance -= amount
            user.add_transaction("Withdraw", amount)
            print(f"Withdrawal of ${amount} successful. New balance: ${user.balance}")
        else:
            print("Insufficient balance.")

    def deposit(self, user, amount):
        user.balance += amount
        user.add_transaction("Deposit", amount)
        print(f"Deposit of ${amount} successful. New balance: ${user.balance}")

    def transfer(self, user, target_user_id, amount):
        target_user = self.users.get(target_user_id)
        if target_user:
            if user.balance >= amount:
                user.balance -= amount
                target_user.balance += amount
                user.add_transaction("Transfer to " + target_user_id, amount)
                target_user.add_transaction("Transfer from " + user.user_id, amount)
                print(f"Transfer of ${amount} to {target_user_id} successful. New balance: ${user.balance}")
            else:
                print("Insufficient balance.")
        else:
            print(f"Target user {target_user_id} does not exist.")

def main():
    atm = ATM()
    atm.add_user("user1", "1234")
    atm.add_user("user2", "5678")

    while True:
        user_id = input("Enter user ID: ")
        pin = input("Enter PIN: ")
        user = atm.authenticate(user_id, pin)

        if user:
            print("Authentication successful. ATM functionality unlocked.")
            while True:
                print("\nOptions:")
                print("1. Transaction History")
                print("2. Withdraw")
                print("3. Deposit")
                print("4. Transfer")
                print("5. Quit")

                choice = input("Enter your choice: ")
                if choice == '1':
                    atm.transaction_history(user)
                elif choice == '2':
                    amount = float(input("Enter amount to withdraw: "))
                    atm.withdraw(user, amount)
                elif choice == '3':
                    amount = float(input("Enter amount to deposit: "))
                    atm.deposit(user, amount)
                elif choice == '4':
                    target_user_id = input("Enter target user ID: ")
                    amount = float(input("Enter amount to transfer: "))
                    atm.transfer(user, target_user_id, amount)
                elif choice == '5':
                    print("Thank you for using the ATM. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Authentication failed. Please try again.")

if __name__ == "__main__":
    main()
