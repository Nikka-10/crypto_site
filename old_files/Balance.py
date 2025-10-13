import database

class Balance_Operations():
    def __init__(self, user_id):
        self.db = database.database()
        self.connection_str = self.db.connection_str
        self.user_id = user_id
        
        
    def insert_money(self, insert_amount) -> None:
        try:
            if self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)) is None:
                raise ValueError("User not found or balance is not set.")
            if insert_amount <= 0:
                raise ValueError("amount must be a positive number.")
            self.db.add_data("update user_info set balance = ? where user_id = ?", (insert_amount, self.user_id))
        except ValueError as error:
            print(error)
    
    
    def withdraw_money(self, withdraw_amount) -> None:
        try:
            balance = float(self.db.get_data("select balance from user_info where user_id = ?", (self.user_id,)))
            if withdraw_amount <= 0:
                raise ValueError("Withdraw amount must be a positive number.")
            if withdraw_amount > balance:
                raise ValueError("Insufficient balance.")
            new_balance = balance - withdraw_amount
            self.db.add_data("update user_info set balance = ? where user_id = ?", (new_balance, self.user_id))
        except ValueError as error:
            print(error)