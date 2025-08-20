import pyodbc

class database(): 
    def __init__(self, server = 'NIKA\\SQLEXPRESS', database = 'crypto_db'):
        self.connection_str = f"""
            driver={{ODBC driver 18 for SQL Server}};
            server={server};
            database={database};
            TrustServerCertificate=Yes;
            Trusted_Connection=yes;;
            """.strip()
         
            
    def get_connection(self) -> str:    
        return self.connection_str
    
    
    def get_data(self, sql_code, sql_input) -> str:
        with pyodbc.connect(self.connection_str) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_code, sql_input)
                result = cursor.fetchone()
                return result[0]
            
            
    def add_data(self, sql_code, sql_input) -> bool:
        with pyodbc.connect(self.connection_str) as conn:
                cursor = conn.cursor()
                cursor.execute(sql_code, sql_input)
                return True
