import database

class operations_history():   
    def __init__(self, user_id):
        self.db = database.database()
        self.user_id = user_id
      
        
    def add_operation(self, operation_type, amount, crypto_currency = None, price = None, timestramp=None):
        try:
            self.db.add_data("insert into crypto_operations(user_id, operation_type, crypto_id, amount, price_per_unit, total_value, timestamp) values(?,?,?,?,?,?,?)", 
                             (self.user_id, operation_type, crypto_currency, amount, price))
            print("Operation added successfully.")
        except Exception as ex:
            print(f"Error adding operation: {ex}")
    
    
    def show_history(self):
        try:
            history = self.db.get_data("select * from operations_history where userid = ?", (self.user_id,))
            return history
        except Exception as ex:
            print(f"Error retrieving history: {ex}")
                  

