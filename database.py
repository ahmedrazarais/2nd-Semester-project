from connection import *



class Database_Creation(Connection):
    """This class is child class having parent Connection class that creates database name store 
        in which 3 tables created accounts table, accounts for sellers and accounts for customers 
        to save details ."""
    
    def __init__(self):
        super().__init__()   # calling parent constructor

    
    # Method to create database name 'store'
    def create_database(self):
        """This method create database name store and when database
           Created successfully it returns nothing just make database 
           name store or raise an error if getting in creation of database"""
        
       # use try except to avoid program from crush
        try:
            # query to make database use if not exists keyword.
            db_query="CREATE DATABASE IF NOT EXISTS store"

            # execute that query
            self.cursor.execute(db_query)

            # commit the change
            self.conn.commit()

           

        
    
            
        # if getting error in database creation raise an error
        except mysql.connector.Error as e:
            print_error(f"Error in database creation as :{e}")
            exit() # wehn database not creted successfully

    

    # Method to create table for accounts where accounts details of users save
    def create_table_for_accounts(self):

        """This method create table for accounts in which accounts details
        of users are save table name accounts_info having multiple colmns."""

        # use try except in making table
        try:

            # fisrt exceute query to use database name store ewhich we make above
            self.cursor.execute("USE store")

            # table query to create table
            tb_query="""CREATE TABLE IF NOT EXISTS accounts_info(
                     first_name VARCHAR(50),
                     last_name VARCHAR (50),
                     address VARCHAR (50),
                     login_credential VARCHAR(60),
                     user_id VARCHAR(50),
                     password VARCHAR(50),
                     security_question VARCHAR(20),
                     account_type VARCHAR (15),
                     cataegory VARCHAR (30) 
                     )"""
            
            # execute table query
            self.cursor.execute(tb_query)

            # commit that change
            self.conn.commit()

        

        except mysql.connector.Error as e:
            print_error(f"Error in creation of accounts table {e}.")
            exit() # immediate exit when accounts table not creted successfully


    
    # Method To create table for users/customers in database store
    def create_table_for_users(self,username):

        """This method create table for user/customer in which we save customer shopping
           details many more The Table name based on user_id which user set during
           registration process..We Call this method when user complete thier registration 
           to make thier table in database."""
        
        try:
            # query to use database name store
            self.cursor.execute("USE store")

            # table query to make table for customers
            user_tb_query=f"""CREATE TABLE IF NOT EXISTS {username} (
            product_id INT,
            product_name VARCHAR(50),
            quantity INT,
            price_per_quantity INT,
            total_price INT,
            time VARCHAR (50),
            status VARCHAR (20),
            cataegory VARCHAR (30) 
            )"""

            # execute table query
            self.cursor.execute(user_tb_query)

            # commit that change
            self.conn.commit()

            

        except mysql.connector.Error as e:
            print_error(f"Error in creation table for customers as {e}.")
            exit()   # exit when table not creted 

    

    # Method to create table for sellers in store database
    def create_table_for_sellers(self,cataegory):
        """This method create table for sellers Table name based on
           cataegory that seller set suring registration process ,Method taken an 
           argument username .We Call this method when user complete thier registration 
           to make thier table in database."""
        
        try:
            # use database store
            self.cursor.execute("USE store")

            # query for seller table
            seller_tb_query=f"""CREATE TABLE IF NOT EXISTS {cataegory} (
            product_id INT,
            product_name VARCHAR (60),
            quantity INT,
            price INT)"""

            # execute that query
            self.cursor.execute(seller_tb_query)

            # commit that change
            self.conn.commit()


        except mysql.connector.Error as e:
            print_error(f"Error in creation table for sellers {e}.")
            exit()  # exit when table not created


# Making objects of both classess and call methods that should be called before starting program

database=Database_Creation()
database.create_database()
database.create_table_for_accounts()
