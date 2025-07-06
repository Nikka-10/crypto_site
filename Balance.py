import database

class Balance_Operations():
    def __init__(self, user_id):
        self.db = database.database()
        self.connection_str = self.db.connection_str
        self.user_id = user_id
        
    def insert_balance(self):
        try:
            if self.db.get_data("select balance from user_info where userid = ?", (self.user_id,)) is None:
                raise ValueError("User not found or balance is not set.")
            balance = float(input("enter your balance: "))
            if balance <= 0:
                raise ValueError("Balance must be a positive number.")
            self.db.add_data("update user_info set balance = ? where userid = ?", (balance, self.user_id))
            print("Balance added successfully.")
        except ValueError as error:
            print(error)
    
    def withdraw_balance(self):
        try:
            balance = float(self.db.get_data("select balance from user_info where userid = ?", (self.user_id,)))
            withdraw_amount = float(input("how much money you want to withdraw: "))
            if withdraw_amount <= 0:
                raise ValueError("Withdraw amount must be a positive number.")
            if withdraw_amount > balance:
                raise ValueError("Insufficient balance.")
            new_balance = balance - withdraw_amount
            self.db.add_data("update user_info set balance = ? where userid = ?", (new_balance, self.user_id))
            print(f"Withdrawal successful. New balance: {new_balance}")
        except ValueError as error:
            print(error)